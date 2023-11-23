from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.templatetags.static import static

import stripe
from django.shortcuts import render, redirect
from .models import Order


def tickets(request):
    return render(request, 'tickets.html')


# ensure this file locally contains test key during development
stripe.api_key = settings.STRIPE_SECRET_KEY


# this view processes data and redirects to stripe checkout
@csrf_exempt
def stripe_checkout(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        # creates valid stripe orders for our products
        stripe_order = [
            {
                "name": "Datorplats | D-LAN 2023",
                "description": "Datorplats (inkl. entré samtliga dagar) till D-LAN 2023. Bokad av " + data['fname'] + " " + data['lname'] + " - " + data['email'] + ".",
                "amount": 9000,
                "currency": "sek",
                "quantity": 0  # increment this if more tickets are purchased in one order
            },
            {
                "name": "Datorplats med datorskjuts | D-LAN 2023",
                "description": "Datorplats (inkl. entré samtliga dagar) till D-LAN 2023 samt datorskjuts till LANet. Bokad av " + data['fname'] + " " + data['lname'] + " - " + data['email'] + ".",
                "amount": 14000,
                "currency": "sek",
                "quantity": 0  # increment this if more tickets are purchased in one order
            }
        ]

        # remove ticket 2 if it's not used
        if data['main_ticket'] != "2" and data['secondary_ticket'] != "2":
            stripe_order.pop()

        # ensure right amount
        if data['main_ticket'] == "1":
            stripe_order[0]['quantity'] += 1
        if data['secondary_ticket'] == "1":
            stripe_order[0]['quantity'] += 1
        if data['main_ticket'] == "2":
            stripe_order[1]['quantity'] += 1
        if data['secondary_ticket'] == "2":
            stripe_order[1]['quantity'] += 1
        if (data['main_ticket'] == "2" and data['secondary_ticket'] == "2") or (data['main_ticket'] == "2" and data['secondary_ticket'] == "0"):
            del stripe_order[0]  # remove ticket 1 if it's not used

        try:
            # initiates a stripe session, passing in stripe_order
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=stripe_order,
                mode='payment',
                # TEST redirect url for successful payment
                success_url='http://localhost:8000/checkout?session_id={CHECKOUT_SESSION_ID}',
                # TEST redirect url for canceled payment
                cancel_url='http://localhost:8000/canceled?session_id={CHECKOUT_SESSION_ID}',

                # LIVE redirect url for successful payment
                # success_url='https://d-lan.se/checkout?session_id={CHECKOUT_SESSION_ID}',
                # LIVE redirect url for canceled payment
                # cancel_url='https://d-lan.se/canceled?session_id={CHECKOUT_SESSION_ID}',

                metadata={
                    'user_id': request.user.id,
                    'booking_data': json_data
                }
            )
            request.session['session_id'] = session.id

        # never got this to trigger, so may be room for improvement
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)})

        # return a JSON response with the Stripe session ID - not entirely sure how useful this is anymore
        return JsonResponse({'session_id': session.id})

    # main return, never seen it trigger
    return JsonResponse({'error': 'Invalid request method'})

# this view manages a successful payment and adds objects to database


def checkout(request):
    # throw 404 if no session id
    session_id = request.session.get('session_id', None)
    if not session_id:
        raise Http404()

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        booking_data = json.loads(session.metadata['booking_data'])

        # Check if an order with the same session_id already exists
        order = Order.objects.filter(session_id=session_id).first()

        # If no order is found, create a new one with data from session
        if order is None:
            order = Order.objects.create(
                fname=booking_data['fname'],
                lname=booking_data['lname'],
                liuid=booking_data['liuid'],
                email=booking_data['email'],
                main_ticket=booking_data['main_ticket'],
                secondary_ticket=booking_data['secondary_ticket'] or 'none',
                groupname=booking_data['groupname'] or 'none',
                phone1=booking_data['phone1'] or 'none',
                phone2=booking_data['phone2'] or 'none',
                order_successful=True,
                session_id=session_id  # Store the session_id in the object
            )
            order.save()  # saves the order to the database

            # used to render the order in the template
            order_details = [
                ('Ordernummer', order.order_number),
                ('Namn', f"{order.fname} {order.lname}"),
                ('E-post', order.email),
                ('LIU-ID', order.liuid),
                ('Din bokning', ''),
            ]

            order_sum = 0

            if (order.main_ticket == '1' or order.main_ticket == 1) and (order.secondary_ticket == '0' or order.secondary_ticket == 0):
                order_details.append(('Biljett 1', 'Datorplats'))
                order_sum = 90
            elif (order.main_ticket == '2' or order.main_ticket == 2) and (order.secondary_ticket == '0' or order.secondary_ticket == 0):
                order_details.append(
                    ('Biljett 1', 'Datorplats med datorskjuts'))
                order_details.append(
                    ('Kontaktnummer - Biljett 1', order.phone1))
                order_sum = 140
            elif (order.main_ticket == '1' or order.main_ticket == 1) and (order.secondary_ticket == '1' or order.secondary_ticket == 1):
                order_details.append(('Biljett 1', 'Datorplats'))
                order_details.append(('Biljett 2', 'Datorplats'))
                order_sum = 180
            elif (order.main_ticket == '1' or order.main_ticket == 1) and order.secondary_ticket == '2':
                order_details.append(('Biljett 1', 'Datorplats'))
                order_details.append(
                    ('Biljett 2', 'Datorplats med datorskjuts'))
                order_details.append(
                    ('Kontaktnummer - Biljett 2', order.phone2))
                order_sum = 230
            elif (order.main_ticket == '2' or order.main_ticket == 2) and (order.secondary_ticket == '2' or order.secondary_ticket == 2):
                order_details.append(
                    ('Biljett 1', 'Datorplats med datorskjuts'))
                order_details.append(
                    ('Kontaktnummer - Biljett 1', order.phone1))
                order_details.append(
                    ('Biljett 2', 'Datorplats med datorskjuts'))
                order_details.append(
                    ('Kontaktnummer - Biljett 2', order.phone2))
                order_sum = 280

            if order.groupname != 'none':
                order_details.append(('Gruppnamn', order.groupname))
            order_details.append(('Total kostnad', order_sum))

            # Prepare the HTML content of the email
            # More details to be included in the email can be added here
            context = {
                'order_details': order_details,
            }

            subject = f'D-LAN 2023 | Bokningsbekräftelse order {order.order_number}'
            recipient_list = [order.email]
            html_message = render_to_string(
                'email.html', context)
            plain_message = strip_tags(html_message)

            # Using None as the from_email in order to use alias
            send_mail(subject, plain_message, None,
                      recipient_list, html_message=html_message)
            order_details.pop()

            # as with many errors, I never got this to trigger
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)})

    # not this one either
    except Exception as e:
        return JsonResponse({'error': str(e)})

    # finally, render the page
    return render(request, 'checkout.html', {'order_details': order_details})


def canceled(request):
    # throw 404 if no session id
    session_id = request.session.get('session_id', None)
    if not session_id:
        raise Http404()

    return render(request, 'canceled.html')


# used by tickets.js to fetch stored liu-ids from database in order to ensure no duplicate entries
def check_liuid_exists(request):
    liuid = request.GET.get('liuid')
    exists = Order.objects.filter(liuid=liuid).exists()
    return JsonResponse({'exists': exists})


def receipt(request):
    return render(request, 'email.html')
