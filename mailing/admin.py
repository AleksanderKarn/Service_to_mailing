from django.contrib import admin

from mailing.models import Message, Mailing
from users.models import User

admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(User)
