from __future__ import annotations
import asyncio
import json
import os
from typing import Set

from backend.gateway import METRICS

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
except Exception:  # pragma: no cover - optional dep missing
    websockets = None  # type: ignore
    WebSocketServerProtocol = None  # type: ignore

_clients: Set[WebSocketServerProtocol] = set()  # type: ignore


async def _handler(ws: WebSocketServerProtocol, path: str) -> None:
    _clients.add(ws)
    try:
        await ws.send(json.dumps(METRICS))
        async for _ in ws:
            pass
    finally:
        _clients.discard(ws)


async def _broadcast_loop() -> None:
    prev = None
    while True:
        data = json.dumps(METRICS)
        if data != prev:
            for ws in list(_clients):
                try:
                    await ws.send(data)
                except Exception:
                    _clients.discard(ws)
            prev = data
        await asyncio.sleep(1)


async def run_server(host: str = "0.0.0.0", port: int = 8777) -> None:
    if not websockets:
        raise RuntimeError("websockets package not installed")
    async with websockets.serve(_handler, host, port):
        print(f"Metrics server running on ws://{host}:{port}")
        await _broadcast_loop()


def main(argv: list[str] | None = None) -> None:
    import argparse
    import backend

    parser = argparse.ArgumentParser(description="Run metrics WebSocket server")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8777")))
    parser.add_argument("--version", action="store_true", help="Print backend version and exit")
    args = parser.parse_args(argv)
    if args.version:
        print(backend.__version__)
        return
    asyncio.run(run_server(args.host, args.port))


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
