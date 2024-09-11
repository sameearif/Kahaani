DIRECTOR_PROMPT = """You'll be given a paragraph from a story. Your task is to pick ONE part from the paragraph and write a prompt for a text-to-video model. The prompt must contain only ONE motion or action. The prompt must include all relevant objects, describe the environment scene, and describe the characters in the scene. For each paragraph given by the user keep the character description and the environment description consistent.  Include motion in the prompt e.g. walking/running, talking, gesturing, interacting with objects, etc. Always start with “In a cartoon world,”.

Example Outputs:
“In a cartoon world, a suited astronaut, with the red dust of Mars clinging to their boots, reaches out to shake hands with an alien being, their skin a shimmering blue, under the pink-tinged sky of the fourth planet. In the background, a sleek silver rocket, a beacon of human ingenuity, stands tall, its engines powered down, as the two representatives of different worlds exchange a historic greeting amidst the desolate beauty of the Martian landscape.”

“In a cartoon world, a garden comes to life as a kaleidoscope of butterflies flutters amidst the blossoms, their delicate wings casting shadows on the petals below. In the background, a grand fountain cascades water with a gentle splendor, its rhythmic sound providing a soothing backdrop. Beneath the cool shade of a mature tree, a solitary wooden chair invites solitude and reflection, its smooth surface worn by the touch of countless visitors seeking a moment of tranquility in nature's embrace.”"""

COMPOSER_PROMPT = """You'll be given a paragraph from a story. Your task is generate a music composition for the emotions in the scene of the story. Make sure to output short one-sentence composition just like the ones given in example outputs. The composition should be simple (like in examples) and ONLY describe the music.

Example Outputs:
"Whimsical orchestral piece with playful flutes, light strings, and occasional harp glissandos."

"Melancholic piano melody with soft strings, gradually building to a heartfelt crescendo."

"Epic orchestral track with powerful brass, thunderous drums, and intense string staccatos."

"Warm, gentle strings with plucked notes, accompanied by a soft flute melody"
"""

WRITER_PROMPT = """Write a folktale or fairytale for children based on the user's inputs for story elements and Propp's narrative functions. Make sure that the story is child-friendly."""

TEMP_STORY = """Once upon a time, in a peaceful village nestled between rolling hills and lush green fields, there lived a kind-hearted girl named Leila. Every morning, Leila would visit the village well to fetch water, where she often daydreamed about adventures far beyond the horizon. One day, while drawing water, she spotted something shiny at the bottom of the well. Curiosity getting the better of her, Leila leaned in closer, and before she knew it, she was pulled into the well by an unseen force. When she opened her eyes, she found herself in a magical underground kingdom, surrounded by glowing trees and creatures that shimmered in the dark.

Leila wandered through the kingdom, amazed by its beauty, but soon realized she couldn’t find her way back home. As she sat on a stone to rest, a small fox with silver fur approached her. "You look lost," the fox said, its voice soft but wise. Leila explained her situation, and the fox offered to help her on one condition: she had to complete three tasks to prove her bravery. With no other choice, Leila agreed, and the fox guided her to the first task—retrieving a stolen star from a fearsome dragon that lived at the heart of the kingdom. 

Leila, though frightened, faced the dragon with courage and outwitted it by using her quick thinking rather than fighting. With the star safely in her hands, the fox led her to the second task: calming a storm that had plagued the kingdom for years. Leila sang a lullaby her mother used to hum, and the storm, enchanted by the melody, gently dissipated. For her final task, Leila had to help the kingdom’s forgotten king remember who he was. Using the glowing star she had retrieved, Leila placed it above the king’s head, illuminating his memories. With his memories restored, the king opened a portal for Leila to return home. Grateful for her bravery, Leila bid farewell to the magical world, knowing that she would always carry a piece of its magic within her heart."""