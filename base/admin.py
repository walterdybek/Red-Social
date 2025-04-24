from django.contrib import admin

# Register your models here.
from .models import Topic, Room, Message, Post ,User
admin.site.register(User)  # Register the custom user model
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Post)