from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_page, name="create"),
    path("listing/<int:id>", views.listing_page, name="listing_page"),
    path("watchlist_edit/<int:auction_id>", views.watchlist_edit, name="watchlist_edit"),
    path("close_listing/<int:auction_id>", views.close_listing, name="close_listing"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("comment/<int:auction_id>", views.comment, name="comment")
]
