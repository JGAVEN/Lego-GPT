"""Simple WebSocket server for real-time collaboration.

Rooms keep a shared message history so clients can issue ``/undo`` and
``/redo`` commands. New peers receive the full history on connect.
"""
from __future__ import annotations

import asyncio
import os
from collections import defaultdict
from typing import Dict, List, Set

try:  # optional dependency
    import websockets
    from websockets.server import WebSocketServerProtocol

    WEBSOCKETS_AVAILABLE = True
except Exception:  # pragma: no cover - missing optional dep
    websockets = None  # type: ignore
    WebSocketServerProtocol = None  # type: ignore
    WEBSOCKETS_AVAILABLE = False

_rooms: Dict[str, Set[WebSocketServerProtocol]] = defaultdict(set)  # type: ignore
_history: Dict[str, List[str]] = defaultdict(list)
_redo: Dict[str, List[str]] = defaultdict(list)
_chat: Dict[str, List[str]] = defaultdict(list)


async def _broadcast_peers(room: str) -> None:
    """Notify all peers in ``room`` about the current participant count."""
    peers = _rooms.get(room)
    if not peers:
        return
    message = f"PEERS {len(peers)}"
    for peer in list(peers):
        try:
            await peer.send(message)
        except Exception:
            pass


async def _handler(ws: WebSocketServerProtocol, path: str) -> None:
    if not path.startswith("/ws/"):
        await ws.close()
        return
    room = path.split("/", 2)[-1]
    peers = _rooms[room]
    peers.add(ws)
    await _broadcast_peers(room)
    # Send existing history to the new peer
    for item in _history[room]:
        await ws.send(item)
    for chat in _chat[room]:
        await ws.send(f"CHAT: {chat}")
    try:
        async for msg in ws:
            broadcast = None
            if msg == "/undo":
                if _history[room]:
                    item = _history[room].pop()
                    _redo[room].append(item)
                    broadcast = f"UNDO: {item}"
            elif msg == "/redo":
                if _redo[room]:
                    item = _redo[room].pop()
                    _history[room].append(item)
                    broadcast = f"REDO: {item}"
            elif msg.startswith("/chat "):
                chat = msg.split(" ", 1)[1]
                _chat[room].append(chat)
                broadcast = f"CHAT: {chat}"
            else:
                _history[room].append(msg)
                _redo[room].clear()
                broadcast = msg
            if broadcast:
                for peer in list(peers):
                    if peer != ws:
                        await peer.send(broadcast)
    finally:
        peers.remove(ws)
        if peers:
            await _broadcast_peers(room)
        else:
            del _rooms[room]
            _history.pop(room, None)
            _redo.pop(room, None)
            _chat.pop(room, None)


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
