from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpRequest
from .form import PaymentForm
from django.conf import settings
from .models import Payments
from django.contrib import messages

# Create your views here.
def initiate_payments(request:HttpRequest) ->HttpResponse:
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        
        if payment_form.is_valid():
            payment = payment_form.save()
            context = {

                'payment':payment,
                'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
            }
            return render(request, 'base/make_payment.html', context)
        
    payment_form = PaymentForm()
    context = {
        'payment_form':payment_form
    }
    return render(request, 'base/initiate_payment.html', context )

def verify_payment(request : HttpRequest,ref:str) ->HttpResponse:

    payment = get_object_or_404(Payments, ref = ref)
    verified = payment.verify_pay()

    if verified:
        messages.success(request, 'Verification Successful')

    else:
        messages.error(request, 'Verification Failed')

    return redirect('initiate_payments')



