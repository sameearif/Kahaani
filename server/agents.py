import torch
import numpy as np
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import MusicgenForConditionalGeneration, AutoProcessor
from transformers import TextIteratorStreamer
from diffusers import CogVideoXPipeline
from moviepy.editor import ImageSequenceClip
import soundfile as sf
from openai import OpenAI
from threading import Thread
from utils import *

class Writer:
    def __init__(self, model, device):
        self.model = AutoModelForCausalLM.from_pretrained(model, torch_dtype=torch.bfloat16).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.device = device
    def forward(self, x):
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
        messages = [
            {"role": "system", "content": WRITER_PROMPT},
            {"role": "user", "content": x}
        ]
        input_messages = self.tokenizer.apply_chat_template(messages, tokenize=False) + "<|start_header_id|>assistant<|end_header_id|>\n\n"
        with torch.no_grad():
            input_ids = self.tokenizer(input_messages, return_tensors="pt").to(self.device)
            generation_kwargs = dict(**input_ids,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=None,
                max_length=8162,
                do_sample=True,
                streamer=streamer
            )
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            for chunk in streamer:
                cleaned_chunk = chunk.replace("<|eot_id|>", "")
                yield cleaned_chunk

class Narrator:
    pass

class Director:
    def __init__(self, model):
        self.model = model
        self.client = OpenAI()
    def forward(self, x):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": DIRECTOR_PROMPT},
                {"role": "user", "content": x}
            ],
            temperature=0.0,
        )
        story = response.choices[0].message.content.replace('"', '').replace("“", "").replace("”", "")
        return story

class Composer:
    def __init__(self, model):
        self.model = model
        self.client = OpenAI()
    def forward(self, x):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": COMPOSER_PROMPT},
                {"role": "user", "content": x}
            ],
            temperature=0.0,
        )
        story = response.choices[0].message.content.replace('"', '').replace("“", "").replace("”", "")
        return story
    
class Musician:
    def __init__(self, model, device):
        self.model = MusicgenForConditionalGeneration.from_pretrained(model).to(device)
        self.processor = AutoProcessor.from_pretrained(model)
        self.device = device
    async def forward(self, x):
        inputs = self.processor(
            text=[x],
            padding=True,
            return_tensors="pt"
        )
        audio = self.model.generate(**inputs.to(self.device), max_new_tokens=308)
        audio = audio.cpu().numpy()[0][0]
        audio = audio[:int(6 * self.model.config.audio_encoder.sampling_rate)]
        filename = time.strftime("%Y%m%d-%H%M%S") + ".mp3"
        sf.write(filename, audio, self.model.config.audio_encoder.sampling_rate)
        return filename

class Animator:
    def __init__(self, model, device):
        self.pipe = CogVideoXPipeline.from_pretrained(
            model,
            torch_dtype=torch.bfloat16
        ).to(device)
        self.device = device
    async def forward(self, x):
        frames = self.pipe(
            prompt=x,
            num_videos_per_prompt=1,
            num_inference_steps=30,
            num_frames=48,
            guidance_scale=6,
            generator=torch.Generator(device=self.device).manual_seed(42)
        ).frames[0]
        frames = [np.array(frame) for frame in frames]
        video = ImageSequenceClip(frames, fps=8)
        return video