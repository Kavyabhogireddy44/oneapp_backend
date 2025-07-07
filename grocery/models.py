from django.db import models

# Create your models here.
# {
# "id": "uuid-or-item-id",
# "name": "Banana",
# "category": "Fruits",
# "description": "Fresh organic bananas",
# "brand": "Dole",
# "quantity": {
# "amount": 6,
# "unit": "pieces"
# },
# "price": {
# "mrp": 199,
# "ourPrice": "148"
# "currency": "INR"
# },
# "discount": {
# "amount": 0.5,
# "type": "flat", // or "percentage"
# "valid_until": "2025-06-30"
# },
# "stock": 150,
# "image_url": "https://example.com/images/banana.jpg",
# "is_available": true,
# "rating": 4.5,
# "created_at": "2025-06-14T10:00:00Z",
# "updated_at": "2025-06-14T12:00:00Z",
# "tags": ["fresh", "organic", "fruit", "snack"]
# }
class GroceryItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.JSONField(default=dict)  # e.g., {"amount": 6, "unit": "pieces"}
    price = models.JSONField(default=dict)  # e.g., {"mrp": 199, "ourPrice": 148, "currency": "INR"}
    discount = models.JSONField(default=dict)  # e.g., {"amount": 0.5, "type": "flat", "valid_until": "2025-06-30"}
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    category_image = models.URLField(max_length=500, blank=True, null=True)  # Optional image for the category
    # category_tag make array or list

    category_tag = models.JSONField(default=list)  # e.g., ["fruits", "snacks", "healthy"]
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.JSONField(default=list)  # e.g., ["fresh", "organic", "fruit", "snack"]

    def __str__(self):
        return self.name