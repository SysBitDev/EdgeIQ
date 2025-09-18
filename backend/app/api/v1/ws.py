from fastapi import APIRouter, WebSocket, WebSocketDisconnect
router = APIRouter(tags=["ws"])
clients: set[WebSocket] = set()

@router.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()  # noop ping
    except WebSocketDisconnect:
        clients.discard(ws)

async def broadcast(event: dict):
    dead=[]
    for c in list(clients):
        try: await c.send_json(event)
        except: dead.append(c)
    for d in dead: clients.discard(d)
