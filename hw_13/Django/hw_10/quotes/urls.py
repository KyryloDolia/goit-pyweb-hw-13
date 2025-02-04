from django.urls import path

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='root'),
    path('<int:page>', views.main, name='root_paginate'),
    path('author/<str:fullname>/', views.author_bio, name='author'),
    path('new/', views.create_quote, name='new'),
    path('quote/delete/<int:quote_id>/', views.delete_quote, name='delete_quote'),
]
