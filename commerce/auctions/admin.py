from django.contrib import admin

from .models import Categories, Auctions, Bids, Comments, Watchlist

# Register your models here.
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)

class AuctionsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.url:  # If URL is not provided
            obj.url = 'https://imgur.com/TZjsMoi.jpg/'
        super().save_model(request, obj, form, change)

admin.site.register(Auctions, AuctionsAdmin)