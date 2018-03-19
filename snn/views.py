from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.template import loader
import json
from django.utils.safestring import mark_safe
from django.db.models import Q
from .models import Users, Friends, Messages, Chats

def index(request):
    pass

def profile_page(request,user_id):
	user = Users.objects.get(pk=user_id)
	username = user.username
	members = user.getOtherMembers()
	fr_IDs = user.get_fr_IDs()
	fr_info = user.get_fr_info()
	last_friendship_id = user.get_last_friendship_id()
	context = {'user_id':user_id, 'username':username, 'members':members, 'fr_IDs':fr_IDs, 'fr_info':fr_info, 'last_friendship_id':last_friendship_id}
	template = loader.get_template('snn/profile_page.html')
	return HttpResponse(template.render(context, request))

def add_remove_friends(request,user_id):
	user = Users.objects.get(pk=user_id)
	if request.POST['action']=='add':
	 	user.addFriend(request.POST['member_id'])
	elif request.POST['action']=='remove':
		user.removeFriend(request.POST['member_id'])
	return HttpResponseRedirect(reverse('snn:profile_page', args=(user_id,)))

def catch_friends(request):
	user_id = int(request.GET.get('user_id'))
	user = Users.objects.get(pk=user_id)
	last_friendship_id_js = int(request.GET.get('id')) 
	last_friendship_id = user.get_last_friendship_id()
	if last_friendship_id != last_friendship_id_js:
		return HttpResponse(last_friendship_id)
	
def chat_room(request,user_id):
	partner_id = request.POST['fr_id']
	partner_name = request.POST['fr_name'] 
	user = Users.objects.get(pk=user_id)
	user_id = user.user_id
	username = user.username
	chats_raw = user.fetch_chats()
	chats = mark_safe(json.dumps(chats_raw, default=str))  
	last_rec_mes_id = user.get_last_rec_mes_id()
	context = {'partner_id':partner_id, 'partner_name':partner_name, 'user_id':user_id, 'username':username, 'chats':chats, 'last_rec_mes_id':last_rec_mes_id}
	template = loader.get_template('snn/chat_room.html')
	return HttpResponse(template.render(context, request))

def chats_giver(request):
	user_id = int(request.GET.get('user_id'))
	user = Users.objects.get(pk=user_id)
	chats_raw = user.fetch_chats()
	chats = mark_safe(json.dumps(chats_raw, default=str))
	return HttpResponse(chats)

def chat_fetcher(request):
	user_id = int(request.GET.get('user_id'))
	partner_id = int(request.GET.get('partner_id'))
	chat_raw = Chats.fetchMessages(user_id,partner_id) 
	chat = mark_safe(json.dumps(chat_raw, default=str))
	return HttpResponse(chat)

def message_sender(request):
	sender_id = int(request.GET.get('user_id'))
	sender_name = request.GET.get('user_name')
	recipient_id = int(request.GET.get('partner_id'))
	recipient = Users.objects.get(pk=recipient_id)
	recipient_name = recipient.username
	message = request.GET.get('message')
	mes_info = {'sender_id':sender_id, 'sender_name':sender_name, 'recipient_id':recipient_id, 'recipient_name':recipient_name, 'message':message}
	Messages.postMessage(mes_info)
	return HttpResponse()

def messages_giver(request):
	user_id = int(request.GET.get('user_id'))
	mes_id = int(request.GET.get('mes_id'))
	user = Users.objects.get(pk=user_id)
	messages_raw = user.fetch_received_messages(mes_id)
	messages = mark_safe(json.dumps(messages_raw, default=str))
	return HttpResponse(messages)

	

