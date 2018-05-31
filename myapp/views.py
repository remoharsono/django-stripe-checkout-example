from django.shortcuts import render
from myproject import settings
from myapp.models import Items

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def thank_you(request):
    return render(request, "thank_you.html")

def payment_form(request):
    context = { "stripe_key": settings.STRIPE_PUBLIC_KEY }
    return render(request, "payment_form.html", context)

@csrf_exempt
def checkout(request):

    new_item = Items(
        name = "Product Name Here",
        description  = "Product Description Here"

    if request.method == "POST":
        token    = request.POST.get("stripeToken")

    try:
        charge  = stripe.Charge.create(
            amount      = 325,
            currency    = "usd",
            source      = token,
            description = "The product charged to the user"
        )

        new_item.charge_id   = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        new_item.save()
        return redirect('thank_you_page')
