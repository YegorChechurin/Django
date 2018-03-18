from django.db import models
from django.db.models import Q
import datetime

class Chats(models.Model):
    chat_id = models.AutoField(primary_key=True)
    chat_key = models.IntegerField()
    participant1_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='participant1_id')
    participant2_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='participant2_id')
    participant1_name = models.CharField(max_length=500)
    participant2_name = models.CharField(max_length=500)
    last_mes_auth_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='last_mes_auth_id')
    last_mes_auth_name = models.CharField(max_length=500)
    last_mes_text = models.CharField(max_length=5000)
    last_mes_ts = models.DateTimeField(auto_now=True) #auto_now_add=True

    @staticmethod
    def createChat(mes_info):
    	sender_id = mes_info['sender_id']
    	sender_name = mes_info['sender_name']
    	recipient_id = mes_info['recipient_id']
    	recipient_name = mes_info['recipient_name']
    	message = mes_info['message']
    	key = sender_id + recipient_id
    	chat = Chats(chat_key=key,participant1_id_id=sender_id,participant2_id_id=recipient_id,participant1_name=sender_name,participant2_name=recipient_name,last_mes_auth_id_id=sender_id,last_mes_auth_name=sender_name,last_mes_text=message)
    	chat.save()

    @staticmethod
    def updateChat(mes_info):
    	sender_id = mes_info['sender_id']
    	sender_name = mes_info['sender_name']
    	recipient_id = mes_info['recipient_id']
    	message = mes_info['message']
    	chat = Chats.objects.get(Q(participant1_id_id=sender_id,participant2_id_id=recipient_id) | Q(participant2_id_id=sender_id,participant1_id_id=recipient_id))
    	chat.last_mes_auth_id_id = sender_id
    	chat.last_mes_auth_name = sender_name
    	chat.last_mes_text = message
    	#chat.last_mes_ts = datetime.datetime.now()
    	chat.save()

    @staticmethod
    def fetchMessages(id_1,id_2):
    	chat_raw = Messages.objects.filter(Q(recipient_id_id=id_1,sender_id_id=id_2) | Q(recipient_id_id=id_2,sender_id_id=id_1)).order_by('message_id')
    	chat = []
    	for c in chat_raw:
    		message = {'sender_id':0, 'recipient_id':0, 'sender_name':0, 'message':0}
    		message['sender_id'] = c.sender_id_id
    		message['recipient_id'] = c.recipient_id_id 
    		message['sender_name'] = c.sender_name
    		message['message'] = c.message
    		chat.append(message)
    	return chat


class Friends(models.Model):
    friendship_id = models.AutoField(primary_key=True)
    fr1_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='fr1_id')
    fr2_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='fr2_id')


class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    recipient_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='recipient_id')
    recipient_name = models.CharField(max_length=500)
    sender_id = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='sender_id')
    sender_name = models.CharField(max_length=500)
    message = models.CharField(max_length=5000)
    ts = models.DateField()

    @staticmethod
    def postMessage(mes_info):
    	if not mes_info:
    		return
    	sender_id = mes_info['sender_id']
    	sender_name = mes_info['sender_name']
    	recipient_id = mes_info['recipient_id']
    	recipient_name = mes_info['recipient_name']
    	message = mes_info['message']
    	mes = Messages(sender_id_id=sender_id,sender_name=sender_name,recipient_id_id=recipient_id,recipient_name=recipient_name,message=message)
    	mes.save()
    	chat = Chats.objects.filter(Q(participant1_id_id=sender_id,participant2_id_id=recipient_id) | Q(participant2_id_id=sender_id,participant1_id_id=recipient_id))
    	if chat:
    		Chats.updateChat(mes_info)
    	else:
        	Chats.createChat(mes_info)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    email = models.CharField(max_length=500)

    def __str__(self):
        return 'id %s %s' % (self.user_id, self.username)

    def getOtherMembers(self):
    	members = Users.objects.all().exclude(pk=self.user_id)
    	return members

    def get_fr_IDs(self):
    	fr_IDs = []
    	result = Friends.objects.filter(Q(fr1_id=self.user_id) | Q(fr2_id=self.user_id))
    	for every in result:
            if every.fr1_id_id == self.user_id:
            	fr_IDs.append(every.fr2_id_id)
            else:
            	fr_IDs.append(every.fr1_id_id)
    	return fr_IDs

    def get_fr_info(self):
    	fr_info = []
    	result = Friends.objects.filter(Q(fr1_id=self.user_id) | Q(fr2_id=self.user_id))
    	if result:
    	    for every in result:
                if every.fr1_id_id == self.user_id:
            	    info = {'id':every.fr2_id.user_id, 'name':every.fr2_id.username}
            	    fr_info.append(info)
                else:
            	    info = {'id':every.fr1_id.user_id, 'name':every.fr1_id.username}
            	    fr_info.append(info)
    	return fr_info

    def get_last_friendship_id(self):
    	result = Friends.objects.filter(Q(fr1_id=self.user_id) | Q(fr2_id=self.user_id))
    	if result:
    		n = len(result)
    		last_id = result[n-1].friendship_id
    		return last_id
    	else:
    		return 0

    def addFriend(self,fr_id):
    	fr_IDs = self.get_fr_IDs()
    	fr_id = int(fr_id)
    	if not fr_id in fr_IDs:
    		friendship = Friends(fr1_id_id=self.user_id,fr2_id_id=fr_id)
    		friendship.save()

    def removeFriend(self,fr_id):
    	fr_IDs = self.get_fr_IDs()
    	fr_id = int(fr_id)
    	if fr_id in fr_IDs:
    		friendship = Friends.objects.get(Q(fr1_id=self.user_id,fr2_id=fr_id) | Q(fr2_id=self.user_id,fr1_id=fr_id))
    		friendship.delete()

    def fetch_chats(self):
    	chats_raw = Chats.objects.filter(Q(participant1_id=self.user_id) | Q(participant2_id=self.user_id)).order_by('-last_mes_ts')
    	if chats_raw:
    		chats = []
    		for c in chats_raw:
    			chat = {'partner_id':0, 'partner_name':0, 'last_mes_auth_id':0, 'last_mes_auth_name':0, 'last_mes_text':0, 'last_mes_ts':0}
    			chat['partner_id'] = c.chat_key - self.user_id
    			if c.participant1_id_id == self.user_id:
    				chat['partner_name'] = c.participant2_name
    			else:
    				chat['partner_name'] = c.participant1_name
    			chat['last_mes_auth_id'] = c.last_mes_auth_id_id
    			chat['last_mes_auth_name'] = c.last_mes_auth_name
    			chat['last_mes_text'] = c.last_mes_text
    			chat['last_mes_ts'] = c.last_mes_ts
    			chats.append(chat)
    		return chats

    def get_last_rec_mes_id(self):
    	result = Messages.objects.filter(recipient_id=self.user_id)
    	if result:
    		n = len(result)
    		last_id = result[n-1].message_id
    		return last_id
    	else:
    		return 0

    def fetch_received_messages(self,mes_id):
    	messages_raw = Messages.objects.filter(Q(recipient_id=self.user_id) & Q(message_id__gt=mes_id)).order_by('message_id')
    	if messages_raw:
    		messages = []
    		for m in messages_raw:
    			message = {'message_id':m.message_id, 'sender_id':m.sender_id_id, 'recipient_id':m.recipient_id_id, 'sender_name':m.sender_name, 'message':m.message}
    			messages.append(message)
    		return messages


    	
    	# cd C:\Python\Social_Nano_Network

    	# python manage.py shell

    	# from snn.models import Users,Friends

    	# u = Users.objects.get(pk=1)

    	# u.removeFriend(5)




    

    