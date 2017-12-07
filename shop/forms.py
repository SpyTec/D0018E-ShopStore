from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(label='comment', max_length=255)


class SearchForm(forms.Form):
    query = forms.CharField(label='query', max_length=255)
