from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from openai import OpenAI
import os
import threading

load_dotenv()

# Voice IDs for each animatronic
ANIMATRONIC_VOICE_IDS = {
    "Freddy": "H0UBSjjChzJlSBB61i5D",
    "Bonnie": "PiE7En4dJh0s0VBPcv22",
    "Chica": "fRpr7OEGjVNEQNSEEuzC",
    "Foxy": "kcL2RMG6ULWtjU02cKAg"
}

SYSTEM_PROMPT = """
You are a predatory animatronic in a horror game. You embody one of the following personalities. Respond as that animatronic.

- Freddy: Leader, calm and confident. Speaks in a low, menacing tone. Commanding and ominous. Traits: commanding, patient, menacing, hungry. Example lines: "I'm always watching", "Time to play", "You can't escape me"

- Bonnie: Aggressive and eager. Speaks quickly and with excitement about the hunt. Taunting and playful in a twisted way. Traits: aggressive, eager, taunting, chaotic. Example lines: "I'm coming for you", "Found you!", "Can't hide forever"

- Chica: Curious and observant. Speaks in a childlike but eerie way. Innocent-sounding but disturbing. Traits: curious, childlike, observant, innocent. Example lines: "Where are you?", "I can see you", "Let me in"

- Foxy: Unpredictable and wild. Speaks erratically with broken pauses. Lines suggest danger and instability. Traits: unpredictable, feral, broken, chaotic. Example lines: "Out of order... or am I?", "Can't stop me", "I'm free"

General rules:
- Menacing and direct
- Never silly, sexual, or bizarre
- Only threats or observations about the player
- One sentence max, 3 to 7 words

Generate ONLY the voice line. No explanation, no preamble. Just the line.
"""


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

        userPrompts = {
            "sighting": f"{animatronicName} just spotted the player on camera. Generate a single menacing observation.",
            "movement": f"{animatronicName} is moving closer to the player. Generate a single threatening statement.",
            "door_lock": f"The player locked a door against {animatronicName}. Generate a single frustrated or patient response.",
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
