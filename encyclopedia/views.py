from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

import random
from markdown2 import Markdown

from . import util

def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})


def entry(request, title):
	"""
    If the entry title exists, it is converted to html and served,
    Else a 404 error page is served
    """
	entry = util.get_entry(title)
	if (entry != None):
		markdowner = Markdown()
		entry = markdowner.convert(entry)
		return render(request, "encyclopedia/entry.html", { "entry": entry })
	else:
		return render(request, "encyclopedia/error.html", {
			"error": {
				"code": 404,
				"msg": f"{title} NOT FOUND!"
			}
		})

  
def search(request):
	"""
    Either directs user to the entry searched for, or displays a list of
    all titles containing the search string
    """
	# print(request.GET.get('q'))
	if request.GET.get('q', '') != '' or request.GET.get('q', '') != '&':
		search_string = request.GET.get('q','')
		if (util.get_entry(search_string) != None):
			return redirect('entry', title = search_string)
		else:
			return render(request, "encyclopedia/search.html", {
				"results": filter(lambda x: (search_string in x), util.list_entries()),
				"search_string": search_string
			})
	else:
		return render(request, "encyclopedia/error.html", {
			"error": {
				"code": 405,
				"msg": "Method not allowed!"
			}
		})




def new(request):
	"""
    POST method to save new entry if the title does not already exist and 
    if it is not left blank. Otherwise, render appropriate error page.
    GET renders a blank form to create a new entry
    """
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
	else:
		return render(request, "encyclopedia/create_new.html")


def edit(request, title):
	"""
	POST method to save edited entry
	GET renders a prepoluted form with entry content
	"""
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		util.save_entry(title, content)
		return redirect('entry', title = title)
	else:
		return render(request, "encyclopedia/edit.html", {
				"title": title,
	            "content": util.get_entry(title)
	        })
	

def lucky(request):
	"""
    Serve a random wiki entry page.
    If there are no entries, render a 404 error page
    """
	if (len(util.list_entries()) > 0):
		return redirect('entry', title = random.choice(util.list_entries()))
	else:
		return render(request, "encyclopedia/error.html", {
			"error": {
				"code": 404,
				"msg": f"The encyclopedia is empty! Add some entries."
			}
		})
	
