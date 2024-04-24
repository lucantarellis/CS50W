from django import forms

from .models import Categories

class NewListing(forms.Form):
    title = forms.CharField(label="Title")
    category = forms.ModelChoiceField(queryset=Categories.objects.all())
    url = forms.URLField(label="Image's URL", required=False, widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    starting_price = forms.DecimalField(label="Starting price")

    def clean_url(self): # Probar que pasa si cambio el clean por default
        url = self.cleaned_data.get('url')
        if not url: # CHECK
            url = "https://imgur.com/TZjsMoi.jpg/"
        return url

    def __init__(self, *args, **kwargs):
        # Defaulting to None in case there's no categories
        categories = kwargs.pop('categories', None)
        # Calling the superclass to set up the fields for category
        super(NewListing, self).__init__(*args, **kwargs)
        if categories:
            self.fields['category'].queryset = categories

class BidForm(forms.Form):
    bid = forms.DecimalField(label="Place a bid")

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Write a comment")