from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auctions, Bids, Categories, Comments, Watchlist
from .forms import NewListing, BidForm, CommentForm

def index(request):
    # Attemp to get success message, returns None if no success msg
    success = request.GET.get("success", None)
    # Retrieve all listings
    auctions = Auctions.objects.filter(closed=False)
    bids = Bids.objects.all()

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "bids": bids,
        "success": success
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
def new(request):

    if request.method == "POST":
        form = NewListing(request.POST)

        if form.is_valid():
            product = form.cleaned_data["title"]
            url = form.cleaned_data["url"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["starting_price"]

        auction = Auctions(
            owner=request.user,
            product=product,
            url=url,
            category=category,
            description=description,
            starting_price=bid
        )

        auction.save()

        success = "Auction listed correctly!"
        url = reverse("index")
        return redirect(f'{url}?success={success}')
    else:
        form = NewListing()

    return render(request, "auctions/new.html", {
        "form": form,
    })

def detail(request, auction_id):
    auction = Auctions.objects.get(pk=auction_id)
    try:
        bid = Bids.objects.get(auction=auction)
        bid_price = bid.bid_amount
    except ObjectDoesNotExist:
        bid = None
        bid_price = 0
    comments = Comments.objects.filter(auction=auction)
    url = reverse("detail", args=[auction_id])
    bid_form = BidForm()
    comment_form = CommentForm()

    if request.method == "POST":
        # Handle bids
        if "place_bid" in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                new_bid = bid_form.cleaned_data["bid"]
                if bid == None and new_bid >= auction.starting_price and request.user != auction.owner:
                    first_bid = Bids(
                        auction=auction,
                        bidder=request.user,
                        bid_amount=new_bid,
                        count=1
                    )

                    first_bid.save()
                    success = "Bid placed correctly."
                    return redirect(f'{url}?success={success}')
                elif new_bid > bid_price and request.user != auction.owner:
                    bid.bid_amount = new_bid
                    bid.bidder = request.user
                    bid.count += 1
                    bid.save()
                    success = "Bid placed correctly."
                    return redirect(f'{url}?success={success}')
                elif request.user == auction.owner:
                    error = "The owner of the listing cannot place a new bid."
                    return redirect(f'{url}?error={error}')
                else:
                    error = "The new bid must be higher than the current price."
                    return redirect(f'{url}?error={error}')

            else:
                error = "Bid amount not valid."
                return redirect(f'{url}?error={error}')

        elif "add_comment" in request.POST:
            comment_data = CommentForm(request.POST)
            if comment_data.is_valid():
                new_comment = Comments(
                    user = request.user,
                    comment = comment_data.cleaned_data["comment"],
                    auction = auction
                )
                new_comment.save()
                success = "Comment stored correctly"
                return redirect(f'{url}?success={success}')

            else:
                error = "Input not valid."                
                return redirect(f'{url}?error={error}')

        elif "close_listing" in request.POST:
            auction.closed = True
            auction.save()
            return redirect("detail", auction_id=auction_id)

        elif "watchlist" in request.POST:
            add_watchlist = Watchlist(
                user = request.user,
                auction = auction
            )
            add_watchlist.save()
            success = "Listing added to your watchlist"
            return redirect(f'{url}?success={success}')
        
        elif "unwatch" in request.POST:
            remove_watchlist = Watchlist.objects.filter(user=request.user, auction=auction)
            remove_watchlist.delete()
            success = "Listing removed from watchlist"
            return redirect(f'{url}?success={success}')

    else:
        if auction.closed == False:
            if request.user.is_authenticated:
                added = Watchlist.objects.filter(user=request.user, auction=auction)
                success = request.GET.get("success", None)
                error = request.GET.get("error", None)
                return render(request, "auctions/details.html", {
                    "auction": auction,
                    "comments": comments,
                    "bid": bid,
                    "bid_form": bid_form,
                    "comment_form": comment_form,
                    "success": success,
                    "error": error,
                    "added": added
                })
            else:
                success = request.GET.get("success", None)
                error = request.GET.get("error", None)
                return render(request, "auctions/details.html", {
                    "auction": auction,
                    "comments": comments,
                    "bid": bid,
                    "bid_form": bid_form,
                    "comment_form": comment_form,
                    "success": success,
                    "error": error
                })
        else:
            message = "This listing is closed."
            if bid != None and request.user == bid.bidder:
                winner = "You won the listing. Congrats!"
                return render(request, "auctions/details.html", {
                    "auction": auction,
                    "comments": comments,
                    "bid": bid,
                    "winner": winner
                })
            else:
                return render(request, "auctions/details.html", {
                    "auction": auction,
                    "comments": comments,
                    "bid": bid,
                    "message": message
                })

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/listing-by-category.html", {
        "categories": categories
    })

def filterby(request, category):
    category = Categories.objects.filter(name=category)
    cat_selected = Auctions.objects.filter(category__in=category)
    if cat_selected == None:
        return render(request, "auctions/filterby.html")
    else:
        return render(request, "auctions/filterby.html", {
            "cat_selected": cat_selected
        })

@login_required
def watchlist(request):
    winned_bids = Bids.objects.filter(bidder=request.user)
    won_auctions = []
    for auction in winned_bids:
        if auction.auction.closed == True:
            won_auctions.append(auction)

    watchlist = Watchlist.objects.filter(auction__closed=False, user=request.user)

    return render(request, "auctions/watchlist.html", {
        "user_watchlist": watchlist,
        "won_auctions": won_auctions
    })