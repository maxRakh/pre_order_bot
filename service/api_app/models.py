from django.db import models


class PreOrder(models.Model):
    number = models.IntegerField()
    product = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=15)
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    city = models.CharField(max_length=20)
    shipping_adress = models.CharField(max_length=200)
    shipping_price = models.PositiveIntegerField()
    client_name = models.CharField(max_length=50)
    client_phone_number = models.CharField(max_length=20)
    type_of_connect = models.CharField(max_length=50)
    date_ordered = models.DateTimeField(auto_now_add=True)
    bought = models.BooleanField(default=False)
    day_of_bought = models.DateTimeField(null=True, blank=True)
    canceled = models.BooleanField(default=False)
    day_of_canceled = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.number}"
