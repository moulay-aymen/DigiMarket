from django.db import models
from django.conf import settings

class WithdrawalRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'En attente'),
        ('Approved', 'Approuvée'),
        ('Paid', 'Payée'),
        ('Rejected', 'Rejetée'),
    )
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2) # En DZD
    rip = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Retrait de {self.amount} DZD - {self.vendor.email} ({self.status})"