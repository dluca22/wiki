from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from http.client import HTTPResponse
from markdown2 import Markdown
from random import choice
from django.core.files.storage import default_storage


from . import util

# Django From class
class SubmitForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50, min_length=1)
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Text body in markdown', 'id':'text_form'}), label='Text', min_length=10, max_length=500, required=True)

# class for edit form
class EditForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':15, 'placeholder':'Text body in markdown', 'id':'text_form'}), label='Edit:', min_length=10, max_length=500, required=True)



# ====================================================
def index(request):
    entries= util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": sorted(entries, key=str.casefold)
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

def search(request):
    # get the query name='q'
    query = request.GET['q']
    articles = util.list_entries()
    # for every element in articles list, if the query is in the element, add it to new list of matching names
    matches = [x for x in articles if query.lower() in x.lower()]

    # if it is exact match go directly
    if query in articles:
        # should have been
        # return HttpResponseRedirect(reverse('query')) O QUALCOSA DEL GENERE   
        return HttpResponseRedirect(f'{query}')

    # else go to result passing the list of matching names
    else:
        return render(request, "encyclopedia/search_result.html", {'matches':matches, 'query': query})


# ====================================================

# view for create form
def create(request):
    # when the form is submitted
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
                return render(request, "encyclopedia/create.html", {'error': "conflict", 'title': article[0], 'query':title })

            # if no article found, save it to file with util func and redirect to page
            else:
                util.save_entry(title=title, content=content)
            return HttpResponseRedirect(f"{title}")

    # if get request displays submit form
    return render(request, "encyclopedia/create.html", {'form':SubmitForm()})

# ====================================================

def editpage(request, title):
    # if form is submitted via POST request
    if request.method == "POST":
        # save logic
        form = EditForm(request.POST)
        if form.is_valid():
            content= form.cleaned_data['text']
            # save entry with same title and updated content
            util.save_entry(title=title, content=content)

            # return getpage(request, title)
            return HttpResponseRedirect(f'/wiki/{title}')

    # if get request


    # if user forces url to edit non existing, edit page shows error and ask to create page for it
    article_list = util.list_entries()
    saved = [x for x in article_list if title.lower() == x.lower()]
    if title not in saved:

        return render(request, "encyclopedia/edit.html", {'error': "missing", 'thing': title })

    # if entry is present, show form with initial value= text of the file
    article = util.get_entry(title)

    form = EditForm(initial={'text':article})

    return render(request, "encyclopedia/edit.html", {'form':form, 'article':title})
# ====================================================

def random(request):
    # choose from the list of entries
    random = choice(util.list_entries())

    # simplest way to just use responseredirect and paste the title
    return HttpResponseRedirect(f'{random}')

# ====================================================