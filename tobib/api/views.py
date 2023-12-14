from django.contrib.auth import get_user_model, login, logout
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes

from api.models import ChatBotRoomMessage
from api.serializers import *
from api.validations import *

#import the functions of the ai model
from api.ai_model import first_answer, second_answer ,question3, question4, fifth_answer

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    

#Get a specefic Chat room 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_bot_room_detail(request,chat_bot_room_id):


    
    if request.method == 'GET':
        user = request.user
        try:
            chat_bot_room = ChatBotRoom.objects.get(user=user, pk =chat_bot_room_id)
        except ChatBotRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChatBotRoomSerializer(chat_bot_room)
        return Response(serializer.data)

#Create a new chat room
#LIst all chat rooms for user

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def chat_bot_rooms_list(request):


    user = request.user
    
    if request.method == 'GET':
        try:
            chat_bot_rooms = ChatBotRoom.objects.filter(user=user)
        except ChatBotRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChatBotRoomSerializer(chat_bot_rooms, many=True)
        return Response(serializer.data)

    elif request.method == 'POST': # Get the user from the request (assuming you are using authentication) user = request.user
        # Combine the user with the request data to create the ChatBotRoom
        data_with_user = {**request.data, 'user': user.id}
        serializer = ChatBotRoomSerializer(data=data_with_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    


#Get Messages for a specefic chat room for the current user
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def room_messages_list(request,chat_bot_room_id):


    user = request.user
    try:
            chat_bot_room = ChatBotRoom.objects.get(user=user,pk=chat_bot_room_id)
    except ChatBotRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        messages = ChatBotRoomMessage.objects.filter(chat_room=chat_bot_room)
        serializer = ChatBotRoomMessageSerializer(messages, many = True)
        return Response(serializer.data)


    elif request.method == 'POST': 

        serializer = ChatBotRoomMessageSerializer(data={**request.data,"chat_room":chat_bot_room.id})

        message_content = request.data["text_content"]
        if serializer.is_valid():
            serializer.save()

            #after saving the message to the db start send the message to ai model function
            if chat_bot_room.number_of_messages == 0:
                answer = first_answer(message_content)
                
                answer_message = ChatBotRoomMessage(text_content= answer, is_bot = True, chat_room = chat_bot_room, answer_number = 1)
                answer_message.save()
                chat_bot_room.update_number_of_messages()
                message_serializer = ChatBotRoomMessageSerializer(answer_message)
                return Response(message_serializer.data, status=201)

            elif chat_bot_room.number_of_messages == 1:
                answer = second_answer(message_content) 
                answer_message = ChatBotRoomMessage(text_content= answer, is_bot = True, chat_room = chat_bot_room,answer_number = 2)
                answer_message.save()
                chat_bot_room.update_number_of_messages()
                message_serializer = ChatBotRoomMessageSerializer(answer_message)
                return Response(message_serializer.data, status=201)


            elif chat_bot_room.number_of_messages == 2:
                answer = question3
                answer_message = ChatBotRoomMessage(text_content= answer, is_bot = True, chat_room = chat_bot_room,answer_number = 3)
                answer_message.save()
                chat_bot_room.update_number_of_messages()
                message_serializer = ChatBotRoomMessageSerializer(answer_message)
                return Response(message_serializer.data, status=201)


            elif chat_bot_room.number_of_messages == 3:
                answer = question4
                answer_message = ChatBotRoomMessage(text_content= answer, is_bot = True, chat_room = chat_bot_room, answer_number = 4)
                answer_message.save()
                chat_bot_room.update_number_of_messages()
                message_serializer = ChatBotRoomMessageSerializer(answer_message)
                return Response(message_serializer.data, status=201)


            elif chat_bot_room.number_of_messages == 4:
                answer1 = ChatBotRoomMessage.objects.filter(answer_number = 1)
                answer2 = ChatBotRoomMessage.objects.filter(answer_number = 2)
                answer4 = ChatBotRoomMessage.objects.filter(answer_number = 4)

                answer = fifth_answer(message_content, answer1, answer2, answer4)
                answer_message = ChatBotRoomMessage(text_content= answer, is_bot = True, chat_room = chat_bot_room, answer_number = 5)
                chat_bot_room.is_active = False
                chat_bot_room.save()
                
                answer_message.save()
                
                chat_bot_room.update_number_of_messages()
                message_serializer = ChatBotRoomMessageSerializer(answer_message)
                return Response(message_serializer.data, status=201)
                  



        return Response(serializer.errors, status=400)