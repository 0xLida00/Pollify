import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Poll

class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.poll_id = self.scope["url_route"]["kwargs"]["poll_id"]
        self.poll_group_name = f"poll_{self.poll_id}"

        # Join poll group
        await self.channel_layer.group_add(
            self.poll_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave poll group
        await self.channel_layer.group_discard(
            self.poll_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # WebSocket does not receive data from frontend, just sends updates
        pass

    async def update_poll(self, event):
        poll_id = event["poll_id"]
        poll = Poll.objects.get(id=poll_id)

        total_votes = poll.votes.count()
        choices_data = [
            {
                "choice_text": choice.choice_text,
                "votes_count": choice.votes_count,
                "percentage": round((choice.votes_count / total_votes) * 100, 2) if total_votes > 0 else 0
            }
            for choice in poll.choices.all()
        ]

        await self.send(text_data=json.dumps({
            "choices": choices_data
        }))