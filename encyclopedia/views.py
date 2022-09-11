from http.client import HTTPResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    article = util.get_entry(entry)
    # convertire a html
    return render(request, "encyclopedia/article.html", {'article': article})

def create(request):
    return render(request, "encyclopedia/create.html")

def random(request):
    random = choice(util.list_entries())
    article = util.get_entry(random)
    return redirect(request, "encyclopedia/article.html", {'article': article})
