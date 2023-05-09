from django.db import models

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    buyer_username = models.CharField(max_length=100)
    total_price = models.IntegerField()
    status_order = models.CharField(max_length=100)
    seller_username = models.CharField(max_length=100)

    def __str__(self):
        return f"Order ID: {self.id}"

class ItemOrders(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    price = models.IntegerField()