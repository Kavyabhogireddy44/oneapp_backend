from django.db import models

# Create your models here.

class Ticket(models.Model):
    # {'title': 'Damaged  Item',
    # 'details': 'jlnfrri  bre',
    # 'created_at': '25/05/2025',
    # 'closed_at': '27/05/2025',
    # 'status': 'Open',
    # 'order_id': 'Order2342323',
    # 'ticket_id': 'Order2342323',
    # 'item_list': [],
    # 'user_id': '1',
    # 'assigned_to': '',
    # 'comment': '',
    # 'connected_by': ''
    user=models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='tickets', blank=True, null=True)
    title=models.CharField(max_length=200, blank=True)
    details=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    closed_at=models.DateTimeField(blank=True, null=True)
    status=models.CharField(max_length=200,default='Open', blank=True)
    order_id=models.CharField(max_length=200, blank=True)
    ticket_id=models.CharField(max_length=200, blank=True)
    item_list=models.TextField(blank=True)
    assigned_to=models.CharField(max_length=200, blank=True)
    comment=models.TextField(blank=True)
    connected_by=models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.subject
