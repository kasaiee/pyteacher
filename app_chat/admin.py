from django.contrib import admin
from app_chat.models import Chat, ChatGroup, Ticket


admin.site.register(Chat)
admin.site.register(ChatGroup)
admin.site.register(Ticket)
