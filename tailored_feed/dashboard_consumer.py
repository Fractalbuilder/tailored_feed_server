from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f"session_{self.session_id}_db"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


    async def update_connected(self, event):
        await self.send(text_data=json.dumps({
            "type": "update_connected",
            "session_id": event["session_id"],
            "assistants_connected": event["assistants_connected"],
        }))
    

    async def update_completeness(self, event):
        await self.send(text_data=json.dumps({
            "type": "update_completeness",
            "session_id": event["session_id"],
            "assistants_in_process": event["assistants_in_process"],
            "assistants_finished": event["assistants_finished"],
        }))
