from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  pass

class Subreddit(models.Model):
  name = models.CharField(max_length=32)
  logo = models.CharField(max_length=1000, blank=True, null=True)

  #ADD "subbed followers" - with a many to many field, you can view all of the users who are following

class Post(models.Model):
  #if someone deletes their account, the post should remain unless user deleted it
  poster = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_posts', blank=True, null=True)
  #optional
  image_url = models.CharField(max_length=1000, blank=True, null=True)
  #optional
  content = models.CharField(max_length=1000, blank=True, null=True)
  upvotes = models.IntegerField()
  subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE, related_name='sub_posts')
  title = models.CharField(max_length=100)

  #ADD date posted

class Comment(models.Model):
  #if someone deletes their account, comment should just say 'deleted' for username

  #add a "date posted"
  poster = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_comments', blank=True, null=True)
  content = models.CharField(max_length=1000)
  upvotes = models.IntegerField()
  root = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='child_comment', blank=True, null=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')


