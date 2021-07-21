from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    MBTI = (
        ('모름', '모름'),
        ('ISTJ', 'ISTJ'),
        ('ISFJ', 'ISFJ'),
        ('INFJ', 'INFJ'),
        ('INTJ', 'INTJ'),
        ('ISTP', 'ISTP'),
        ('ISFP', 'ISFP'),
        ('INFP', 'INFP'),
        ('INTP', 'INTP'),
        ('ESTP', 'ESTP'),
        ('ESFP', 'ESFP'),
        ('ENFP', 'ENFP'),
        ('ENTP', 'ENTP'),
        ('ESTJ', 'ESTJ'),
        ('ESFJ', 'ESFJ'),
        ('ENFJ', 'ENFJ'),
        ('ENTJ', 'ENTJ'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=25, null=False)
    birthday = models.DateField(null=True)
    mbti = models.CharField(default='', max_length=4, null=False, choices=MBTI)
    number = models.CharField(default='', max_length=15, null=True)
    email = models.CharField(default='', max_length=50, null=True)
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''