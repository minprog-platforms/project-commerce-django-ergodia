from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.category_name}"


class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=360)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=5)
    photo_url = models.URLField(max_length=250, blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="listings")
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.amount}"


class Comment(models.Model):
    text = models.CharField(max_length=360)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} on {self.auction}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user}: {self.auction}"
