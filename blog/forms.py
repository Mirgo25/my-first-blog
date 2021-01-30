from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
	"""Форма для добавления/редактирования поста в блоге."""
	class Meta:
	    model = Post
	    fields = ('title', 'text')


class CommentForm(forms.ModelForm):
	"""Форма для добавления комментария под постом."""
	class Meta:
		model = Comment
		fields = ('author', 'text')
		