from django import forms

class NewPost(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="New Post", required=True)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content