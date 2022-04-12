from django.db import models

# Create your models here.
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

PAYMENT_CHOICES = (
    ('Credit', 'Credit'),
    ('Debit', 'Debit')
)

CAUSES_CHOICES = (
    ('Education', 'Education'),
    ('Emergency', 'Emergency'),
    ('Medical', 'Medical'),
    ('Non-profit', 'Non-profit')
)

FOR_CHOICES = (
    ('Myself', 'Myself'),
    ('Friend', 'Friend'),
    ('Non-profit', 'Non-profit'),
)


# Customer model
class Customer(AbstractUser):
    country = models.CharField(max_length=30, blank=True, null=True, default='')
    city = models.CharField(max_length=30, blank=True, null=True, default='')
    state = models.CharField(max_length=30, blank=True, null=True, default='')
    zipcode = models.CharField('Zip Code', max_length=5, blank=True, null=True, default='')
    phone_num = models.CharField('Mobile Number', max_length=15, blank=True, null=True)
    email = models.EmailField(null=False, unique=True,
                              error_messages={'unique': 'A user with that email already exists.'})

    class Meta:
        verbose_name = "Customer"

# Fundraiser model
class Fundraiser(models.Model):
    name = models.CharField(max_length=75, blank=False)
    goal = models.DecimalField(max_digits=12, blank=False, decimal_places=2)
    fundraiser_date = models.DateTimeField('Start Date:', blank=False)
    description = models.CharField('About the fundraiser:', max_length=1000, null=True, blank=True)
    cause_type = models.CharField(choices=CAUSES_CHOICES, max_length=128)
    for_whom_type = models.CharField('Raising Fundraiser for WHOM:', choices=FOR_CHOICES, max_length=128)
    image = models.ImageField(upload_to="fundraisers/images", null=True)
    flag = models.CharField(default='Open', null=True,  max_length=10,) #open, close, completed,
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='fundraiser_customer_id')

    class Meta:
        verbose_name = "Fundraiser"

    def __str__(self):
        return self.name

# donation model
class Donation(models.Model):
    amount = models.DecimalField(max_digits=5, blank=False, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)
    method = models.CharField(choices=PAYMENT_CHOICES, max_length=128)
    comment = models.CharField(max_length=500, null=True, blank=True)
    fundraiser_id = models.ForeignKey(Fundraiser, on_delete=models.CASCADE, related_name='donation_fundraiser_id')
    customer_id = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE, related_name='donation_customer_id')

    class Meta:
        verbose_name = "Donation"

    def __str__(self):
        return self.fundraiser_id.name + ' for ' + str(self.amount)
        #+ ' by ' + self.customer_id.username
