"""Simple WebSocket server for real-time collaboration."""
from __future__ import annotations

import asyncio
import os
from collections import defaultdict
from typing import Dict, Set

try:  # optional dependency
    import websockets
    from websockets.server import WebSocketServerProtocol

    WEBSOCKETS_AVAILABLE = True
except Exception:  # pragma: no cover - missing optional dep
    websockets = None  # type: ignore
    WebSocketServerProtocol = None  # type: ignore
    WEBSOCKETS_AVAILABLE = False

_rooms: Dict[str, Set[WebSocketServerProtocol]] = defaultdict(set)  # type: ignore


async def _handler(ws: WebSocketServerProtocol, path: str) -> None:
    if not path.startswith("/ws/"):
        await ws.close()
        return
    room = path.split("/", 2)[-1]
    peers = _rooms[room]
    peers.add(ws)
    try:
        async for msg in ws:
            for peer in list(peers):
                if peer != ws:
                    await peer.send(msg)
    finally:
        peers.remove(ws)
        if not peers:
            del _rooms[room]


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
