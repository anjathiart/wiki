from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class EntryEditForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea)
	# title = forms.CharField(label="New Task")
	# priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)


def index(request):
	print(util.list_entries())
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})


def entry(request, title):
	entry = util.get_entry(title)
	if (entry != None):
		return render(request, "encyclopedia/entry.html", { "entry": entry })
	else:
		return render(request, "encyclopedia/error.html", {
			"error": {
				"code": 404,
				"msg": f"{title} NOT FOUND!"
			}
		})

def search(request):
	if (request.GET.get('q', '') != ''):
		search_string = request.GET.get('q','')
		if (util.get_entry(search_string) != None):
			return redirect('entry', title = search_string)
		else:
			# TODO -> try use a lamda search / filter function instead
			list_entries_matched = []
			for entry_title in util.list_entries():
				if (search_string in entry_title):
					list_entries_matched.append(entry_title)
			return render(request, "encyclopedia/search.html", {
				"results": list_entries_matched,
				"search_string": search_string
			})

def new(request):
	return render(request, "encyclopedia/create_new.html")

def save(request):
	print(request)
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get('content')
		if title in util.list_entries():
			return render(request, "encyclopedia/error.html", {
				"error": {
					"code": 400,
					"msg": f"This title, {title}, already exists!"
				}
			})
		if title == '':
			return render(request, "encyclopedia/error.html", {
				"error": {
					"code": 400,
					"msg": f"Please add an entry title!"
				}
			})
		util.save_entry(title, content)
		return redirect('entry', title = title)

def edit(request, title):
	# TODO --> some error handling
	if request.method == "GET":
		return render(request, "encyclopedia/edit.html", {
				"title": title,
	            "content": util.get_entry(title)
	        })
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		util.save_entry(title, content)
		return redirect('entry', title = title)



	
	
