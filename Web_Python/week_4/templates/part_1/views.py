from django.http import HttpResponse
from django.shortcuts import render

def echo(request):
    context = {
        'get' : request.GET,
        'post' : request.POST,
        'meta': request.META
    }
    return render(request, 'echo.html', context=context)

def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })

def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 5),
        'b': request.GET.get('b', 2)
    })