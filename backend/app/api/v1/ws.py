import logging
from typing import Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["ws"])
log = logging.getLogger("ws")

clients: Set[WebSocket] = set()


@router.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.discard(ws)


async def broadcast(event: dict):
    dead = []
    for c in list(clients):
        try:
            await c.send_json(event)
        except Exception as exc:
            log.debug("Broadcast to client failed: %r", exc)
            dead.append(c)
    for d in dead:
        clients.discard(d)
