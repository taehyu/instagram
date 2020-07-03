from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        pass

    def create_superuser(self, email, username, password):

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=60, blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to=image_file_path, default='default.png')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    is_active = models.BooleanField(Default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_posts')
    photo = models.ImageField(upload_to=image_file_path, blank=False)
    text = models.TextField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="likers")

    def __str__(self):
        return f'{self.author}\'s post'


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    text = models.CharField(max_length=300)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}\'s comment'

