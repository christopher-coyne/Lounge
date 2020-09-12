from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse

from posts.models import User, Post, Comment, Subreddit
# Create your views here.

#testing branch comment

#FORMS
class NewPost(forms.Form):
  #poster already provided in user
  #upvotes start at 1
  title = forms.CharField(label = "Post Title", widget=forms.TextInput(attrs={'placeholder': 'Required'}), max_length=100, min_length=1)
  image_url = forms.CharField(label = "Image Url", widget=forms.Textarea(attrs={'placeholder': 'Optional If You Have Text'}), required=False, max_length=1000)
  content = forms.CharField(label = "Text", widget=forms.Textarea(attrs={'placeholder': 'Optional If You Have Link/Image'}), required=False, max_length=1000)
  sub = forms.CharField(label = "SubLounge", widget=forms.TextInput(attrs={'placeholder': 'SubLounge'}))

class NewSub(forms.Form):
  title = forms.CharField(label = "New SubLounge Title", widget=forms.TextInput(attrs={'placeholder': 'Required'}), max_length=100, min_length=1)

class AddComment(forms.Form):
  content = forms.CharField(label = "Comment", widget=forms.TextInput(attrs={'placeholder': 'Your Comment Here'}), max_length=500, min_length=1)

#FUNCTIONS
def index(request):
  subnames = Subreddit.objects.all()
  postnames = Post.objects.all()
  return render(request, "posts/index.html", {
    "sublist": subnames,
    "postlist": postnames
  })

def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
      return render(request, "posts/register.html", {
          "message": "Your passwords must match."
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "posts/register.html", {
          "message": "Username already taken."
      })
    login(request, user)
    return HttpResponseRedirect(reverse("index"), {
      "message": "Success! Your account has been created. "
    })
  else:
      return render(request, "posts/register.html")

def login_view(request):
  if request.method == "POST":

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"), {
        'message': 'Login Successful'
      })
    else:
      return render(request, "posts/login.html", {
          "message": "Invalid username and/or password."
      })
  else:
      return render(request, "posts/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def create_post(request):
  if request.method == "POST":
    form = NewPost(request.POST)
    if form.is_valid():
      title = request.POST["title"]
      image_url = request.POST["image_url"]
      content = request.POST["content"]
      subname = request.POST["sub"]
      sub = Subreddit.objects.filter(name=subname)[0]
      new_post = Post(poster=request.user, image_url=image_url, content=content, upvotes=1, subreddit=sub, title=title)
      new_post.save()
      return HttpResponseRedirect(reverse("index"))
  return render(request, "posts/newpost.html", {
    "form": NewPost()
  })

def create_sub(request):
  if request.method == "POST":
    form = NewSub(request.POST)
    if form.is_valid():
      sub_name = request.POST["title"]
      #OBVIOUSLY CHANGE THIS LATER
      new_sub = Subreddit(name=sub_name, logo=None)
      new_sub.save()
      return render(request, "posts/newsub.html", {
        "message": "New SubLounge has been created!"
      })
  return render(request, "posts/newsub.html", {
    "form": NewSub()
  })

def post_page(request, id):
  mypost = Post.objects.get(pk=id)
  if request.method == "POST":
    form = AddComment(request.POST)
    if form.is_valid():
      poster = request.user
      content = request.POST['content']
      upvotes = 1
      root = None
      post = Post.objects.get(pk=id)

      new_comment = Comment(poster=poster, content=content, upvotes=upvotes, root=root, post=post)
      new_comment.save()

      return render(request, "posts/post_page.html", {
          "post": mypost,
          "form": AddComment(),
          "comments": Comment.objects.all()
        })

  return render(request, "posts/post_page.html", {
    "post": mypost,
    "form": AddComment(),
    "comments": Comment.objects.all()
  })

'''
MAKE A NEW SUB, TEST THAT SUB THAT DOES NOT HAVE SPACES in it, since urls cant have spaces
'''
def sub_page(request, name):
  sublounge = Subreddit.objects.get(name=name)
  return render(request, "posts/sub_page.html", {
    "subname": name,
    "subposts": Post.objects.filter(subreddit=sublounge)
  })


