from django.urls import path


from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("search/", views.search, name="search"),
	path("new/", views.new, name="new"),
	path("lucky/", views.lucky, name="lucky"),
	path("wiki/<str:title>/", views.entry, name="entry"),
	path("wiki/<str:title>/edit/", views.edit, name="edit")
]
