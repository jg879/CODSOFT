from django.shortcuts import render
from datetime import datetime
import math
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Min
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings

# Create your views here.
@login_required(login_url='/accounts/login')
def main(request):
    return render(request,"hotel.html")

@csrf_exempt
def search_hotels(request):
    city = request.GET.get('city')
    check_in_date = request.GET.get('check_in')
    check_out_date = request.GET.get('check_out')
    star_rating = int(request.GET.get('star_rating'))

    check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")

    hotels = Hotel.objects.filter(city__iexact=city, rating__gte=star_rating)
    number_of_days = (check_out_date - check_in_date).days
    try:
        max_price = hotels.aggregate(Max('price_per_night'))['price_per_night__max']
        min_price = hotels.aggregate(Min('price_per_night'))['price_per_night__min']
    except:
        max_price = 0
        min_price = 0

    return render(request, "hotel_search.html", {
        'hotels': hotels,
        'city': city,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        'star_rating': star_rating,
        'max_price': math.ceil(max_price / 100) * 100,
        'min_price': math.floor(min_price / 100) * 100,
        'days': number_of_days,
    })


def review_hotel(request):
    hotel_name = request.GET.get('hotel_name')
    hotel = Hotel.objects.get(name = hotel_name)
    rooms = Room.objects.filter(hotel__name__iexact=hotel_name)
    check_in_str = request.GET.get('check_in_date')
    check_out_str = request.GET.get('check_out_date')
    
    
    check_in_str = check_in_str.replace(', midnight', '').strip()
    check_out_str = check_out_str.replace(', midnight', '').strip()
    
    check_in_str = check_in_str.replace('Sept.', 'Sep.')
    check_out_str = check_out_str.replace('Sept.', 'Sep.')

    check_in_date = datetime.strptime(check_in_str, "%b. %d, %Y").date()
    check_out_date = datetime.strptime(check_out_str, "%b. %d, %Y").date()
    for room in rooms:
        room.check_in_date = check_in_date
        room.check_out_date = check_out_date
        room.save()
    
    return render(request,'bookhotel.html',{
        'rooms':rooms,
        'hotel':hotel,
    })

    
def hotel_payment(request):
    total_room_price = float(request.POST.get('total_room_price_with_tax'))
    user = request.user
    check_in_str = request.POST.get('check_in_date')
    check_out_str = request.POST.get('check_out_date')
    print("********")
    print(total_room_price)
    print("********")
    
    check_in_str = check_in_str.replace(', midnight', '').strip()
    check_out_str = check_out_str.replace(', midnight', '').strip()
    
    check_in_str = check_in_str.replace('Sept.', 'Sep.')
    check_out_str = check_out_str.replace('Sept.', 'Sep.')

    check_in_date = datetime.strptime(check_in_str, "%b. %d, %Y").date()
    check_out_date = datetime.strptime(check_out_str, "%b. %d, %Y").date()

    booking = Booking.objects.create(
            user=user,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_room_price,
        )
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    amount_in_paise = int(total_room_price * 100)
    order_currency = 'INR'
    payment = client.order.create(dict(amount=amount_in_paise, currency=order_currency, payment_capture=1))
    booking.razor_pay_order_id = payment['id']
    booking.save()

    return render(request,'hotelpayment.html',{
        'total_payment': total_room_price,
        'id': booking.razor_pay_order_id
    })

def success(request):
    order_id = request.GET.get('order_id')
    booking = Booking.objects.get(razor_pay_order_id = order_id)
    booking.is_paid = True
    booking.save()
    return render(request,'payment_success2.html')