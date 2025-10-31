from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from openai import OpenAI
import os
import threading

load_dotenv()

# Animatronic personality profiles
ANIMATRONIC_PROFILES = {
    "Freddy": {
        "voice_id": "PiE7En4dJh0s0VBPcv22",  # Need to find actual voice IDs
        "personality": "Freddy is the leader, calm and confident. He speaks in a low, menacing tone. His lines are commanding and ominous.",
        "traits": ["commanding", "patient", "menacing", "hungry"],
        "example_lines": ["I'm always watching", "Time to play", "You can't escape me"]
    },
    "Bonnie": {
        "voice_id": "PiE7En4dJh0s0VBPcv22",
        "personality": "Bonnie is aggressive and eager. He speaks quickly and with excitement about the hunt. His lines are taunting and playful in a twisted way.",
        "traits": ["aggressive", "eager", "taunting", "chaotic"],
        "example_lines": ["I'm coming for you", "Found you!", "Can't hide forever"]
    },
    "Chica": {
        "voice_id": "PiE7En4dJh0s0VBPcv22",
        "personality": "Chica is curious and observant. She speaks in a childlike but eerie way. Her lines are innocent-sounding but disturbing.",
        "traits": ["curious", "childlike", "observant", "innocent"],
        "example_lines": ["Where are you?", "I can see you", "Let me in"]
    },
    "Foxy": {
        "voice_id": "PiE7En4dJh0s0VBPcv22",
        "personality": "Foxy is unpredictable and wild. He speaks erratically with broken pauses. His lines suggest danger and instability.",
        "traits": ["unpredictable", "feral", "broken", "chaotic"],
        "example_lines": ["Out of order... or am I?", "Can't stop me", "I'm free"]
    }
}

SYSTEM_PROMPT = """You are a voice line generator for a horror game. You create short, terrifying dialogue lines for animatronic characters.

Rules:
1. Generate ONLY one short line (1 short sentence)
2. The line should be eerie, taunting, or ominous based on the situation
3. Lines should feel unpredictable and personal - never generic
4. Keep it simple and natural - avoid overly dramatic language
5. Lines should be 5-15 words maximum
6. Make it sound like it could be whispered, growled, or spoken by a machine
7. Never ask questions back - only make statements or observations
8. Avoid meta references to the game itself"""


class Eleven: # this was sorta ripped from elevenlabs docs
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs = ElevenLabs(api_key=self.api_key)

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

    def generateVoiceLine(self, animatronic_name, event_type, context=""):
        """Generate a single voice line based on event and animatronic personality"""

        profile = ANIMATRONIC_PROFILES.get(animatronic_name, ANIMATRONIC_PROFILES["Bonnie"])

        # Build the user prompt based on event type
        user_prompts = {
            "sighting": f"Create a menacing one-liner for {animatronic_name} who has just been spotted by the player. {profile['personality']}. Make it threatening but brief.",

            "movement": f"Create a one-liner for {animatronic_name} as it moves closer to the player's location. {profile['personality']}. Convey movement and hunger.",

            "door_lock": f"Create a dismissive or menacing one-liner for {animatronic_name} reacting to a door being locked against it. {profile['personality']}. Should sound frustrated or patient.",

            "door_unlock": f"Create an excited or menacing one-liner for {animatronic_name} as a door opens for it. {profile['personality']}. Should sound triumphant.",

            "power_warning": f"Create a taunting one-liner for {animatronic_name} as the player's power fails. {profile['personality']}. Reference the darkness or lack of escape.",

            "waiting": f"Create an eerie one-liner for {animatronic_name} while stalking the player. {profile['personality']}. Should sound patient, like a predator waiting.",
        }

        prompt = user_prompts.get(event_type, user_prompts["waiting"])
        if context:
            prompt += f" Context: {context}"

        try:
            completion = self.openrouter.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating voice line: {e}")
            # Fallback lines if API fails
            fallbacks = {
                "Freddy": "I'm always here.",
                "Bonnie": "I'm coming.",
                "Chica": "Where are you?",
                "Foxy": "I'm free."
            }
            return fallbacks.get(animatronic_name, "I see you.")

    def generateLines(self): # kept for backwards compatibility
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
