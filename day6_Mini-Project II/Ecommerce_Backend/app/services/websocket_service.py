from app.core.websocket_manager import ConnectionManager

class WebSocketService:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def notify_user(self, user_id: int, message: str):
        await self.manager.send_personal(user_id, message)

    async def notify_all(self, message: str):
        await self.manager.broadcast(message)