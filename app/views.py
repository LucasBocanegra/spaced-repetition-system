from django.shortcuts import render
from django.utils import timezone
from .models import Deck, Card
from .forms import DeckForm
from .forms import CardForm
from .forms import UserForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



def index(request):
    return render(request, 'app/index.html', {})


def my_decks(request):
    if request.user.is_authenticated():
        decks = Deck.objects.filter(owner=request.user)
        return render(request, 'app/my_decks.html', {'decks': decks})


def user_new(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return my_decks(request)
    else:
        form = UserForm()
    return render(request, 'app/user_new.html', {'form': form,})


def deck_new(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.owner = request.user
            deck.created_date = timezone.now()
            deck.save()
            return my_decks(request)
    else:
        form = DeckForm()
    return render(request, 'app/deck_new.html', {'form': form, })


def deck_add_card(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.view_date = timezone.now()
            card.save()
            return deck_detail(request, deck.pk)
    else:
        form = CardForm()
    return render(request, 'app/card_new.html', {'form': form})

def deck_edit(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if request.method == "POST":
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.owner = request.user
            deck.created_date = timezone.now()
            deck.save()
            return deck_detail(request,deck.pk)
    else:
        form = DeckForm(instance=deck)
    return render(request, 'app/deck_edit.html', {'form': form})


def deck_detail(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    cards = Card.objects.filter(deck=pk)

    return render(request, 'app/deck_detail.html', {'cards': cards, 'deck': deck})


def deck_delete(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if request.method == "POST":
        form = DeckForm(request.POST, instance=deck)
        # if form.is_valid():
        #     deck = form.save(commit=False)
        #     deck.owner = request.user
        #     deck.created_date = timezone.now()
        #     deck.save()mtnecks
        #     return deck_detail(request, deck.pk)
    else:
        deck.delete()
        decks = Deck.objects.all()
        return render(request, 'app/my_decks.html', {'decks': decks})


def init_review(request, pk):
    if request.user.is_authenticated():
        cards = Card.objects.filter(deck=pk)

        return render(request, 'app/init_review.html', {'cards': cards})

