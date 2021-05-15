# pylint: skip-file

from django.views.generic.edit import FormMixin
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.base import ContextMixin

from login_registration.models import Customer
from .forms import Submit_BG_form
from .models import BoardGame, Cart, CartProduct


class SuggestionFormMixin(FormMixin):
    
    form_class = Submit_BG_form

    def post(self, request, *args, **kwargs):
        if request.POST.get("suggestion_bg"):
            form = Submit_BG_form(request.POST)
            if form.is_valid():
                # Отправка пожелания или отзыва менеджерам
                customer_name = form.cleaned_data["customer_name"]
                message = form.cleaned_data["message"]
                message = f"Имя: {customer_name} \nСообщение: {message}"
                send_mail(
                    "Поиск игры или отзыв покупателя",
                    message, 
                    settings.EMAIL_HOST_USER,  # В setting заменить на новый созданный
                    ["borodachnikolay@mail.ru"]  # Список менеджеров
                )
                return HttpResponseRedirect(self.request.get_full_path_info()) #Должно возвращать на ту же страницу но хз

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            # Как различать анонимных пользователей чтобы у них не была общая корзина?
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = self.cart
        return context