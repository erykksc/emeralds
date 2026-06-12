# Emeralds

Multiplayer board game — collect gems, avoid traps, gather relics.
Features a Pygame renderer and Tornado WebSocket server for multiplayer.

Players connect via web browser (for example on their phones) to the WebSocket server (`http://<ip>:<port>`) to control their actions.

## Demo

## Rules

**Goal:** collect as many gems as possible by exploring the cave.

- In the cave you'll find gems, relicts, and traps.
- Gems found are split equally among players who are exploring; any remainder stays in place.
- Relicts stay in place and are only collected when exactly one player returns to save them — worth their value in gems.
- If the same type of trap is triggered twice in one round, all exploring players lose all gems collected that round.
- You can go back at any time to save the gems you've collected this round and pick up any gems left behind (split equally among returning players).
- The longer you explore the more gems you can collect, but the danger to lose them all increases

## Setup

```bash
# Install uv if you don't have it: https://docs.astral.sh/uv/
uv sync
```

## Run

```bash
uv run python3 pygame_version/main.py
```
