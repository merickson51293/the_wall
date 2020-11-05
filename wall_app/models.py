from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postdata['first_name'])<2:
            errors['first_name']="First name must be longer than 2 characters!"
        if len(postdata['last_name'])<2:
            errors['last_name']="Last name must be longer than 2 characters!"
        if not email_check.match(postdata['email']):
            errors['email']="Email must be valid format!"
        if len(postdata['password'])<8:
            errors['password']="Password must be at least 8 characters!"
        if postdata['password'] != postdata['conf_password']:
            errors['conf_password']="Password and confirm password must match!"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class Message(models.Model):
    message=models.CharField(max_length=255)
    person = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    
class Comment(models.Model):
    comment=models.CharField(max_length=255)
    person = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Message, related_name="post_comments", on_delete=models.CASCADE)
