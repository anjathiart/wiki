from django.urls import path


from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("search/", views.search, name="search"),
	path("new/", views.new, name="new"),
	path("save/", views.save, name="save"),
	path("<str:title>/", views.entry, name="entry"),
	path("<str:title>/edit/", views.edit, name="edit")
]
