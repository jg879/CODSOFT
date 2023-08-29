from datetime import timedelta, datetime
from .models import *
from tqdm import tqdm
from accounts.models import *
from .constant import FEE
import secrets
def get_number_of_lines(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def createWeekDays():
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for i,day in enumerate(days):
        Week.objects.create(number=i, name=day)

def addPlaces():
    file = open("./Data/airports.csv", "r")
    print("Adding Airports...")
    total = get_number_of_lines("./Data/airports.csv")
    for i, line in tqdm(enumerate(file), total=total):
        if i == 0:
            continue
        data = line.split(',')
        city = data[0].strip()
        airport = data[1].strip()
        code = data[2].strip()
        country = data[3].strip()
        try:
            Place.objects.create(city=city, airport=airport, code=code, country=country)
        except Exception as e:
            continue
    print("Done.\n")

def addDomesticFlights():
    file = open("./Data/domestic_flights.csv", "r")
    print("Adding Domestic Flights...")
    total = get_number_of_lines("./Data/domestic_flights.csv")
    for i, line in tqdm(enumerate(file), total=total):
        if i == 0:
            continue
        data = line.split(',')
        origin = data[1].strip()
        destination = data[2].strip()
        depart_time = datetime.strptime(data[3].strip(), "%H:%M:%S").time()
        depart_week = int(data[4].strip())
        duration = timedelta(hours=int(data[5].strip()[:2]), minutes=int(data[5].strip()[3:5]))
        arrive_time = datetime.strptime(data[6].strip(), "%H:%M:%S").time()
        arrive_week = int(data[7].strip())
        flight_no = data[8].strip()
        airline = data[10].strip()
        economy_fare = float(data[11].strip()) if data[11].strip() else 0.0
        business_fare = float(data[12].strip()) if data[12].strip() else 0.0
        first_fare = float(data[13].strip()) if data[13].strip() else 0.0

        try:
            a1 = Flight.objects.create(origin=Place.objects.get(code=origin), destination=Place.objects.get(code=destination), depart_time=depart_time , duration=duration, arrival_time=arrive_time, plane=flight_no, airline=airline, economy_fare=economy_fare, business_fare=business_fare, first_fare=first_fare)
            a1.depart_day.add(Week.objects.get(number=depart_week))
            a1.save()
        except Exception as e:
            print(e)
            return
    print("Done.\n")

def addInternationalFlights():
    file = open("./Data/international_flights.csv", "r")
    print("Adding International Flights...")
    total = get_number_of_lines("./Data/international_flights.csv")
    for i, line in tqdm(enumerate(file), total=total):
        if i == 0:
            continue
        data = line.split(',')
        origin = data[1].strip()
        destination = data[2].strip()
        depart_time = datetime.strptime(data[3].strip(), "%H:%M:%S").time()
        depart_week = int(data[4].strip())
        duration = timedelta(hours=int(data[5].strip()[:2]), minutes=int(data[5].strip()[3:5]))
        arrive_time = datetime.strptime(data[6].strip(), "%H:%M:%S").time()
        arrive_week = int(data[7].strip())
        flight_no = data[8].strip()
        airline = data[10].strip()
        economy_fare = float(data[11].strip()) if data[11].strip() else 0.0
        business_fare = float(data[12].strip()) if data[12].strip() else 0.0
        first_fare = float(data[13].strip()) if data[13].strip() else 0.0

        try:
            a1 = Flight.objects.create(origin=Place.objects.get(code=origin), destination=Place.objects.get(code=destination), depart_time=depart_time , duration=duration, arrival_time=arrive_time, plane=flight_no, airline=airline, economy_fare=economy_fare, business_fare=business_fare, first_fare=first_fare)
            a1.depart_day.add(Week.objects.get(number=depart_week))
            a1.save()
        except Exception as e:
            print(e)
            return
    print("Done.\n")


def createticket(user,passengers,passengerscount,flight1,flight_1date,flight_1class,countrycode,email,mobile):
    ticket = Ticket.objects.create()
    ticket.user = user
    ticket.ref_no = secrets.token_hex(3).upper()
    for passenger in passengers:
        ticket.passengers.add(passenger)
    ticket.flight = flight1
    ticket.flight_ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]))
    ###################
    flight1ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
    flight1adate = (flight1ddate + flight1.duration)
    ###################
    ticket.flight_adate = datetime(flight1adate.year,flight1adate.month,flight1adate.day)
    ffre = 0.0
    if flight_1class.lower() == 'first':
        ticket.flight_fare = flight1.first_fare*int(passengerscount)
        ffre = flight1.first_fare*int(passengerscount)
    elif flight_1class.lower() == 'business':
        ticket.flight_fare = flight1.business_fare*int(passengerscount)
        ffre = flight1.business_fare*int(passengerscount)
    else:
        ticket.flight_fare = flight1.economy_fare*int(passengerscount)
        ffre = flight1.economy_fare*int(passengerscount)
    ticket.other_charges = FEE                   
    ticket.total_fare = ffre+FEE+0.0                    
    ticket.seat_class = flight_1class.lower()
    ticket.status = 'PENDING'
    ticket.mobile = ('+'+countrycode+' '+mobile)
    ticket.email = email
    ticket.save()
    return ticket