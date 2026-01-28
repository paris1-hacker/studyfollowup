from django.contrib import admin
from . import models

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    pass



@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass