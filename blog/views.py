from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
	"""Возвращает список опубликованных постов."""
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
	"""Возвращает определённый пост."""
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
	"""Создаёт новый пост в блоге с помощью формы."""
	if request.method == 'POST':
	    form = PostForm(request.POST)
	    if form.is_valid():
	        post = form.save(commit=False)
	        post.author = request.user
	        post.save()
	        return redirect('post_detail', pk=post.pk)
	else:
	    form = PostForm()

	return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
	"""Редактирует определённый пост с помощью формы."""
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
	    form = PostForm(request.POST, instance=post)
	    if form.is_valid():
	        post = form.save(commit=False)
	        post.author = request.user
	        post.save()
	        return redirect('post_detail', pk=post.pk)
	else:
	    form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
	"""Возвращает список чернеток (неопубликованных постов)."""
	posts = Post.objects.filter(
	    published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
	"""Публикация поста в блог."""
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
	"""Удаляет пост из блога."""
	post = get_object_or_404(Post, pk=pk)
	if post.published_date:
	    post.delete()
	    return redirect('post_list')
	else:
	    post.delete()
	    return redirect('post_draft_list')


def add_comment_to_post(request, pk):
	"""Добавляет комментарий к определённому посту с помощью формы."""
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
	"""Подтверждает комментарий, что делает его видимым для остальных пользователей."""
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
	"""Удаляет комментарий под определённым постом."""
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)
