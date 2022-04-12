from django.views.generic import TemplateView
from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetConfirmView, \
        PasswordResetDoneView
from .views import *

app_name = 'customer'

urlpatterns = [
        path('', ListFundraisers,name='fundraiserslist'),
        path('signup/', CustomerSignUp, name='signup'),
        ######################PASSWORD RELATED########################
        path('change-password/', PasswordChangeView.as_view(), name='password_change'),
        path('change-password-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
        path('password-reset-form/', PasswordResetFRUSEmailView.as_view(), name='password_reset_form'),
        path('password-reset-done-form/', PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        #########################FUNDRAISERS GENERAL #########################
        path('fundraisers-list/',ListFundraisers,name='fundraiserslist'),
        path('about-us/',AboutFundraiseUs,name='aboutus'),
        path('resources/',Resources,name='resources'),
        path('contact-us/',ContactUs,name='contactus'),
        #####################PROFILE RELATED #########################
        path('profile_preview/', TemplateView.as_view(template_name='CustomerProfile_preview.html'),
             name='profile_preview'),
        path('edit_profile/', edit_customerProfile, name='edit_profile'),
        #####################FUNDRAISERS ON CATEGORIES #######################
        path('fundraisers-list-on-medical/', FundraiserOnMedical, name='medical'),
        path('fundraisers-list-on-non-profit/', FundraiserOnNonProfit, name='non_profit'),
        path('fundraisers-list-on-education/', FundraiserOnEducation, name='education'),
        path('fundraisers-list-on-emergency/', FundraiserOnEmergency, name='emergency'),
        #############################ACTIONS ON CUSTOMERS FUNDRAISERS###############
        path('fundraisers-create/',FundraiserCreate,name='create_fundraiser'),
        path('fundraisers-customerlist/',MyFundraiser,name='customer_fundraiser'),
        path('fundraisers-edit/<int:pk>',EditFundraiser,name='customerfundraisers_edit'),
        path('fundraisers-delete/<int:pk>', DeleteFundraiser, name='customerfundraisers_delete'),
        path('fundraisers-close/<int:pk>', CloseFundraiser, name='customerfundraisers_close'),
        path('fundraisers-history/<int:pk>', HistoryFundraiser, name='customerfundraisers_history'),
        path('fundraisers-report', ReportFundraiser, name='fundraisersPDFlist'),
        path('fundraisers-search', FundraiserListSearch, name='fundraiserslist_search'),
        ############################DONATION OF FUNDRAISER###########################
        path('fundraisers-donate/<int:pk>', DonateFundraiser, name='customer_donate'),
        path('fundraisers-payment/<int:pk>', DonationPaymentDone, name='customer_payment'),
        path('fundraisers-donationslist/', MyDonations, name='customer_donationslist'),

]
