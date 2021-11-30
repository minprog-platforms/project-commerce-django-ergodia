from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, reset_queries
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, CharField, Textarea
from .models import Auction, Bid, Category, Comment, Watchlist
from django.contrib.auth.decorators import login_required


from .models import User


class AuctionForm(ModelForm):
    description = CharField(widget=Textarea)
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'photo_url', 'category']
        labels = {
            'photo_url': 'Photo URL (optional)',
            'category': 'Category (optional)'
        }

def index(request):
    # retrieve the listings that are active
    auctions = Auction.objects.filter(active="True")

    return render(request, "auctions/index.html", {
        "auctions": auctions
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_page(request):
    if request.method == "POST":

        form = AuctionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = AuctionForm()
        
        return render(request, "auctions/create_page.html", {
            "form": form
        })
