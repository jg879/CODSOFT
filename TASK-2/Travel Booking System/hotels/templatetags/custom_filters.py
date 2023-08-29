from django import template

register = template.Library()

@register.filter
def calculate_net_price(room, hotel):
    number_of_days = (room.check_out_date - room.check_in_date).days
    return number_of_days*(room.room_charge + hotel.price_per_night)
