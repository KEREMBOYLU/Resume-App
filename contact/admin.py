from django.contrib import admin
from contact.models import *

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message', 'updated_date', 'created_date']
    search_fields = ['name', 'email', 'subject', 'message']

    class Meta:
        model = Message


@admin.register(ContactAreaInfo)
class ContactAreaInfoAdmin(admin.ModelAdmin):
    list_display = ['id','order', 'title', 'description', 'icon', 'link', 'updated_date', 'created_date']
    search_fields = ['id','order', 'title', 'description', 'icon', 'link',]
    list_editable = ['order', 'title', 'description', 'icon', 'link',]

    class Meta:
        model = ContactAreaInfo