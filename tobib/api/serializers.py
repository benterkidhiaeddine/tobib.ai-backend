from django.core.exceptions import ValidationError
from rest_framework import serializers
from api.models import *

from django.contrib.auth import get_user_model, authenticate
#User serializers

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username')



#Create BotChatRoom Serializer
class ChatBotRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotRoom
        fields = '__all__'

    def create(self, validated_data):
        # Override the create method to handle the creation of ChatBotRoom instances
        return ChatBotRoom.objects.create(**validated_data)


    
    
#Create BotChatRoomMessage Serializer
class ChatBotRoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ChatBotRoomMessage
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return ChatBotRoomMessage.objects.create(**validated_data)


