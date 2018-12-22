from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
import os


class Profile(models.Model):
    user = models.OneToOneField(User)
    contactInfo = models.CharField(max_length=500, blank = True)
    address = models.CharField(max_length=500, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    profilepic = models.FileField(null=True, upload_to='Profile_Picture', default=os.path.join(settings.MEDIA_ROOT, "default.jpg"))

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Author(models.Model):
    name = models.CharField(max_length=300)
    bio = models.CharField(max_length=5000, blank = True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    author = models.ForeignKey(Author, null=True, blank=True)
    ISBN = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    amount = models.IntegerField(default=1)
    mode = models.CharField(max_length=10)
    locked = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.book.name


class Friend(models.Model):
    user1 = models.ForeignKey(Profile, related_name='Friend1')
    user2 = models.ForeignKey(Profile, related_name='Friend2')
    date = models.DateField(default='2000-01-01')


class TransferLog(models.Model):
    provider = models.ForeignKey(Profile, related_name='Provider')
    receiver = models.ForeignKey(Profile, related_name='Receiver')
    book = models.ForeignKey(Book)
    date = models.DateField(default=timezone.now)


class WallPost(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, default="Untitled")
    text = models.TextField()
    creationDate = models.DateTimeField(default = timezone.now)
    cover = models.FileField(null=True, blank = True, upload_to='Post_Covers')

    def __str__(self):
        return str(self.title) + "-" + str(self.user)


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(WallPost)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user.username) + "-" + str(self.post.title)


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(WallPost)
    time = models.DateTimeField(default=timezone.now)
    text = models.TextField(default = "")

    def __str__(self):
        return str(self.user.username) + "-" + str(self.post.title)


class RequestLog(models.Model):
    donor = models.ForeignKey(Profile, related_name='donor')
    requestor = models.ForeignKey(Profile, related_name='requestor')
    book = models.ForeignKey(Book)

    def __str__(self):
        return str(self.requestor.user.username) + " requests " + str(self.donor.user.username) + " for " + str(self.book.name)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='Sender')
    receiver = models.ForeignKey(User, related_name='Receiver')
    text = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    readflag = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender.username) + " to " + str(self.receiver.username) + ": " + str(self.time)


class ServerMessage(models.Model):
    recipient = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    mode = models.CharField(max_length=10)

    def __str__(self):
        return str(self.recipient.username + " " + self.book.name + "mode: " + self.mode)

