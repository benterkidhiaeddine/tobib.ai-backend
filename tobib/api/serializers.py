from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.validators import EmailValidator
from api.models import ChatBotRoom, ChatBotRoomMessage

from django.contrib.auth import get_user_model, authenticate

# User serializers

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "username", "password")

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(
            email=clean_data["email"], password=clean_data["password"]
        )
        user_obj.username = clean_data["username"]
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "password")

        # No validation for email if already exists when login
        extra_kwargs = {
            "email": {"validators": []},
        }

    ##
    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data["email"], password=clean_data["password"]
        )
        if not user:
            raise ValidationError("user not found")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("email", "username")


# Create BotChatRoomMessage Serializer
class ChatBotRoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotRoomMessage
        fields = "__all__"


# Create BotChatRoom Serializer
class ChatBotRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotRoom
        fields = "__all__"


class CreateChatBotRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBotRoom
        fields = ("title", "ct_scan_url", "blood_work_url", "x_ray_url")
