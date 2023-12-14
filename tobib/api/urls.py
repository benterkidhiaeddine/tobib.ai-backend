from django.urls import path, include,re_path
from rest_framework import permissions
from api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),

   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('chat_bot_rooms', views.chat_bot_rooms_list),
    path('chat_bot_rooms/<int:chat_bot_room_id>', views.chat_bot_room_detail),
    path('chat_bot_rooms/<int:chat_bot_room_id>/chat_bot_messages', views.room_messages_list),
    #Authentification paths
    path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),

    #Swagger routes
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
    


]