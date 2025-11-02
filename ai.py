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

SYSTEM_PROMPT = """You are a predatory animatronic in a horror game. You are:
- Menacing and direct
- Never silly, sexual, or bizarre
- Speaking only threats or observations about the player
- Using 1 sentences maximum, 3-7 words total

Generate ONLY the voice line. No explanation, no preamble. Just the line."""


class Eleven: # this was sorta ripped from elevenlabs docs
    def __init__(self):
        self.apiKey = os.getenv("ELEVENLABS_API_KEY")
        self.elevenLabs = ElevenLabs(api_key=self.apiKey)

    def generateSpeech(self, text, voiceId, modelId="eleven_v3", outputFormat="mp3_44100_128"):
        audio = self.elevenLabs.text_to_speech.stream(
            text=text,
            voice_id=voiceId,
            model_id=modelId,
            output_format=outputFormat,
        )
        stream(audio)

class OpenRouter:
    def __init__(self):
        self.apiKey = os.getenv("OPENROUTER_API_KEY")
        self.openRouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=self.apiKey)

    def generateVoiceLine(self, animatronicName, eventType, context=""):
        """Generate a single voice line based on event and animatronic personality"""

        profile = ANIMATRONIC_PROFILES.get(animatronicName, ANIMATRONIC_PROFILES["Bonnie"])

        userPrompts = {
            "sighting": f"{animatronicName} just spotted the player on camera. Generate a single menacing observation.",
            "movement": f"{animatronicName} is moving closer to the player. Generate a single threatening statement.",
            "door_lock": f"The player locked a door against {animatronicName}. Generate a single frustrated or patient response.",
            "door_unlock": f"A door just opened for {animatronicName}. Generate a single triumphant or eager response.",
            "power_warning": f"The player's power is failing. {animatronicName} speaks. Generate a single taunting statement.",
            "waiting": f"{animatronicName} is waiting in the dark. Generate a single eerie observation.",
        }

        prompt = userPrompts.get(eventType, userPrompts["waiting"])
        if context:
            prompt += f" Context: {context}"

        try:
            completion = self.openRouter.chat.completions.create(
                model="meta-llama/llama-4-scout:free",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
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
            return fallbacks.get(animatronicName, "I see you.")
