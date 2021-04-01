# pylint: skip-file

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Count


class BoardGameManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def get_queryset_with_url(self):
        qs = self.get_queryset()
        data = [
            dict(name=bg.name, eng_name=bg.eng_name, quantity=bg.quantity,
                 price=bg.price, img=bg.img, slug=bg.slug, url=bg.get_absolute_url())
            for bg in qs
        ]
        return data


class BoardGame(models.Model):

    name = models.CharField('Название игры', max_length=50)
    eng_name = models.CharField(
        "Название игры на английском", max_length=50, blank=True)
    description = models.TextField('Описание')
    quantity = models.IntegerField("Количество", validators=[MinValueValidator(
        limit_value=0, message="Не может быть меньше 0 игр")])
    price = models.DecimalField('Цена', max_digits=5, decimal_places=2)
    add_date = models.DateField('Дата добавления', default=timezone.now())
    img = models.ImageField("Обложка игры", upload_to='bgpictures/')
    slug = models.SlugField("Название для URL", blank=True, unique=True)

    objects = BoardGameManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("one_bg", kwargs={"slug": self.slug})


class CartProduct(models.Model):
    boardgame = models.ForeignKey(
        "BoardGame", verbose_name=("Товар"), on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(
        verbose_name=("Количество товара"), default=1)
    price_for_product = models.DecimalField(
        'Цена для товара', max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Товар {self.boardgame.name} в корзине"

    def save(self, *args, **kwargs):
        self.price_for_product = self.qty * self.boardgame.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey("Customer", verbose_name=(
        "Владелец"), on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(
        "CartProduct", verbose_name=("Товары в корзине"), blank=True)
    total_product = models.PositiveIntegerField(
        verbose_name="Всего товаров в корзине", default=0)
    final_price = models.DecimalField(
        "Цена для всей корзины", max_digits=7, decimal_places=2, default=0)
    # Для того чтобы когда покупатель оплатил корзину, он мог класть товары в новую корзину
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        if self.for_anonymous_user is False:
            return f"Корзина принадлежит {self.owner.user.username} и в ней {self.total_product} товаров"
        else:
            return f"Корзина анонимного пользвателя и в ней {self.total_product} товаров"
    
    def save(self, *args, **kwargs):
        if self.pk:
            cart_data = self.products.aggregate(total_price=Sum("price_for_product"), total_qty=Sum("qty"))
            if cart_data.get("total_price"): # При большем числе выдаёт ошибку, потому что max_digits = 7 
                cart_data["total_price"] = round(cart_data["total_price"], 2)
                self.final_price = cart_data["total_price"]
            else:
                self.final_price = 0
            if cart_data.get("total_qty"):
                self.total_product = cart_data["total_qty"]
            else:
                self.total_product = 0
        super().save(*args, **kwargs)

class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"Это пользователь {self.user.username}: {self.user.first_name} {self.user.last_name}"
    
@receiver(post_save, sender=User)
def user_save_handler(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()   # --- Хз
