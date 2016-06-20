from django.db import models
from django.utils import timezone


class Deck(models.Model):
    owner = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    limit_view_cards = models.IntegerField(default=10)

    def __str__(self):
        return self.title


class Card(models.Model):
    phrase = models.CharField(max_length=800)
    translation = models.CharField(max_length=800)
    level = models.IntegerField(default=0)
    view_date = models.DateTimeField(default=timezone.now)
    deck = models.ForeignKey('Deck', on_delete=models.CASCADE)

    def __str__(self):
        return self.phrase


