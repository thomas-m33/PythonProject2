from django import forms
from .models import Post
from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'tags']
        # This is the data that the views normally require. The code below is to make categories and tags show up properly.

        widgets = {
            'categories': forms.SelectMultiple(attrs={
                'size': 6,  # how many options are visible
                'class': 'form-control',  # use Bootstrap styling
            }),
            'tags': TagWidget(attrs={'class': 'form-control'})
            # The TagWidget makes sure the tags are displayed as text and not as a Python list
            # If you just use forms.TextInput() it shows up as ['tag1', 'tag2', etc.] in the post update page.
        }
