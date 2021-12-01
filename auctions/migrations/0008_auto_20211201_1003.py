# Generated by Django 3.2.9 on 2021-12-01 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20211201_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='auction',
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='comment',
            name='auction',
        ),
        migrations.AddField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auction'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='auction',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='auctions.auction'),
            preserve_default=False,
        ),
    ]