# Generated by Django 3.0.4 on 2020-04-06 15:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import events.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Updated at')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('picture', models.URLField(verbose_name='Picture url')),
                ('location_city', models.CharField(max_length=250, verbose_name='City')),
                ('location_street', models.CharField(max_length=250, verbose_name='Street')),
                ('location_number', models.PositiveIntegerField(verbose_name='Street number')),
                ('start_day', models.DateField(verbose_name='Starting day')),
                ('start_time', models.TimeField(verbose_name='Starting time')),
                ('end_time', models.TimeField(verbose_name='Ending time')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price')),
                ('capacity', models.PositiveSmallIntegerField(verbose_name='Capacity')),
                ('min_age', models.PositiveSmallIntegerField(verbose_name='Minimum age')),
                ('lang', models.CharField(max_length=250, verbose_name='Language')),
                ('pets', models.BooleanField(verbose_name='Pets allowed')),
                ('parking_nearby', models.BooleanField(verbose_name='Parking nearby')),
                ('extra_info', models.TextField(blank=True, null=True, verbose_name='Extra info for the attendee')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_events', to='events.Category')),
                ('created_by', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='host_events', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_event_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['price', '-start_day', '-title'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('amount', models.PositiveIntegerField(verbose_name='Amount')),
                ('concept', models.CharField(max_length=140, verbose_name='Concept')),
                ('created_by', models.ForeignKey(on_delete=models.SET(events.models.get_sentinel_user), related_name='transmitter_transaction', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_transaction', to='events.Event')),
                ('recipient', models.ForeignKey(on_delete=models.SET(events.models.get_sentinel_user), related_name='recipient_transaction', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_transaction_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Updated at')),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Score')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('on', models.CharField(choices=[('ATTENDEE', 'attendee'), ('HOST', 'host')], max_length=8, verbose_name='On')),
                ('created_by', models.ForeignKey(on_delete=models.SET(events.models.get_sentinel_user), related_name='reviewer_ratings', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='events.Event')),
                ('reviewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_ratings', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_rating_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
                'ordering': ['-score'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=250, null=True, verbose_name='Location')),
                ('picture', models.URLField(blank=True, default='https://i.imgur.com/Kt7wGfh.png', null=True, verbose_name='Picture url')),
                ('birthdate', models.DateField(verbose_name='Birthdate')),
                ('token', models.CharField(editable=False, max_length=8, verbose_name='Personal token')),
                ('eventpoints', models.PositiveIntegerField(default=0, editable=False, verbose_name='Eventpoints')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Updated at')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_message_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_message_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['created_at'],
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='Updated at')),
                ('status', models.CharField(choices=[('ACCEPTED', 'Accepted'), ('PENDING', 'Pending'), ('REJECTED', 'Rejected')], default='PENDING', max_length=8, verbose_name='Status')),
                ('created_by', models.ForeignKey(on_delete=models.SET(events.models.get_sentinel_user), related_name='attendee_enrollments', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_enrollments', to='events.Event')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_enrollment_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Enrollment',
                'verbose_name_plural': 'Enrollments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='events_cate_name_a3fb74_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['-location_city', '-location_street', '-location_number', 'start_day', 'end_time', 'start_time', 'price', 'category'], name='events_even_locatio_1c6d68_idx'),
        ),
    ]
