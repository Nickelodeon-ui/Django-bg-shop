from django.shortcuts import render
from django.conf import settings
from django.views.generic import FormView, View
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse,FileResponse
from django.urls import reverse_lazy

from .models import Customer
from .forms import CustomerForm, MyLoginForm


class RegistrationFormView(FormView):

    form_class = CustomerForm
    template_name = "login_registration/registration.html"
    success_url = reverse_lazy("boardgames:catalog")

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
            return render(request, "login_registration/registration.html", {"form": form})


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("boardgames:catalog")


class MyLoginView(LoginView):
    authentication_form = MyLoginForm
    template_name = "login_registration/login.html"

    def get_success_url(self):
        return reverse_lazy("boardgames:catalog")