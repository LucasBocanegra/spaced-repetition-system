from django.db.models.expressions import Date
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime,timedelta
from .models import Deck, Card
from .forms import DeckForm
from .forms import CardForm
from .forms import UserForm
from .forms import UserFormLogin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'app/index.html', {})


def my_decks(request):
    if request.user.is_authenticated():
        decks = Deck.objects.filter(owner=request.user)
        return render(request, 'app/my_decks.html', {'decks': decks})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(my_decks)
    else:
        return render(request, 'app/user_login.html')


def user_new(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(user_login)
    else:
        form = UserForm()
    return render(request, 'app/user_new.html', {'form': form, })


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
            return redirect(deck_detail, pk=deck.pk)
    else:
        form = CardForm()
    return render(request, 'app/card_new.html', {'form': form, 'deck':deck})


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
    return render(request, 'app/deck_edit.html', {'form': form, 'deck':deck})


def card_edit(request, pk):
    card = get_object_or_404(Card, pk=pk)
    # deck = get_object_or_404(Deck, pk=pk2)

    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.view_date = timezone.now()
            card.save()
            return redirect(deck_detail, pk=card.deck.pk)
    else:
        form = CardForm(instance=card)
    return render(request, 'app/card_edit.html', {'form': form, 'deck': card.deck})


def deck_detail(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    cards = Card.objects.filter(deck=pk)

    return render(request, 'app/deck_detail.html', {'cards': cards, 'deck': deck})


def deck_delete(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if request.method == "POST":
        form = DeckForm(request.POST, instance=deck)
    else:
        deck.delete()
        return redirect(my_decks)


def init_review(request, pk):
    # if request.user.is_authenticated():
    #     cards = Card.objects.filter(deck=pk)

    deck = get_object_or_404(Deck, pk=pk)
    current_step = int(request.GET['step'])
    limit = int(deck.limit_view_cards)
    if current_step <= deck.limit_view_cards:
        cards = Card.objects.filter(deck=pk).order_by('view_date')

        print('updated date\n')
        print(timezone.get_current_timezone_name())
        print(timezone.get_current_timezone())
        print(timezone.now())
        print(cards)

        if cards.count() < limit:
            if current_step > cards.count():
                return redirect(my_decks)

        return render(request, 'app/init_review.html',
                      {'card': cards[0], 'deck': deck, 'step': current_step,
                       'listSize': deck.limit_view_cards if cards.count() > limit else cards.count})
    else:
        return redirect(my_decks)


def card_update(request, pk):
    answer = request.GET['answer']
    new_step = int(request.GET['step'])+1
    cards = Card.objects.filter(pk=pk)

    if answer == 'hit':
        cards.update(view_date=timezone.localtime(timezone.now()))
    else:
        cards.update(view_date=timezone.localtime(timezone.now()-timedelta(minutes=10)))

    return redirect('/deck/'+str(cards[0].deck_id)+'/cards/init?step='+str(new_step))


def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
    else:
        deck = get_object_or_404(Deck, pk=card.deck.pk)
        card.delete()
        cards = Card.objects.filter(deck=deck)
        return redirect(deck_detail, pk=deck.pk)
