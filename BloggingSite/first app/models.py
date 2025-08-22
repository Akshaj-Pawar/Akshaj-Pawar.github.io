from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Posts(models.Model):

    def total_likes(self):
        return self.likes.count()

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1500)
    image = models.CharField(max_length=2083)
    link = models.CharField(max_length=2083)
    views = models.IntegerField()
    likes = models.ManyToManyField(User, related_name='blog_post')
    file = models.FilePathField(path='/Users/ravinderkumar/PycharmProjects/DesignSite/firstapp/word_files') #i need to save the file in the directory #/Users/ravinderkumar/PycharmProjects/DesignSite/firstapp/word_files


class Comment(models.Model):
    Posts = models.ForeignKey(Posts, related_name='Comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=225)
    comment_text = models.TextField()