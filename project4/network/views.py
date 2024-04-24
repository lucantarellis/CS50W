from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Relationship
from .forms import NewPost


def index(request):

    if request.method == "POST":
        form = NewPost(request.POST)

        if form.is_valid():
            new_post = Post(
                user=request.user,
                content=form.cleaned_data['content'],
                )
            new_post.save()

            success = "Post submited"
            url = reverse("index")
            return redirect(f'{url}?success={success}')
    else:
        posts = Post.objects.order_by('-date')
        form = NewPost()


    return render(request, "network/index.html", {
        "posts" : posts,
        "form" : form
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, user_id):

    url = reverse("profile", args=[user_id])
    current_user = User.objects.get(pk=request.user.id)
    other_user = User.objects.get(pk=user_id)
    is_following = current_user.is_following(other_user)

    if request.method == "POST":

        if "unfollow" in request.POST:
            current_user.unfollow(other_user)
            success = "User unfollowed."
            return redirect(f'{url}?success={success}')
        
        elif "follow" in request.POST:
            current_user.follow(other_user)
            success = "User followed."
            return redirect(f'{url}?success={success}')

    else:
        success = request.GET.get("success", None)
        error = request.GET.get("error", None)
        profile = User.objects.get(pk=user_id)
        
        try:
            posts = Post.objects.filter(user=user_id).order_by('-date')
        except ObjectDoesNotExist:
            posts = None

        return render(request, "network/profile.html", {
            "posts" : posts,
            "profile" : profile,
            "is_following" : is_following,
            "success" : success,
            "error" : error
        })
    
@login_required   
def following(request):
    user = request.user

    # Get all users the logged-in user is following
    following_users = User.objects.filter(followers__follower=user)

    # Get posts from these following users ordered by newest to oldest
    following_posts = Post.objects.filter(user__in=following_users).order_by('-date')
    paginator = Paginator(following_posts, 10)

    page_number = request.GET.get('page')
    page_posts= paginator.get_page(page_number)

    return render(request, 'network/following.html', {
        'page_posts': page_posts
    })