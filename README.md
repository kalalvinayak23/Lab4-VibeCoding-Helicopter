# Lab 4 - VibeCoding: Helicopter

## Run on macOS

```bash
cd Lab-4/helicopter
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

**Controls:** Up/Down to fly, Space to activate a one-hit shield, R to restart after game over.

## Deliverables

All required files are in [Lab-4](Lab-4):

- [Updated game](Lab-4/helicopter)
- [Before video](Lab-4/videos/before.mp4) and [after video](Lab-4/videos/after.mp4): 10 seconds each, captured from actual gameplay with scripted controls.
- [Chat history PDF](Lab-4/Chat_History.pdf)

The game includes responsive movement, screen boundaries, collision/game over, distance scoring, and a one-hit shield. Each task has a separate commit.

## Tests

From `Lab-4/helicopter`:

```bash
python3 -m unittest discover -s tests -v
```

All 12 tests passed. The shared conversation link still needs to be added for the assignment checklist.

Starter source: https://github.com/SETAPESU26/08_helicopter
