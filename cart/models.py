from django.db import models

# Create your models here.

class Cart(models.Model):
    cartProductId = models.AutoField(primary_key=True)
    productId = models.IntegerField()
    quantity = models.IntegerField()
    buyerUsername =  models.CharField(max_length=100)
    sellerUsername = models.CharField(max_length=100)

    def __str__(self):
        return f"Cart ID: {self.cartProductId}"
