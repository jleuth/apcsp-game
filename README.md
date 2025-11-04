# apcsp-game

a fnaf clone made in pygame for apcsp (yes i know this is absurdly overqualified for the class shhhh)

## what even is this

it's basically five nights at freddy's but i made it in python because i apparently hate myself. you're a security guard trying to survive the night (6-8 minutes) while freddy, bonnie, chica, and foxy try their absolute hardest to jumpscare you into oblivion.

you've got:
- 8 different camera angles to stalk the animatronics
- doors you can lock (but they drain power like crazy)
- a power meter that laughs at your poor resource management
- AI-generated voice lines because apparently regular horror games weren't enough
- actual jumpscares with videos because i wanted nightmares

## the tech stuff (aka why this is way too extra)

- **pygame** for the main game engine
- **opencv** for the jumpscare videos
- **OpenRouter API** (LLaMA model) to generate contextual AI voice lines on the fly
- **ElevenLabs** for text-to-speech so each animatronic sounds appropriately terrifying
- probably too much code for what should've been a simple project

each animatronic has their own personality and voice, pathfinding with waypoints, and a dice-roll movement system because i wanted to be faithful to fnaf's AI. they're smarter than they have any right to be.

## how to actually run this thing

1. clone this repo (you're probably already here)
2. install the stuff:
```bash
pip install pygame opencv-python python-dotenv openai
```

3. make a `.env` file with your API keys:
```
OPENROUTER_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

4. run it:
```bash
python main.py
```

5. try not to die (you will die)

## gameplay tips

- cameras drain power but you NEED them to track the animatronics
- doors drain even MORE power but they're the only way to not get jumpscared
- if you run out of power you lose
- if an animatronic reaches your office you lose
- survive until 6 AM (or like 7 minutes) and you win
- good luck you're gonna need it

## credits

made by me for apcsp because apparently i don't understand the concept of "appropriate scope for a class project"

written with **claude** (the AI) who helped me turn this from a mess into a slightly more organized mess. claude also helped me refactor everything to camelCase and generally made this code way cleaner than it had any right to be. thanks claude you're the real MVP

also shoutout to hallie :3

## is this overkill for apcsp?

yes. absolutely. 100%. but it works and it's fun and that's what matters right?

---

if you actually play this and get jumpscared don't blame me i warned you
