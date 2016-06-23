from django.shortcuts import render
from django.utils import timezone
from .models import Deck
from .forms import DeckForm
from django.shortcuts import get_object_or_404


def deck_list(request):
    return render(request, 'app/deck_list.html', {})


def my_decks(request):
    decks = Deck.objects.all()
    return render(request, 'app/my_decks.html', {'decks': decks})


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
    return render(request, 'app/deck_new.html', {'form': form})


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
    return render(request, 'app/deck_detail.html', {'deck': deck})
