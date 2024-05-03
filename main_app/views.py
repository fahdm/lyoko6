from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,  UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Post, Comment, Category
from .forms import PostForm,CommentForm
import logging

logger = logging.getLogger(__name__)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {"posts": posts}
    return render(request, 'home.html', context)

def post_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {"category": category, "posts": posts}
    return render(request, "posts/category.html", context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  
            comment.post = post  
            comment.save()
            return HttpResponseRedirect(request.path_info)  

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post_id)  
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comments/edit_comment.html', {'form': form})





class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully')
        return super().form_valid(form)

class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/edit_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments_post.html'  

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user  
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
    
# class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Comment
#     template_name = 'comments/confirm_delete.html'

#     success_url = reverse_lazy('detail')  

#     def form_valid(self, form):
#         logger.debug("Form valid, processing deletion")
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         logger.error("Form invalid: %s", form.errors)
#         return super().form_invalid(form)

#     def test_func(self):
#         comment = self.get_object()
#         return self.request.user == comment.author

#     def get_success_url(self):
#         comment = self.get_object()
#         return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comments/confirm_delete.html'

    def get_success_url(self):
       
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def delete(self, request, *args, **kwargs):
    
        return super().delete(request, *args, **kwargs)