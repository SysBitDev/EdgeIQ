import asyncio
from typing import Any, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/api/v1", tags=["ws"])

_connections: Set[WebSocket] = set()
_lock = asyncio.Lock()


@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    async with _lock:
        _connections.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        async with _lock:
            _connections.discard(ws)


async def broadcast_event(payload: Any):
    dead = []
    async with _lock:
        for c in list(_connections):
            try:
                await c.send_json(payload)
            except Exception:
                dead.append(c)
        for d in dead:
            _connections.discard(d)
