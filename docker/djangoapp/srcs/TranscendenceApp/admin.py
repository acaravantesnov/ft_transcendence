'''
Defines how the admin interface for this app is going to look like.
'''

from django.contrib import admin
from .models import *

admin.site.register(MyCustomUser)
admin.site.register(Game)