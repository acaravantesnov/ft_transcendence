import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TranscendenceProject.settings')
django.setup()

from django.contrib.auth import get_user_model

MyCustomUser = get_user_model()

MyCustomUser.objects.create_user(
    username=os.environ.get('AIUSER_USERNAME'),
    first_name=os.environ.get('AIUSER_FIRST_NAME'),
    last_name=os.environ.get('AIUSER_LAST_NAME'),
    email=os.environ.get('AIUSER_EMAIL'),
    avatar=os.environ.get('AIUSER_AVATAR'),
    password=os.environ.get('AIUSER_PASSWORD'),
)

MyCustomUser.objects.create_user(
    username=os.environ.get('MUSER_USERNAME'),
    first_name=os.environ.get('MUSER_FIRST_NAME'),
    last_name=os.environ.get('MUSER_LAST_NAME'),
    email=os.environ.get('MUSER_EMAIL'),
    avatar=os.environ.get('MUSER_AVATAR'),
    password=os.environ.get('MUSER_PASSWORD'),
)

MyCustomUser.objects.create_user(
    username=os.environ.get('DUSER_USERNAME'),
    first_name=os.environ.get('DUSER_FIRST_NAME'),
    last_name=os.environ.get('DUSER_LAST_NAME'),
    email=os.environ.get('DUSER_EMAIL'),
    avatar=os.environ.get('DUSER_AVATAR'),
    password=os.environ.get('DUSER_PASSWORD'),
)

MyCustomUser.objects.create_user(
    username=os.environ.get('AUSER_USERNAME'),
    first_name=os.environ.get('AUSER_FIRST_NAME'),
    last_name=os.environ.get('AUSER_LAST_NAME'),
    email=os.environ.get('AUSER_EMAIL'),
    avatar=os.environ.get('AUSER_AVATAR'),
    password=os.environ.get('AUSER_PASSWORD'),
)

MyCustomUser.objects.create_user(
    username=os.environ.get('ALUSER_USERNAME'),
    first_name=os.environ.get('ALUSER_FIRST_NAME'),
    last_name=os.environ.get('ALUSER_LAST_NAME'),
    email=os.environ.get('ALUSER_EMAIL'),
    avatar=os.environ.get('ALUSER_AVATAR'),
    password=os.environ.get('ALUSER_PASSWORD'),
)
