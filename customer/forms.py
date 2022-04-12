from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from .models import Customer, Fundraiser, Donation
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, UserChangeForm


# create customer form
class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = (
        "username", "first_name", "last_name", "email", "phone_num", "country", "city", "state", "zipcode")


# create fundraiser form
class FundraisersCreateForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ("name", "goal", "fundraiser_date", "description", "cause_type", "for_whom_type","image")
        widgets={
            'fundraiser_date': DateTimePickerInput,
        }


# edit customer details form
class CustomerEditProfileForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "<span class='text-white'>Click here to change your password </span>"
            "<u><a class='text-white' href=\"../password_change/\">Change My Password</a></u>."
        ),
    )
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "email", "phone_num", "country", "state", "city", "zipcode")

    def __init__(self, *args, **kwargs):
        super(CustomerEditProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True


# form for editing customers fundraisers
class CustomerEditFundraisersForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ("name", "goal", "fundraiser_date", "description", "image", "cause_type","for_whom_type")
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'tell about the Fundraiser..', 'rows': 5, }),
        }


# donations form
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ("amount", "method","comment")