from django import forms
from .models import Comment #имортируем комменты из моделей

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #Django auto использует все поля модели но мы явно укажем нужные поля fields
        fields = ('name', 'email', 'body')


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)