# pylint: skip-file

from django.urls import path

from .views import (
    BoardGamesListView,
    BoardGamesDetailView,
    RegistrationFormView,
    MyLogoutView,
    MyLoginView,
    CartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartView,
    BggHot15View,
    MoreBoardGamesView,
    DownloadCSVView,
    DownloadPDFView
    )


urlpatterns = [
    path('', BoardGamesListView.as_view(), name="catalog"),
    path("more-bg/<int:lower_border>", MoreBoardGamesView.as_view(), name="more_bg"),
    path("register", RegistrationFormView.as_view(), name="register"),
    path("login", MyLoginView.as_view(), name="login"),
    path("logout", MyLogoutView.as_view(), name="logout"),
    path("cart", CartView.as_view(), name="cart"),
    path("cart/update-cart", UpdateCartView.as_view(), name="update_cart"),
    path("add-to-cart/<slug:slug>", AddToCartView.as_view(), name="add_to_cart"),
    path("remove-from-cart/<slug:slug>", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("hot15bgg", BggHot15View.as_view(), name="hot15bgg"),
    path("<slug:slug>", BoardGamesDetailView.as_view(), name="one_bg"),
    path("download-csv/", DownloadCSVView.as_view(), name="download_csv"),
    path("download-pdf/", DownloadPDFView.as_view(), name="download_pdf")
]   