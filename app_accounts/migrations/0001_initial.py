# Generated by Django 2.2.1 on 2019-05-18 19:53

import app_accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_base', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_base.Course')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_base.CourseSession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='درباره من')),
                ('_education', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'دانش\u200cآموزش'), (2, 'دیپلم'), (3, 'دانشجو'), (4, 'کاردانی'), (5, 'کارشناسی'), (6, 'کارشناسی ارشد'), (7, 'دکتری')], null=True, validators=[app_accounts.models.check_education], verbose_name='تحصیلات')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='شماره همراه')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=app_accounts.models.avatar_path)),
                ('show_resume', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
