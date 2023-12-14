import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tobib.settings')  # Replace 'your_project.settings' with your actual project settings module
django.setup()

from django.contrib.auth import get_user_model
from api.models import ChatBotRoom, ChatBotRoomMessage
from api.serializers import UserRegisterSerializer, ChatBotRoomSerializer, ChatBotRoomMessageSerializer

UserModel = get_user_model()

def create_users():
    users = []
    for i in range(1, 3):
        user_data = {
            'email': f'user{i}@example.com',
            'username': f'user{i}',
            'password': 'password123'
        }
        serializer = UserRegisterSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        users.append(user)
    return users

def create_chat_rooms(users):
    chat_rooms = []
    for user in users:
        chat_room_data = {
            'title': f'Chat Room for {user.username}',
            'user': user.id,
            'ct_scan_url': 'https://example.com/ct_scan',
            'blood_work_url': 'https://example.com/blood_work',
            'x_ray_url': 'https://example.com/x_ray',
            'is_active': True,
            'number_of_messages': 0,
        }
        serializer = ChatBotRoomSerializer(data=chat_room_data)
        serializer.is_valid(raise_exception=True)
        chat_room = serializer.save()
        chat_rooms.append(chat_room)
    return chat_rooms

def create_chat_messages(chat_room):
    messages = []
    for i in range(1, 6):
        message_data = {
            'chat_room': chat_room.id,
            'text_content': f'Message {i} in {chat_room.title}',
            'is_bot': False,
        }
        serializer = ChatBotRoomMessageSerializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        messages.append(message)
    return messages

if __name__ == '__main__':
    users = create_users()
    chat_rooms = create_chat_rooms(users)

    for chat_room in chat_rooms:
        create_chat_messages(chat_room)

    print('Data creation completed.')
