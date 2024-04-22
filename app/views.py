from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
import requests
from newsapi import NewsApiClient
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

API_KEY = '9d3c0947d5bb4233828570f33ead5357'

@login_required(login_url='/login/')
def home(request):
    # url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}'
    # news = requests.get(url).json()
    newsapi = NewsApiClient(api_key=API_KEY)
    news = newsapi.get_top_headlines(country='gb')
    a = news['articles']

    desc = []
    title = []
    img = []
    url = []
    for i in range(len(a)):
        f = a[i]
        title.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
        url.append(f['url'])

        data_list = zip(title, desc, img, url)

    data = {
        'title': 'Articles home',
        'data': data_list,
        'blogs': BlogModel.objects.all(),
    }
    return render(request, 'home.html', data)


@login_required(login_url='/login/')
def dashboard(request):
    data = {
        'blogs': BlogModel.objects.filter(user=request.user),
    }
    return render(request, 'dashboard.html', data)


@login_required(login_url='/login/')
def blogdetail(request, slug):
    data = {
        'title': 'Blog detail',
        'blog': BlogModel.objects.get(slug=slug),
    }
    return render(request, 'blogdetail.html', data)


def register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    message = ""
    try:
        if request.method == 'POST':
            first_name = request.POST.get('userfirstname')
            last_name = request.POST.get('userlastname')
            email = request.POST.get('useremail')
            password = request.POST.get('userpassword')

            if request.POST.get('userfirstname') == "" or request.POST.get('userlastname') == "" or request.POST.get('useremail') == "" or request.POST.get('userpassword') == "":
                error = True
                return render(request, 'register.html', {'title': 'Register user', 'error': error})

            user_obj = User.objects.filter(username=email).first()

            if user_obj:
                message = ("Account with this email is already created.")
                return render(request, 'register.html', {'title': 'Register user', 'message': message})

            user_obj = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user_obj.set_password(password)
            user_obj.save()
            message = "Account successfully created"

    except Exception as e:
        print(e)

    data = {
        'title': 'Register user',
        'message': message,
    }
    return render(request, 'register.html', data)


def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    message = ""
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if request.POST.get('email') == "" or request.POST.get('password') == "":
                error = True
                return render(request, 'login.html', {'title': 'Login user', 'error': error})

            user_obj = User.objects.filter(username=email).first()
            if user_obj is None:
                message = ("Email not registered")
                return render(request, 'login.html', {'title': 'Login user', 'message': message})

            user_obj = authenticate(request, username=email, password=password)

            if user_obj is not None:
                auth_login(request, user_obj)
                next = request.GET.get('next')
                if next is not None:
                    return redirect(next)
                else:
                    return redirect('/dashboard/')
            else:
                message = "Incorrect Password"

    except Exception as e:
        print(e)

    data = {
        'title': 'Login user',
        'message': message,
    }
    return render(request, 'login.html', data)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')


@login_required
def update_profile(request):
    try:
        if request.method == 'POST':
            first_name = request.POST.get('u_firstname')
            last_name = request.POST.get('u_lastname')
            email = request.POST.get('u_email')

            user_obj = User.objects.get(username=request.user)
            if user_obj:
                user_obj.first_name = first_name
                user_obj.last_name = last_name
                user_obj.email = email
                user_obj.username = email
                user_obj.save()

    except Exception as e:
        print(e)

    return redirect('/dashboard/')


@login_required
def delete_blog(request, slug):
    blog = BlogModel.objects.get(slug=slug)
    blog.delete()
    return redirect('/dashboard/')


@login_required
def create_blog(request):
    try:
        if request.method == 'POST':
            title = request.POST.get("blog_title")
            poster = request.FILES['blog_poster']
            content = request.POST.get("blog_content")
            author = request.POST.get("blog_author")

            blog = BlogModel(
                user=request.user,
                title=title,
                poster=poster,
                content=content,
                author=author
            )
            blog.save()
            return redirect('/dashboard/')

    except Exception as e:
        print(e)

    return redirect('/dashboard/')


class BlogModelViewSet(viewsets.ModelViewSet):
    queryset = BlogModel.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]
