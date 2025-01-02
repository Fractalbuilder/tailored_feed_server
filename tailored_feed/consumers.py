from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AssessmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f"session_{self.session_id}"
        
        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        #question_response = data['response']
        question_response = data.get('response', 'No response found')

        print(f"Message received: {question_response}")
        
        # Send the next question or end the assessment
        await self.send(text_data=json.dumps({
            'question': 'Next question or end assessment message here'
        }))
        
    async def send_question(self, event):
        question = event['question']
        
        await self.send(text_data=json.dumps({
            'question': question
        }))
