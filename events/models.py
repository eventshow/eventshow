import pytz
import uuid

from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.timezone import now


from core.models import Common

# Create your models here.


User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]


class Profile(models.Model):
    EVENTPOINT_VALUE = 0.005
    TOKEN_LENGTH = 8

    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)
    location = models.CharField(
        'Location', max_length=250, blank=True, null=True)
    picture = models.URLField('Picture url', blank=True, null=True)
    birthdate = models.DateField('Birthdate')
    token = models.CharField('Personal token', max_length=8, editable=False)
    eventpoints = models.PositiveIntegerField(
        'Eventpoints', default=0, editable=False)
    bio = models.TextField('Bio', blank=True, null=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    @property
    def avg_attendee_score(self):
        return self.user.reviewed_ratings.filter(on='ATTENDEE').aggregate(
            models.Avg('score'))['score__avg']

    @property
    def avg_host_score(self):
        return self.user.reviewed_ratings.filter(on='HOST').aggregate(
            models.Avg('score'))['score__avg']

    @property
    def discount(self):
        return self.eventpoints * self.EVENTPOINT_VALUE

    def save(self, *args, **kwargs):
        self.token = get_random_string(length=self.TOKEN_LENGTH).upper()
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username + ' profile'


class Category(models.Model):
    name = models.CharField('Category', max_length=250)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        ordering = ['-name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Event(Common):
    UTC = pytz.UTC

    title = models.CharField('Title', max_length=250)
    description = models.TextField('Description')
    picture = models.URLField('Picture url')

    location_city = models.CharField('City', max_length=250)
    location_street = models.CharField('Street', max_length=250)
    location_number = models.PositiveIntegerField('Street number')

    start_day = models.DateField('Starting day')
    start_time = models.TimeField('Starting time')
    end_time = models.TimeField('Ending time')
    price = models.DecimalField(
        'Price', max_digits=6, decimal_places=2)
    capacity = models.PositiveSmallIntegerField('Capacity')
    min_age = models.PositiveSmallIntegerField('Minimum age')
    lang = models.CharField('Language', max_length=250)
    pets = models.BooleanField('Pets allowed')
    parking_nearby = models.BooleanField('Parking nearby')
    extra_info = models.TextField(
        'Extra info for the attendee', blank=True, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='host_events', default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='category_events', null=True)

    class Meta:
        indexes = [models.Index(
            fields=['-location_city', '-location_street', '-location_number', 'start_day', 'end_time', 'start_time',
                    'price',
                    'category'])]
        ordering = ['price', '-start_day', '-title']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    @property
    def duration(self):
        end_time = datetime.combine(
            date.today(), self.end_time)
        start_time = datetime.combine(
            date.today(), self.start_time)
        duration = (end_time - start_time).seconds / 60

        return int(duration)

    @property
    def has_finished(self):
        end_datetime = datetime.combine(self.start_day, self.end_time)
        return self.UTC.localize(end_datetime) <= now()

    @property
    def has_started(self):
        start_datetime = datetime.combine(self.start_day, self.start_time)
        return self.UTC.localize(start_datetime) >= now()

    @property
    def location(self):
        return ' '.join([self.location_city, self.location_street, str(self.location_number)])

    @property
    def location(self):
        return ' '.join([self.location_city, self.location_street, str(self.location_number)])

    @property
    def g_location(self):
        aux = ','.join([self.location_street, self.location_city])
        return '+'.join([str(self.location_number), aux])

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Enrollment(Common):
    STATUS_CHOICES = (
        ('ACCEPTED', 'Accepted'),
        ('PENDING', 'Pending'),
        ('REJECTED', 'Rejected')
    )

    status = models.CharField('Status', max_length=8,
                              choices=STATUS_CHOICES, default='PENDING')

    created_by = models.ForeignKey(
        User, on_delete=models.SET(get_sentinel_user), related_name='attendee_enrollments')
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='event_enrollments')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return self.created_by.username + ' on ' + self.event.title + ', status ' + self.status


class Rating(Common):
    ON_CHOICES = (
        ('ATTENDEE', 'attendee'),
        ('HOST', 'host')
    )

    score = models.PositiveSmallIntegerField(
        'Score', validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField('Comment', blank=True, null=True)
    on = models.CharField('On', max_length=8, choices=ON_CHOICES)

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='ratings')
    created_by = models.ForeignKey(
        User, on_delete=models.SET(get_sentinel_user), related_name='reviewer_ratings')
    reviewed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewed_ratings')

    class Meta:
        ordering = ['-score']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    """ def save(self, *args, **kwargs):
        # self.full_clean()
        return super().save(*args, **kwargs) """

    """ def clean(self):
        if self.created_by == self.reviewed:
            raise ValidationError('It is not possible to rate yourself') """

    def __str__(self):
        return '{0} on {1}'.format(self.score, self.reviewed)

    def get_absolute_url(self):
        return reverse('rating-detail', kwargs={'pk': self.pk})


class Transaction(Common):
    id = models.UUIDField('Id', primary_key=True,
                          default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET(
        get_sentinel_user), related_name='transmitter_transaction')
    recipient = models.ForeignKey(User, on_delete=models.SET(
        get_sentinel_user), related_name='recipient_transaction')
    amount = models.PositiveIntegerField('Amount')
    concept = models.CharField('Concept', max_length=140)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return str(self.id)
