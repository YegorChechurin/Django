from django.urls import path, re_path

from . import views

app_name = 'snn'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/profile_page', views.profile_page, name='profile_page'),
    path('<int:user_id>/',views.add_remove_friends, name='add_remove_friends'),
    path('<int:user_id>/chat_room',views.chat_room, name='chat_room'),
    re_path(r'^catch_friends/$',views.catch_friends, name='catch_friends'),
    re_path(r'^chats_giver/$',views.chats_giver, name='chats_giver'),
    re_path(r'^chat_fetcher/$',views.chat_fetcher, name='chat_fetcher'),
    re_path(r'^message_sender/$',views.message_sender, name='message_sender'),
    re_path(r'^messages_giver/$',views.messages_giver, name='messages_giver'),
]
