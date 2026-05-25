from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    icon = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True, verbose_name="Tavsifi")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")
    brand = models.CharField(max_length=100, verbose_name="Brend", default="Nomalum")
    specs = models.TextField(null=True, blank=True, verbose_name="Texnik xususiyatlari")
    stock = models.IntegerField(verbose_name="Omborda", default=10)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 verbose_name="Kategoriyasi", related_name="products")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-id']

    def get_image(self):
        imgs = self.images.all()
        if imgs:
            return imgs[0].image.url
        return "https://placehold.co/500x500/1e293b/60a5fa?text=TechZone"

    def avg_rating(self):
        comments = self.comment_set.all()
        if not comments:
            return 0
        return round(sum(c.rate for c in comments) / len(comments), 1)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"{self.product.name}"


class Comment(models.Model):
    text = models.CharField(max_length=500)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonim'}: {self.text}"

    class Meta:
        ordering = ['-time']


class Order(models.Model):
    PAYMENT_TYPE = {
        'cash': 'Naqd pul',
        'card': 'Karta',
        'stripe': 'Stripe'
    }
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE)
    delivery = models.BooleanField(default=False)
    address = models.CharField(max_length=500, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"#{self.pk} - {self.user.username}"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created']


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.product.name if self.product else "O'chirilgan mahsulot"

    def subtotal(self):
        return self.price * self.quantity
