# Generated by Django 5.1.1 on 2024-12-17 11:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_ticket_is_available'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Short title or headline for the testimonial.', max_length=255)),
                ('content', models.TextField(help_text='The main testimonial content.')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False, help_text='Admin approval for display.')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]
