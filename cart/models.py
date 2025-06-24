from django.db import models
from grocery.models import GroceryItem

class Cart(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(GroceryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def is_valid(self):
        return self.item.is_available and self.item.stock >= self.quantity

    def status(self):
        if not self.item.is_available:
            return 'Unavailable'
        elif self.item.stock < self.quantity:
            return 'Out of stock'
        return 'Available'

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
