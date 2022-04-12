from django.contrib import admin

from .models import Fundraiser, Donation, Customer


# listing down model details in admin page
class FundraiserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'goal', 'fundraiser_date', 'cause_type', 'for_whom_type', 'customer_id')


class CustomerAdmin(admin.ModelAdmin):
    list_display=('id', 'username', 'first_name', 'last_name', 'email', 'phone_num','city','state', 'zipcode')


class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'time','fundraiser_id','customer_id')


# Register your models here.
admin.site.register(Fundraiser, FundraiserAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Customer, CustomerAdmin)

