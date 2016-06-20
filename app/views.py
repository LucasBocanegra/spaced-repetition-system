from django.shortcuts import render


def deck_list(request):
    return render(request, 'app/deck_list.html', {})
