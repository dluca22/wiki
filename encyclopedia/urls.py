from django.urls import path

from . import views

app_name='wiki'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('create', views.create, name='create'),
    # if i use 'random' creates problems
    path('rndm', views.random, name='random'),
    path('<str:title>', views.getpage, name='title'),
    path('delete/<str:title>', views.deletepage, name='delete'),
    path('edit/<str:title>', views.editpage, name='edit'),

]
