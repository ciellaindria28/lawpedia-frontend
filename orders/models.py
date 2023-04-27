from django.db import models

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    total_price = models.IntegerField()
    status_order = models.CharField(max_length=100)

    def __str__(self):
        return f"Order ID: {self.id}"