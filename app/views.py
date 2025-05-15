from django.shortcuts import render, redirect
from .forms import FeedbackForm, CommentForm, BlogForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment

def index(request):
    return render(request, 'app/index.html', {'title': 'Главная'})

def about(request):
    return render(request, 'app/about.html', {'title': 'О нас', 'message': 'Сведения о нас.'})

def contact(request):
    return render(request, 'app/contact.html', {'title': 'Контакты', 'message': 'Страница с нашими контактами.'})

def links(request):
    return render(request, 'app/links.html', {'title': 'Полезные ресурсы'})

def pool(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data
            context['form_submitted'] = True
            return render(request, 'app/pool.html', context)
    else:
        form = FeedbackForm()
    return render(request, 'app/pool.html', {'form': form})

def registration(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                validate_password(form.cleaned_data['password1'], user=None)
                form.save()
                return redirect("login")
            except ValidationError as e:
                form.add_error('password1', e)
    return render(request, "app/registration.html", {"regform": form})

def blog_list(request):
    blogs = Blog.objects.all().order_by('-posted')
    return render(request, 'app/blog_list.html', {'blogs': blogs, 'title': 'Блог'})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = blog.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = CommentForm()
    return render(request, 'app/blog_detail.html', {'blog': blog, 'comments': comments, 'form': form})

@login_required
def newpost(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_detail', blog_id=post.id)
    else:
        form = BlogForm()
    return render(request, 'app/newpost.html', {"form": form, "title": "Добавить статью"})

def videopost(request):
    return render(request, 'app/videopost.html', {'title': 'Видеоматериалы'})