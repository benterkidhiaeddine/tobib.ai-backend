from django.db import models


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model


class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = AppUserManager()

    def __str__(self):
        return self.username


# Buisiness logic models here

UserModel = get_user_model()


class ChatBotRoom(models.Model):
    title = models.TextField(blank=False, null=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    ct_scan_url = models.URLField(blank=True, null=True)
    blood_work_url = models.URLField(blank=True, null=True)
    x_ray_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    number_of_messages = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"ChatRoom - {self.title} {self.user.username}"

    def update_number_of_messages(self):
        self.number_of_messages += 1
        self.save()

    def deactivate_chat_room(self):
        self.is_active = False
        self.save()


class ChatBotRoomMessage(models.Model):
    chat_room = models.ForeignKey(ChatBotRoom, on_delete=models.CASCADE)
    answer_number = models.IntegerField(default=0)
    text_content = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f'{self.timestamp} - {"Bot" if self.is_bot else "Human"}: {self.text_content}'
