from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from http.client import HTTPResponse
from markdown2 import Markdown
from random import choice
from django.core.files.storage import default_storage


from . import util

# Django From class
class SubmitForm (forms.Form):
    # title = forms.CharField(label="Title")
    title = forms.CharField(label='Title', max_length=50, min_length=1)
    ## TODO change min length to 10+
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Text body'}), label='Text', min_length=1, max_length=500, required=True,)
    # text =  forms.CharField(widget=forms.TextInput(attrs={'text':'text'}))


# ====================================================
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# ====================================================

# view for article request
def getpage(request, title):
    # call util function returning <name> or None:
    article = util.get_entry(title)
    # if None > error page
    if article is None:
        return render(request, "encyclopedia/not_existing.html", {'title': title })

    # if exists, convert and display
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/article.html", {'article': markdowner.convert(article), 'title': title})

# ====================================================
# every article has delete button
def deletepage(request, title):
    # copy util.py but only delete object then redirect to index page with updated list
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

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

        # Django get the form data from post request
        form = SubmitForm(request.POST)

        #Django form validation
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['text']

            # get list and find if the title EQUALS one in the list (while compared lowercase)
            article_list = util.list_entries()
            article = [x for x in article_list if title.lower() == x.lower()]

            # if there's an article, display error page with the link to it
            # create.html handles what to display based on error "conflict" being passed
            if article:
                return render(request, "encyclopedia/create.html", {'error': "conflict", 'title': article[0] })

            # if no article found, save it to file with util func and redirect to page
            else:
                util.save_entry(title=title, content=content)
                return HttpResponseRedirect(f"{title}")

    # get request displays submit form
    return render(request, "encyclopedia/create.html", {'form':SubmitForm()})

# ====================================================
def editpage(request, title):

    if request.method == "POST":
        # save logic
        return HttpResponseRedirect(f"{title}")

    article = util.get_entry(title)

    article_body = SubmitForm({'body': article})

    return render(request, "encyclopedia/edit.html", {'form':SubmitForm(), 'thing':title, 'body': article_body})
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