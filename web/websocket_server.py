from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from web.state import get_state

router = APIRouter()

connected_clients: list[WebSocket] = []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    # Al conectar, mandamos el estado actual inmediatamente
    await websocket.send_json(get_state())

    try:
        while True:
            # Mantiene la conexión viva; no esperamos mensajes del cliente por ahora
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def broadcast(state: dict):
    """Sends the given state to every connected WebSocket client."""
    disconnected = []
    for client in connected_clients:
        try:
            await client.send_json(state)
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        connected_clients.remove(client)