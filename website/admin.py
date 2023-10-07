from django.contrib import admin
from .models import Images, Feedback, AI_Response
from django.contrib import admin
from .models import User


# Register your models here.

admin.site.register(User)

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Feedback)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')


@admin.register(AI_Response)
class AI_ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'value', 'result', 'userId')
