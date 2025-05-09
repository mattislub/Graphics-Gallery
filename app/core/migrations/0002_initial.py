# Generated by Django 4.2.16 on 2024-11-26 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistimage',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.imageproduct'),
        ),
        migrations.AddField(
            model_name='wishlistimage',
            name='wishlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.wishlist'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='images',
            field=models.ManyToManyField(blank=True, through='core.WishlistImage', to='shop.imageproduct'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='core_user_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='core_user_permissions', to='auth.permission'),
        ),
    ]
