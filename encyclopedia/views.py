from audioop import reverse
from http.client import HTTPResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from random import choice
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    article = util.get_entry(title)
    if article is None:
        return render(request, "encyclopedia/notExisting.html", {'article': title})

    # convertire a html
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/article.html", {'article': markdowner.convert(article), 'title': title})

def create(request):
    var = "culo"
    return render(request, "encyclopedia/create.html", {'var': var})

def random(request):
    random = choice(util.list_entries())
    random_article = util.get_entry(random)
    return HttpResponseRedirect(reverse('title', kwargs = {'title': random_article}))

    # NO return render(request, "encyclopedia/article.html", {'article': article})

    # NO return redirect(request, f"encyclopedia/{article}.html", {'article': article})
