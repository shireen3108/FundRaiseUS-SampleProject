from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

from FundRaiseUs import settings
from .forms import CustomerCreationForm, FundraisersCreateForm, CustomerEditProfileForm, CustomerEditFundraisersForm, \
    DonationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Fundraiser, Donation
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


# register for customer
def CustomerSignUp(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))

        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = CustomerCreationForm()
        return render(request, 'registration/signup.html', {'form': form})


# method for editing customer profile
@login_required()
def edit_customerProfile(request):
    if request.method == 'POST':
        form = CustomerEditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('customer:profile_preview'))
        else:
            return render(request, 'Edit_CustomerProfile.html', {'form': form})
    else:
        form = CustomerEditProfileForm(instance=request.user)
        return render(request, 'Edit_CustomerProfile.html', {'form': form})


##Password
class PasswordResetFRUSEmailView(PasswordResetView):
    PasswordResetView.extra_email_context = {'fr_site_name': 'FundraiseUs'}


def HomeView(request):
    if request.method == 'GET':
        return render(request, 'home.html')


# list open fundraisers/home page
def ListFundraisers(request):
    totalfunds = {}
    loop_times = 3

    fundraiserList = Fundraiser.objects.filter(fundraiser_date__lte=datetime.now(), flag='Open')
    if request.user.is_authenticated is False:
        fundraiserList = fundraiserList[:loop_times]
    # fundraiserListDict = fundraiserList.values()
    get_donatedSum_fundRaiserList(fundraiserList, totalfunds)
    return render(request, 'fundraiser_list.html',
                  {'fundraiserList': fundraiserList, 'overallfunds_donated': totalfunds,
                   "loop_times": loop_times})


# calculate total funds for fundraiser list
def get_donatedSum_fundRaiserList(fundraiserList, totalfunds):
    for f in fundraiserList:
        get_donatedSum_fundRaiser(f, totalfunds)


# calculate total funds for a Fundraiser
def get_donatedSum_fundRaiser(f, totalfunds):
    listdonations = Donation.objects.filter(fundraiser_id=f.id)
    overallfunds = sum(listdonations.values_list('amount', flat=True))
    totalfunds.update({f: [overallfunds, overallfunds * 100 / f.goal]})


# Fundraiser on category medical
def FundraiserOnMedical(request):
    medicalFundraiserList = Fundraiser.objects.filter(cause_type='Medical', flag='Open')
    return render(request, 'FundraiserByCategory.html',
                  {'fundraiserList': medicalFundraiserList, 'cause_type': 'Medical'})


# Fundraiser on category Education
def FundraiserOnEducation(request):
    educationFundraiserList = Fundraiser.objects.filter(cause_type='Education', flag='Open')
    return render(request, 'FundraiserByCategory.html',
                  {'fundraiserList': educationFundraiserList, 'cause_type': 'Education'})


# Fundraiser on category non profit
def FundraiserOnNonProfit(request):
    nonprofitFundraiserList = Fundraiser.objects.filter(cause_type='Non-profit', flag='Open')
    return render(request, 'FundraiserByCategory.html',
                  {'fundraiserList': nonprofitFundraiserList, 'cause_type': 'Non-profit'})


# Fundraiser on category Emergency
def FundraiserOnEmergency(request):
    emergencyFundraiserList = Fundraiser.objects.filter(cause_type='Emergency', flag='Open')
    return render(request, 'FundraiserByCategory.html',
                  {'fundraiserList': emergencyFundraiserList, 'cause_type': 'Emergency'})


# about Fundraiser page
def AboutFundraiseUs(request):
    return render(request, 'Aboutus.html')


# Fundraiser resources tips and tricks
def Resources(request):
    return render(request, 'Resources.html')


# Fundraiser contact us page
def ContactUs(request):
    return render(request, 'ContactUs.html')


##################CUSTOMER ACTIONS###########

# method to create fundraiser
@login_required()
def FundraiserCreate(request):
    form = FundraisersCreateForm
    if request.method == "POST":
        form = FundraisersCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer_id = request.user
            instance.save()
            return redirect(reverse('customer:fundraiserslist'))
        else:
            return render(request, 'Fundraisers/create_fundraisers.html', {'form': form})
    else:
        return render(request, 'Fundraisers/create_fundraisers.html', {'form': form})


# method to list out the customer created fundraisers
@login_required()
def MyFundraiser(request):
    totalfunds = {}
    if request.method == 'GET':
        my_fundraisers = Fundraiser.objects.filter(customer_id=request.user, )
        get_donatedSum_fundRaiserList(my_fundraisers, totalfunds)
        return render(request, 'Fundraisers/My_fundraiser_list.html',
                      {'overallfunds_donated': totalfunds, 'my_fundraisers': my_fundraisers})


# method to edit customer create Fundraisers
@login_required()
def EditFundraiser(request, pk):
    Fundraisers = Fundraiser.objects.filter(id=pk).first()
    # if request.user != Fundraiser.customer_id:
    #     return HttpResponseForbidden()

    if request.method == 'POST':
        form = CustomerEditFundraisersForm(request.POST, request.FILES, instance=Fundraisers)
        if form.is_valid():
            instance = form.save(commit=False)
            totalfunds = {}
            get_donatedSum_fundRaiser(instance, totalfunds)
            if instance.goal <= totalfunds.get(instance)[0]:
                instance.flag = 'Completed'
            instance.save()
            form.save()
            return redirect(reverse('customer:customer_fundraiser'))
        else:
            return render(request, 'Fundraisers/Customer_editFundraiser.html', {'form': form})
    form = CustomerEditFundraisersForm(instance=Fundraisers)
    return render(request, 'Fundraisers/Customer_editFundraiser.html', {'form': form})


# method to delete customer posted Fundraisers
def DeleteFundraiser(request, pk):
    Fundraisers = Fundraiser.objects.filter(id=pk).first()
    Fundraisers.delete()
    totalfunds = {}
    my_fundraisers = Fundraiser.objects.filter(customer_id=request.user, )
    get_donatedSum_fundRaiserList(my_fundraisers, totalfunds)
    return render(request, 'Fundraisers/My_fundraiser_list.html',
                  {'overallfunds_donated': totalfunds, 'my_fundraisers': my_fundraisers})


# method to close customer posted Fundraisers
def CloseFundraiser(request, pk):
    Fundraisers = Fundraiser.objects.get(id=pk)
    Fundraisers.flag = 'Closed'
    Fundraisers.save()
    totalfunds = {}
    my_fundraisers = Fundraiser.objects.filter(customer_id=request.user, )
    get_donatedSum_fundRaiserList(my_fundraisers, totalfunds)
    return render(request, 'Fundraisers/My_fundraiser_list.html',
                  {'overallfunds_donated': totalfunds, 'my_fundraisers': my_fundraisers})


# method to check history Fundraisers
def HistoryFundraiser(request, pk):
    listdonations = Donation.objects.filter(fundraiser_id=pk, fundraiser_id__customer_id=request.user).order_by('-time')
    return render(request, 'Fundraisers/My_fundraiser_history.html', {'listdonations': listdonations})


# donate for a fundraiser by customer
def DonateFundraiser(request, pk):
    fundraiser = Fundraiser.objects.filter(id=pk).first()
    totalfunds = {}
    get_donatedSum_fundRaiser(fundraiser, totalfunds)
    fundraiser_donationsum = totalfunds.get(fundraiser)[0]
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                name_on_donation = request.user
            else:
                name_on_donation = None
            donation.customer_id = name_on_donation
            donation.fundraiser_id = fundraiser
            donation.time = datetime.now()
            donation.save()
            if fundraiser.goal <= fundraiser_donationsum + donation.amount:
                fundraiser.flag = 'Completed'
                fundraiser.save()
            return render(request, 'Customer_PaymentDone.html', {'donation': donation, })
        else:
            return render(request, 'Customer_Donate_forms.html', {'fundraiser': fundraiser, 'form': form, })
    else:
        form = DonationForm()
        return render(request, 'Customer_Donate_forms.html', {'fundraiser': fundraiser, 'form': form, })


# donation successful page
def DonationPaymentDone(request, pk):
    donation = Donation.objects.filter(id=pk).first()
    return render(request, 'Customer_PaymentDone.html', {'donation': donation, })


# check customer donations
@login_required()
def MyDonations(request):
    if request.method == 'GET':
        Donation_details = Donation.objects.filter(customer_id=request.user)
        return render(request, 'Fundraisers/My_Donations.html', {'donationslist': Donation_details})


# making pdf for the history of donations done on the customer fundraisers
def ReportFundraiser(request):
    my_fundraisers = Fundraiser.objects.filter(customer_id=request.user)
    donations = Donation.objects.all()
    context = {'my_fundraisers': my_fundraisers, 'donations': donations}
    pdfbytes = render_to_pdf('Fundraisers/FundraiserslistPDF.html', context)
    sendEmail(pdfbytes, request)

    totalfunds = {}
    my_fundraisers = Fundraiser.objects.filter(customer_id=request.user)
    get_donatedSum_fundRaiserList(my_fundraisers, totalfunds)
    return render(request, 'Fundraisers/My_fundraiser_list.html',
                  {'overallfunds_donated': totalfunds, 'my_fundraisers': my_fundraisers})


# method to make pdf
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.replace(u'\ufeff', '').encode("latin-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


# method to send email of the pdf
def sendEmail(pdf, request):
    username = request.user
    email = request.user.email
    subject = "Fundraiser - Donation History Report "
    content = {'uname': username, 'fr_site_name': 'FundraiseUs.com'}
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    message = EmailMultiAlternatives(subject=subject, body="Welcome..", from_email=from_email,
                                     to=[to_email], )
    html_template = get_template("Fundraisers/email_generation_fundraiser_donations.html").render(context=content)
    message.attach_alternative(html_template, "text/html")
    message.attach('MyFundraiserDonationsHistory.pdf', pdf, 'application/pdf')
    message.send()


# method to search for customer fundraiser
def FundraiserListSearch(request):
    pk = request.GET['fundraiser_search']
    fundraisersSearched = Fundraiser.objects.filter(~Q(customer_id=request.user), name__icontains=pk,
                                                    fundraiser_date__lte=datetime.now())
    totalfundsSearched = {}
    get_donatedSum_fundRaiserList(fundraisersSearched, totalfundsSearched)
    return render(request, 'fundraiser_list.html',
                  {'fundraiserListSearched': fundraisersSearched, 'searchString': pk,
                   'overallfunds_donated_searched': totalfundsSearched, })
