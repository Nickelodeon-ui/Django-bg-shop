# pylint: skip-file
import os
import csv
import json
import io
from reportlab.pdfgen import canvas
from boardgamegeek import BGGClient

from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, DetailView, FormView, View
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse,FileResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.sessions.models import Session
from django.http import JsonResponse

from .models import BoardGame, Customer, Cart, CartProduct
from .forms import Submit_BG_form, CustomerForm, MyLoginForm
from .mixins import SuggestionFormMixin, CartMixin


class BoardGamesListView(CartMixin, SuggestionFormMixin, ListView):

    model = BoardGame
    template_name = "home.html"
    context_object_name = "boardgames"

    def get_queryset(self):
        return self.model.objects.get_queryset_with_url()[:9]


class MoreBoardGamesView(View):
    def get(self, request, *args, **kwargs):
        bgs = list(BoardGame.objects.values())
        lower_border = kwargs["lower_border"]
        upper_border = lower_border + 3

        reached_max = True if upper_border >= len(bgs) else False

        bgs = bgs[lower_border:upper_border]
        return JsonResponse(data={"data": bgs, "reached_max": reached_max})


class DownloadCSVView(View):
    def get(self, request, *args, **kwargs):
        bg_qs = BoardGame.objects.get_queryset_with_url()

        with open("bg_catalog.csv", 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Название на русском", "Название на английском", "Количество на складе", "Цена", "Ссылка"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for bg in bg_qs:
                writer.writerow({"Название на русском": bg.get('name'), "Название на английском": bg.get('eng_name'),
                                "Количество на складе": bg.get('quantity'), "Цена": bg.get('price'), "Ссылка": 'http://127.0.0.1:8000' + bg.get('url')})
                    
        with open("bg_catalog.csv", 'r', newline='', encoding='utf-8') as csvfile:
            response = HttpResponse(csvfile, content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="bg_catalog.csv"' 

        os.remove('bg_catalog.csv')
        return response

class DownloadPDFView(View):
    
    def get(self, request, *args, **kwargs):
        buffer = io.BytesIO()
        
        p = canvas.Canvas(buffer)
        ##############


        ##############
        # Сначала заканчиваем создавать страницу, закрывая её
        p.showPage()
        # Создается pdf-файл
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

class BoardGamesDetailView(CartMixin, SuggestionFormMixin, DetailView):

    model = BoardGame
    context_object_name = "boardgame"
    template_name = "boardgames/one_bg.html"
    slug_url_kwarg = "slug"
    slug_field = "slug"

    def get_queryset(self):
        return super().get_queryset().filter(slug__exact=self.kwargs.get("slug"))


class RegistrationFormView(FormView):

    form_class = CustomerForm
    template_name = "boardgames/registration.html"
    success_url = reverse_lazy("catalog")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Если пользователь уже есть в БД
            user = authenticate(
                username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                # создается объект user из формы и сигнал post_save (created=True) создает связь one to one
                user = form.save()
                # Для предотвращения ошибки получаем созданный объект из БД, потому что пока что у нас в user лежит объект
                # без поля One to one (которое задастся путем сигнала-ресивера), а просто объект класса user - для доступа к полям address и phone
                user.refresh_from_db()
                address = form.cleaned_data["address"]
                phone = form.cleaned_data["phone"]
                user.customer.address = address
                user.customer.phone = phone
                user.save()
                login(request, user)
                return HttpResponseRedirect(self.get_success_url())
        else:
            # return HttpResponseRedirect(self.request.path_info)
            return render(request, "boardgames/registration.html", {"form": form})


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("catalog")


class MyLoginView(LoginView):
    authentication_form = MyLoginForm
    template_name = "boardgames/login.html"

    def get_success_url(self):
        return reverse_lazy("catalog")


class CartView(CartMixin, SuggestionFormMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            "cart": self.cart,
            "form": self.get_form()
        }
        return render(request, "boardgames/cart.html", context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        bg_slug = kwargs["slug"]
        bg = BoardGame.objects.get(slug=bg_slug)

        if bg in [product.boardgame for product in self.cart.products.all()]:
            cart_product = self.cart.products.filter(boardgame=bg)[0]
            cart_product.qty += 1
            cart_product.save()
        else:
            cart_product = CartProduct.objects.create(boardgame=bg)
            self.cart.products.add(cart_product)

        self.cart.save()
        messages.add_message(request, messages.INFO,
                             "Товар был добавлен в корзину")
        return HttpResponseRedirect(reverse_lazy('one_bg', kwargs={"slug": self.kwargs.get("slug")}))


class RemoveFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        bg_slug = kwargs["slug"]
        bg = BoardGame.objects.get(slug=bg_slug)

        cart_product = self.cart.products.filter(boardgame=bg)[0]
        self.cart.products.remove(cart_product)
        cart_product.delete()

        self.cart.save()
        messages.add_message(request, messages.INFO,
                             "Товар был удалён из корзины")
        return HttpResponseRedirect(reverse_lazy('cart'))


class UpdateCartView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        old_data = [[item.boardgame.name, item.qty]
                    for item in self.cart.products.all()]
        for old_val, new_val in zip(old_data, request.POST.items()):
            # Думаю оно будет правильно работать, т.к. zip идет до самой малой по длине из последовательностей

            old_name = old_val[0]
            new_name = new_val[0]
            old_qty = old_val[1]
            new_qty = int(new_val[1])

            if old_name == new_name and old_qty != new_qty:
                bg = BoardGame.objects.get(name=old_name)
                cart_product = self.cart.products.filter(boardgame=bg).first()
                cart_product.qty = new_qty

                cart_product.save()
                self.cart.save()
        # Сделать проверку на правильность выполненности view

        # Для случая, когда все хорошо
        response = {
            'status': 1,
            'message': 'Всё хорошо',
            'url': str(reverse_lazy('cart'))
        }

        messages.add_message(request, messages.INFO,
                             "Корзина обновлена успешно")
        return HttpResponse(json.dumps(response), content_type='application/json')


class BggHot15View(CartMixin, SuggestionFormMixin, View):
    def get(self, request, *args, **kwargs):
        bgg = BGGClient()
        lst = bgg.hot_items("boardgame")
        lst = lst[:25]

        all_db_bg = BoardGame.objects.get_queryset_with_url()
        all_db_bg_titles = [bg.get("eng_name").lower() for bg in all_db_bg]
        all_db_bg = [{bg.get("eng_name").lower(): bg.get(
            "url"), "ru_name": bg.get("name")} for bg in all_db_bg]

        context = {
            "cart": self.cart,
            "form": self.get_form(),
            "hot25lst": lst[:15],
            "all_db_bg": all_db_bg,
            "all_db_bg_titles": all_db_bg_titles
        }
        return render(request, "boardgames/bgghot15.html", context)
