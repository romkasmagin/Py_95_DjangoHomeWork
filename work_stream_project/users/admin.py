from django.contrib import admin
from users.models import Profile, Message, Skill


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email', )


class MessageAdmin(admin.ModelAdmin):
    search_fields = ('subject', )


class SkillsAdmin(admin.ModelAdmin):
    search_fields = ('name', )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Skill, SkillsAdmin)
