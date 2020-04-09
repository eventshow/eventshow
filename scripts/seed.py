import csv
import json
import random
import re


from random import randrange
from datetime import datetime, timedelta


from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core import management
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from faker import Faker

from events.models import Category

User = get_user_model()

INITIAL_DATA = []

CATEGORIES = ['TV', 'Juegos', 'Idiomas',
              'Aprender', 'Cocina', 'Deportes', 'Otros']
ENROLLMENT_STATUS = ['ACCEPTED', 'PENDING', 'REJECTED']
EVENT_PKS_THIS_YEAR = range(1, 151)
EVENT_PKS_FUTURE = range(151, 301)
PROFILE_IMAGE_FILES = [
    'https://i.imgur.com/DHM869r.png',
    'https://i.imgur.com/nPuyNCw.png',
    'https://i.imgur.com/zcvvJuz.png',
    'https://i.imgur.com/JoIFIzC.png',
    'https://i.imgur.com/q5WVAgm.png',
    'https://i.imgur.com/L8OjFOg.png',
    'https://i.imgur.com/V0Vx876.png',
    'https://i.imgur.com/yejzBet.png',
    'https://i.imgur.com/Gcw4VIN.png',
    'https://i.imgur.com/Kt7wGfh.png',
    'https://i.imgur.com/bq3Bb34.png',
    'https://i.imgur.com/smMeZJA.png',
]
EVENT_IMAGE_FILES = [
    'https://i.imgur.com/gIVamei.jpg',
    'https://i.imgur.com/x9GBkxo.jpg',
    'https://i.imgur.com/HZWQeck.jpg',
    'https://i.imgur.com/9TwAW0f.jpg',
    'https://i.imgur.com/WO6zhE1.jpg',
    'https://i.imgur.com/IaA01VF.jpg',
    'https://i.imgur.com/LKXjMBj.jpg',
    'https://i.imgur.com/ZmkYrp3.jpg',
]
FAKE = Faker('es_ES')
USER_PKS = range(1, 31)
TIMEZONE = '+0000'


def run():
    management.call_command('flush', interactive=False)

    seed_users()
    seed_profiles()
    seed_categories()
    seed_events(EVENT_PKS_THIS_YEAR)
    seed_events(EVENT_PKS_FUTURE, True)

    with open('initial_data/initial_data.json', 'w') as file:
        file.write(json.dumps(INITIAL_DATA, indent=4))

    management.call_command('loaddata', 'initial_data/initial_data')


def seed_users():
    for pk in USER_PKS:
        profile = FAKE.profile()
        names = profile['name'].split(' ')
        first_name = names[0]
        last_name = names[1]

        fields = {
            'password': make_password(profile['username']),
            'is_superuser': False,
            'username': profile['username'],
            'first_name': first_name,
            'last_name': last_name,
            'email': profile['mail'],
            'is_staff': False,
            'date_joined': now().strftime('%Y-%m-%d %H:%M:%S%z'),
        }
        user = {
            'pk': pk,
            'model': 'auth.User',
            'fields': fields
        }

        INITIAL_DATA.append(user)

    superuser = {
        'pk': USER_PKS[-1]+1,
        'model': 'auth.User',
        'fields': {
            'password': make_password('showman'),
            'is_superuser': True,
            'username': 'showman',
            'is_staff': True,
            'date_joined': now().strftime('%Y-%m-%d %H:%M:%S%z'),
        }
    }

    INITIAL_DATA.append(superuser)


def seed_profiles():
    for user_pk in USER_PKS:
        profile = {
            'pk': user_pk,
            'model': 'events.Profile',
            'fields': {
                'location': FAKE.city(),
                'picture': random.choice(PROFILE_IMAGE_FILES),
                'birthdate': '1980-01-01',
                'eventpoints': FAKE.random_int(1, 250),
                'token': get_random_string(length=8).upper(),
                'bio': FAKE.text(),
                'user': user_pk,
            }
        }

        INITIAL_DATA.append(profile)

    superuser_profile = {
        'pk': USER_PKS[-1]+1,
        'model': 'events.Profile',
        'fields': {
            'location': FAKE.city(),
            'picture': random.choice(PROFILE_IMAGE_FILES),
            'birthdate': '1980-01-01',
            'token': get_random_string(length=8).upper(),
            'bio': FAKE.text(),
            'user': USER_PKS[-1]+1
        }
    }

    INITIAL_DATA.append(superuser_profile)


def seed_categories():
    for ix, category in enumerate(CATEGORIES):
        fields = {
            'name': category,
        }
        category = {
            'pk': ix,
            'model': 'events.Category',
            'fields': fields
        }
        INITIAL_DATA.append(category)


def seed_events(event_pks, future=False):
    addresses = generate_addresses()
    for event_pk in event_pks:
        if future:
            start_day = FAKE.date_between(start_date='now',
                                          end_date='+2y')
        else:
            start_day = FAKE.date_between(start_date='-1y', end_date='now')
        category = CATEGORIES.index(random.choice(CATEGORIES))
        host = random.choice(USER_PKS)

        aux = list(USER_PKS).copy()
        aux.remove(host)
        enrollers = random.sample(set(aux), k=FAKE.random_int(1, len(aux)))
        splited_address = FAKE.address().split('\n')
        city = splited_address[1].split(',')[0]

        street = re.match(
            r'[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)* (((#|[nN][oO]\.?) ?)?(( ?[a-zA-Z\-]+)+)?)',
            splited_address[0]).group()

        # finds all digits in string and take the first which is the street number
        number = [int(s) for s in splited_address[0].split() if s.isdigit()][0]

        address = random.choice(addresses)
        city = address['localidad']
        residence = address['domicilio']
        street = re.match(
            r'[a-zA-ZÀ-ÖØ-öø-ÿ/]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*',
            residence).group()
        # finds all digits in string and take the first which is the street number
        aux = [int(s) for s in residence.split() if s.isdigit()]
        number = aux[0] if aux else 0
        price = FAKE.random_int(5, 20)

        min_start_time = datetime.strptime('09:00', '%H:%M')
        max_start_time = datetime.strptime('15:00', '%H:%M')
        min_end_time = datetime.strptime('16:00', '%H:%M')
        max_end_time = datetime.strptime('22:00', '%H:%M')

        start_time = random_time(min_start_time, max_start_time)
        end_time = random_time(min_end_time, max_end_time)
        capacity = FAKE.random_int(2, 20)

        fields = {
            'title': FAKE.word(),
            'description': FAKE.text(),
            'picture': random.choice(EVENT_IMAGE_FILES),
            'location_city': city,
            'location_street': street,
            'location_number': number,
            'capacity': capacity,
            'min_age': FAKE.random_int(16, 25),
            'lang': 'español',
            'pets': random.choice([False, True]),
            'parking_nearby': random.choice([False, True]),
            'extra_info': FAKE.sentence(),
            'start_day': start_day.strftime('%Y-%m-%d'),
            'start_time': start_time.strftime('%H:%M:%S%z'),
            'end_time': end_time.strftime('%H:%M:%S%z'),
            'price': price,
            'created_by': host,
            'category': category,
        }
        event = {
            'pk': event_pk,
            'model': 'events.Event',
            'fields': fields
        }

        seed_event_enrollments(event_pk, enrollers, host,
                               start_day, price, capacity)

        INITIAL_DATA.append(event)


def generate_addresses():
    data = []

    with open('initial_data/direcciones_dependencias_guardia_civil.csv', encoding='ISO-8859-1') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';', skipinitialspace=True)
        next(reader)
        for row in reader:
            new = {}
            if row['PROVINCIA'] == 'SEVILLA':
                new['localidad'] = row['LOCALIDAD'].title()
                new['domicilio'] = row['DOMICILIO'].title()

                data.append(new)
    return data


def seed_event_enrollments(event, enrollers, host, event_date, price, capacity):
    created_at = FAKE.date_time_between(
        start_date='-1y', end_date=event_date)
    updated_at = FAKE.date_time_between(
        start_date=created_at, end_date=event_date).strftime('%Y-%m-%d %H:%M:%S%z')
    created_at = created_at.strftime('%Y-%m-%d %H:%M:%S%z')

    ac = 0
    ix = 0
    num_enrollers = len(enrollers)

    attendees = []

    while ac < capacity and ix < num_enrollers:
        status = random.choice(ENROLLMENT_STATUS)
        enroller = enrollers[ix]

        fields = {
            'status': status,
            'created_at': created_at + TIMEZONE,
            'updated_at': updated_at + TIMEZONE,
            'created_by': enroller,
            'event': event,
        }
        enrollment = {
            'model': 'events.Enrollment',
            'fields': fields
        }

        seed_transaction(event, enroller, host, updated_at, price)
        if status == 'ACCEPTED':
            ac += 1
            if enroller not in attendees:
                attendees.append(enroller)

        INITIAL_DATA.append(enrollment)
        ix += 1

    if status == 'ACCEPTED' and event_date <= now().date():
        attendees_sublist = set(random.sample(
            attendees, k=FAKE.random_int(1, len(attendees))))
        seed_event_ratings(event, host, attendees_sublist, 'HOST', event_date)

        attendees_sublist = set(random.sample(
            attendees, k=FAKE.random_int(1, len(attendees))))
        seed_event_ratings(event, attendees_sublist, host,
                           'ATTENDEE', event_date)


def seed_event_ratings(event, revieweds, reviewers, on, event_date):
    created_at = FAKE.date_time_between(
        start_date=event_date, end_date='+1y').strftime('%Y-%m-%d %H:%M:%S%z')

    if on == 'HOST':
        for reviewer in reviewers:
            fields = {
                'score': FAKE.random_int(1, 5),
                'comment': FAKE.text(),
                'event': event,
                'on': on,
                'created_at': created_at + TIMEZONE,
                'updated_at': created_at + TIMEZONE,
                'created_by': reviewer,
                'reviewed': revieweds,
            }
            rating = {
                'model': 'events.Rating',
                'fields': fields
            }
            INITIAL_DATA.append(rating)
    else:
        for reviewed in revieweds:
            fields = {
                'score': FAKE.random_int(1, 5),
                'comment': FAKE.text(),
                'event': event,
                'on': on,
                'created_at': created_at + TIMEZONE,
                'updated_at': created_at + TIMEZONE,
                'created_by': reviewers,
                'reviewed': reviewed,
            }
            rating = {
                'model': 'events.Rating',
                'fields': fields
            }
            INITIAL_DATA.append(rating)


def seed_transaction(event, transmitter, recipient, created_at, amount):
    fields = {
        'amount': amount*100 + 1.15,
        'created_at': created_at + TIMEZONE,
        'updated_at': created_at + TIMEZONE,
        'event': event,
        'created_by': transmitter,
        'customer_id': 'cus_{0}'.format(get_random_string(length=14)),
        'is_paid_for': random.choice([True, False]),
        'recipient': recipient,
        'event': event
    }
    transaction = {
        'model': 'events.Transaction',
        'fields': fields
    }

    INITIAL_DATA.append(transaction)


def random_time(start, end):
    delta = end - start
    int_delta = delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
