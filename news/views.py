from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics

class PostListView(ListView):
	model = Post
	template_name = 'news/index.html'
	context_object_name = 'posts'
	ordering = ['-datetime']
	paginate_by = 5


class UserPostListView(ListView):
	model = Post
	template_name = 'news/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-datetime')


# Здесь был Азамат
class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/news'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



#API Views
class NewsList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer


	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
