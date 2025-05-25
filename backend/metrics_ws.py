"""WebSocket server streaming backend metrics."""
from __future__ import annotations

import asyncio
import json
import os

from backend.gateway import METRICS

try:  # optional dependency
    import websockets
    from websockets.server import WebSocketServerProtocol
except Exception:  # pragma: no cover - optional
    websockets = None  # type: ignore
    WebSocketServerProtocol = None  # type: ignore


async def _handler(ws: WebSocketServerProtocol) -> None:
    last = None
    await ws.send(json.dumps(METRICS))
    try:
        while True:
            await asyncio.sleep(1)
            if METRICS != last:
                await ws.send(json.dumps(METRICS))
                last = METRICS.copy()
    except Exception:
        pass


async def run_server(host: str = "0.0.0.0", port: int = 8790) -> None:
    if not websockets:
        raise RuntimeError("websockets package not installed")
    async with websockets.serve(_handler, host, port, path="/metrics"):
        print(f"Metrics WS on ws://{host}:{port}/metrics")
        await asyncio.Future()


def main(argv: list[str] | None = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run Lego GPT metrics WebSocket server")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8790")))
    args = parser.parse_args(argv)
    asyncio.run(run_server(args.host, args.port))


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
