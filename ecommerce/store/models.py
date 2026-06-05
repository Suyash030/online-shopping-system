from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total() for item in items])
        return total

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
    
    from django.contrib.auth.models import User

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"