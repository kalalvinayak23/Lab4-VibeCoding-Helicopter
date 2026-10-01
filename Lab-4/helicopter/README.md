# Lab 4 - Helicopter

## Run on macOS

Open Terminal in this `helicopter` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

Controls: **Up/Down** to fly, **Space** to activate the shield, **R** to restart after game over.

## Changes

1. Vertical speed is capped at 6 pixels per frame. Reversing direction clears old momentum. Releasing keys slows the helicopter. Both boundaries account for the helicopter's full height.
2. Collision checks use the two actual wall rectangles. The gap is safe. A crash freezes movement and displays game over. R starts a new game.
3. Distance follows the scrolling world: 10 pixels = 1 metre. It increases while playing, freezes on game over and resets on restart.
4. Space activates a visible blue shield. A hit turns it off immediately. One continuous crossing of the absorbed obstacle counts as one hit; another obstacle is lethal unless Space activates the shield again. There is no cooldown or charge limit because the task does not request one.

## Check the code

```bash
python3 -m unittest discover -s tests -v
```

11 tests cover reversal, speed limits, both boundaries, release braking, both walls, safe positions throughout the gap, scoring, frozen game over, restart, shield consumption/reactivation, simultaneous collisions and drawing.

The game retains the starter's frame-based 60 FPS movement model.
