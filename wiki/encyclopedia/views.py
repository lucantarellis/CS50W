from django.http import HttpResponseRedirect
from django.shortcuts import render
from random import choice
from django.urls import reverse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entries.html", {
            "entry_page": markdown2.markdown(util.get_entry(entry)),
            "entry": entry
    })
    else:
        return render(request, "encyclopedia/entries.html", {
            "url": request.get_full_path()
        })

def search(request):
    # Request search query and makes it lowercase
    query = request.GET.get("q", "")
    query_low = query.lower()
    # Check if query exists, if true it renders the entry page
    if util.get_entry(query):  
        return render(request, "encyclopedia/entries.html", {
            "entry_page": markdown2.markdown(util.get_entry(query)),
            "entry": query
        })
    # If false it looks for substrings and shows entries that match
    else:
        # Create empty list
        entries_found = []
        # Store list of entries in entries variable
        entries = util.list_entries()
        # Loop through the list of entries to make them lowercase, as done with the query
        for entry in entries:
            entry_low = entry.lower()
            # Checks if query is a substring of entry
            if query_low in entry_low:
                # If it is, it'll append the entry into entries_found list
                entries_found.append(entry)
        # Returns entries found
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries_found": entries_found,
            # "entries" is passed because if there's no entries_found it'll show the list of all the entries
            "entries": entries
        })

def new(request):
    if request.method == "POST":
        # Request new entry data
        new_title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        # Store list of entries
        entries = util.list_entries()
        for entry in entries:
            entry = entry.lower()
            low_title = new_title.lower()
            # Check if title already exists
            if low_title in entry:
                # Raise error if it does and render content
                error = "Title already exist. Try another."
                return render(request, "encyclopedia/new.html", {
                    "error": error,
                    "title": new_title,
                    "content": content
                })
        # If it does not exist, it saves the new entry and renders content
        util.save_entry(new_title, content)
        return render(request, "encyclopedia/entries.html", {
            "entry_page": markdown2.markdown(content),
            "entry": new_title
        })
    else:
        return render(request, "encyclopedia/new.html")
    
def edit(request, entry):
    if request.method == "POST":
        # Request entry content to be saved in the new version of entry
        content = request.POST.get("content", "")
        util.save_entry(entry, content)
        return render(request, "encyclopedia/entries.html", {
            "entry_page": markdown2.markdown(content),
            "entry": entry
        })
    else:
        # Request entry content to populate textarea tag
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
            "entry": entry,
            "content": content
        })
    
def random(request):
    # Assign list of entries to a variable to use that variable to get a random element from the list
    entry_list = util.list_entries()
    random_entry = choice(entry_list)
    # Return random content using entries.html template
    return HttpResponseRedirect(reverse("entry", args=[random_entry]))


