from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, reset_queries
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, CharField, Textarea, ValidationError
from .models import Auction, Bid, Category, Comment, Watchlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            'amount': 'Make a bid:',
        }
    def __init__(self, auction_id, *args, **kwargs):
        self._starting_bid = float(Auction.objects.filter(id=auction_id)[0].starting_bid)
        try:
            self._highest_bid = float(Bid.objects.filter(auction=auction_id).last().amount)
        except Exception:
            self._highest_bid = None
        super(BidForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self._highest_bid is not None:
            if float(self.data["amount"]) <= self._highest_bid:
                raise ValidationError("The bid must be higher than the current bid")
        elif self._highest_bid is None:
            if float(self.data["amount"]) < self._starting_bid:
                raise ValidationError("The bid must be higher or equal to the starting bid")
        return self.data


class CommentForm(ModelForm):
    text = CharField(label="Comment Text:", widget=Textarea(attrs={'rows': 4, 'cols': 15}))
    class Meta:
        model = Comment
        fields = ['text']


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
            form = form.save(commit= False)
            
            # add the user to the form
            form.user = request.user
            form.save()
            return HttpResponseRedirect(f"listing/{form.pk}")

    else:
        form = AuctionForm()
        
        return render(request, "auctions/create_page.html", {
            "form": form
        })


def listing_page(request, id): 
        auction = Auction.objects.get(pk=id)
        comments = Comment.objects.filter(auction=auction)
        return render(request, "auctions/listing_page.html", {
            "auction": auction,
            "comments": comments,
            "bid_form": BidForm(id),
            "comment_form": CommentForm()
        })
    #except Exception:
    #    return render(request, "auctions/error_page.html")

@login_required
def watchlist_edit(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        
        # try to find if the auction is already been put in the watchlist by the user
        try:
            watchlist = Watchlist.objects.get(Q(auction = auction) | Q(user = request.user))
        except Exception:
            watchlist = None

        # add item to watchlist if not there and delte it if its there
        if watchlist is None:
            watchlist = Watchlist()
            watchlist.user = request.user
            watchlist.auction = auction
            watchlist.save()
        else:
            watchlist.delete()
        
        return HttpResponseRedirect(f"/listing/{auction_id}")

@login_required
def close_listing(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        auction.active = False
        auction.save()

        return HttpResponseRedirect(f"/listing/{auction_id}")

@login_required
def bid(request, auction_id):
    if request.method == "POST":

        form = BidForm(auction_id, request.POST)
        auction = Auction.objects.get(pk=auction_id)
        comments = Comment.objects.filter(auction=auction)

        if form.is_valid():
            # try to find if the user already bid on the auction
            try:
                previous_bid = Bid.objects.get(Q(auction = auction) | Q(user = request.user))
            except Exception:
                previous_bid = None

            # delete previous bid if there is any
            if previous_bid is not None:
                previous_bid.delete()
            
            form = form.save(commit= False)
            
            # add the user to the form
            form.user = request.user
            form.auction = auction
            form.save()
            return HttpResponseRedirect(f"/listing/{auction_id}")

        else:
            # return the same page in case of an error
            return render(request, "auctions/listing_page.html", {
            "auction": auction,
            "comments": comments,
            "bid_form": form,
            "comment_form": CommentForm()
            })


def comment(request, auction_id):
    if request.method == "POST":

        form = CommentForm(request.POST)
        auction = Auction.objects.get(pk=auction_id)

        if form.is_valid():
            form = form.save(commit= False)
            
            # add the user to the form
            form.user = request.user
            form.auction = auction
            form.save()
            
            return HttpResponseRedirect(f"/listing/{auction_id}")
