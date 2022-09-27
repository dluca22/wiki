from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from http.client import HTTPResponse
from markdown2 import Markdown
from random import choice

from . import util


class SubmitForm (forms.Form):
    # title = forms.CharField(label="Title")
    title = forms.CharField(label='Title', max_length=50, min_length=1)

    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Text body'}), label='Text', min_length=10, max_length=500, required=True,)
    # text =  forms.CharField(widget=forms.TextInput(attrs={'text':'text'}))

# ====================================================

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# ====================================================

# view for article request
def getpage(request, title):
    # call util functio returning <name> or None:
    article = util.get_entry(title)
    # if None > error page
    if article is None:
        return render(request, "encyclopedia/not_existing.html", {'title': title })

    # if exists, convert and display
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/article.html", {'article': markdowner.convert(article), 'title': title})

# ====================================================
# no need to use Django Forms Classes
def search(request):

    query = request.GET['q']
    articles = util.list_entries()
    # for every element in articles list, if the query is in the element, add it to list of matches
    matches = [x for x in articles if query.lower() in x.lower()]

    # if it is exact match
    if query in articles:
        return HttpResponseRedirect(f'{query}')

    # else go to result passing the list of matches
    else:
        return render(request, "encyclopedia/search_result.html", {'matches':matches, 'query': query})


# ====================================================

"""Ho aggiunto la form e la mostra in create, ho aggiunto il placeholder per il text body ma non sono riuscito a togliere i <label>

completare la struttura della form poi aggiungere la logica per 'POST'
"""

# view for create form
def create(request):

    if request.method == "POST":
        form = SubmitForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']

            return HttpResponseRedirect(f'{title} and {text}')

    else:
        return render(request, "encyclopedia/create.html", {'form':SubmitForm()})

# ====================================================

def random(request):
    random = choice(util.list_entries())
    # OLD  random_article = util.get_entry(random)

    # simplest way to just use responseredirect and paste the title
    return HttpResponseRedirect(f'{random}')


    # CANT MAKE IT WORK return HttpResponseRedirect(reverse('getentry', kwargs = {'title': random_article}))
    # NO return render(request, "encyclopedia/article.html", {'article': article})

    # NO return redirect(request, f"encyclopedia/{article}.html", {'article': article})

# ====================================================