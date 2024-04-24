from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def follower_count(self):
        return Relationship.objects.filter(following=self).count()
    
    def following_count(self):
        return Relationship.objects.filter(follower=self).count()
    
    def follow(self, user):
        Relationship.objects.get_or_create(follower=self, following=user)

    def unfollow(self, user):
        Relationship.objects.filter(follower=self, following=user).delete()

    def is_following(self, user):
        return Relationship.objects.filter(follower=self, following=user).exists()

class Relationship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return Like.objects.filter(post=self).count()
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)