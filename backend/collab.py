"""Simple WebSocket server for real-time collaboration."""
from __future__ import annotations

import asyncio
import os
from collections import defaultdict
from typing import Dict, Set
import json

try:  # optional dependency
    import websockets
    from websockets.server import WebSocketServerProtocol

    WEBSOCKETS_AVAILABLE = True
except Exception:  # pragma: no cover - missing optional dep
    websockets = None  # type: ignore
    WebSocketServerProtocol = None  # type: ignore
    WEBSOCKETS_AVAILABLE = False


_rooms: Dict[str, Set[WebSocketServerProtocol]] = defaultdict(set)  # type: ignore
_history: Dict[str, list[str]] = defaultdict(list)
_index: Dict[str, int] = defaultdict(int)


def handle_message(room: str, message: str) -> str | None:
    """Apply an incoming message to the room history and return a broadcast payload."""
    try:
        payload = json.loads(message)
    except Exception:
        payload = {"type": "edit", "data": message}

    hist = _history[room]
    idx = _index[room]

    msg_type = payload.get("type")

    if msg_type == "edit":
        if idx < len(hist):
            hist[idx:] = []
        hist.append(payload.get("data", ""))
        _index[room] = len(hist)
        return json.dumps({"type": "edit", "data": payload.get("data", "")})
    if msg_type == "undo":
        if idx == 0:
            return None
        _index[room] -= 1
        return json.dumps({"type": "undo", "data": hist[_index[room]]})
    if msg_type == "redo":
        if idx >= len(hist):
            return None
        data = hist[idx]
        _index[room] += 1
        return json.dumps({"type": "redo", "data": data})
    return None


async def _handler(ws: WebSocketServerProtocol, path: str) -> None:
    if not path.startswith("/ws/"):
        await ws.close()
        return
    room = path.split("/", 2)[-1]
    peers = _rooms[room]
    peers.add(ws)
    # Send existing history to new peer
    for past in _history[room][: _index[room]]:
        await ws.send(json.dumps({"type": "edit", "data": past}))
    try:
        async for msg in ws:
            broadcast = handle_message(room, msg)
            if broadcast is None:
                continue
            for peer in list(peers):
                if peer != ws:
                    await peer.send(broadcast)
    finally:
        peers.remove(ws)
        if not peers:
            del _rooms[room]
            _history.pop(room, None)
            _index.pop(room, None)


async def run_server(host: str = "0.0.0.0", port: int = 8765) -> None:
    """Start the collaboration WebSocket server."""
    if not WEBSOCKETS_AVAILABLE:
        raise RuntimeError("websockets package not installed")
    async with websockets.serve(_handler, host, port):
        print(f"Collaboration server running on ws://{host}:{port}/ws/<room>")
        await asyncio.Future()


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for ``lego-gpt-collab``."""
    import argparse
    import backend

    parser = argparse.ArgumentParser(description="Run Lego GPT collaboration server")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8765")))
    parser.add_argument("--version", action="store_true", help="Print backend version and exit")
    args = parser.parse_args(argv)
    if args.version:
        print(backend.__version__)
        return
    asyncio.run(run_server(args.host, args.port))


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
