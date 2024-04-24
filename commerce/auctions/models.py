from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Auctions(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=64)
    url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category")
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    closed = models.BooleanField(default=False)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.product

class Bids(models.Model):
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Bid by {self.bidder.username} on {self.auction.product}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment made by {self.user.username} on {self.auction.product}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, null=True)
