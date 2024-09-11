import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from moviepy.editor import AudioFileClip
import asyncio
import time
from agents import *
from utils import TEMP_STORY

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

writer = Writer("kahaani/llama-3.1-8b-gutenberb-propp-1", "cuda")
director = Director("gpt-4o")
animator = Animator("THUDM/CogVideoX-5b", "cuda")
composer = Composer("gpt-4o")
musician = Musician("facebook/musicgen-large", "cuda")

class WriterInput(BaseModel):
    prompt: str

class AnimatorInput(BaseModel):
    paragraph: str

@app.post("/writer")
async def generate_story(writer_input: WriterInput):
    return StreamingResponse(writer.forward(writer_input.prompt), media_type="text/plain")

@app.post("/animator")
async def generate_animation(animator_input: AnimatorInput):
    scene = director.forward(animator_input.paragraph)
    composition = composer.forward(scene)
    video_task = animator.forward(scene)
    music_task = musician.forward(composition)
    video, music_file = await asyncio.gather(video_task, music_task)
    music = AudioFileClip(music_file)
    video = video.set_audio(music)
    video_file = time.strftime("%Y%m%d-%H%M%S") + ".mp4"
    video.write_videofile(video_file, codec="libx264", fps=24)
    def iterfile():
        with open(video_file, mode="rb") as f:
            yield from f
        os.remove(video_file)
        os.remove(music_file)

    return StreamingResponse(iterfile(), media_type="video/mp4")

