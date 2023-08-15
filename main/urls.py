from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name = 'dashboard'),
    path('booksearch', views.books, name = 'book'),
    path('allocate', views.allocate, name='allocate'),
    path('addnewmember', views.add_new_member, name = 'add_new_member'),
    path('existingmembers', views.existing_members, name = 'existing_members'),
    path('returnbook', views.return_book, name = 'return' ),
    path('allocate2', views.allocate2, name = 'allocate2')
]