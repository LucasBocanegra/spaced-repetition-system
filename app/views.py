from django.shortcuts import render
from django.utils import timezone
from .models import Deck

def deck_list(request):
    return render(request, 'app/deck_list.html', {})

def my_decks(request):
    decks = Deck.objects.all()
    return render(request, 'app/my_decks.html', {'decks': decks})


