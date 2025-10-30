from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from openai import OpenAI
import os

load_dotenv()

class Eleven: # this was sorta ripped from elevenlabs docs
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs = ElevenLabs(api_key=self.api_key)
        self.bonnieVoice = "PiE7En4dJh0s0VBPcv22"

    def generateSpeech(self, text, voice_id, model_id="eleven_v3", output_format="mp3_44100_128"):
        audio = self.elevenlabs.text_to_speech.stream(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
        stream(audio)
        
class OpenRouter:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=self.api_key)

    def generateLines(self): # also ripped from openrouter docs
        completion = self.openrouter.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "user",
                    "content": "What is the meaning of life?" #placeholder
                }
            ]
        )
        return completion.choices[0].message.content
