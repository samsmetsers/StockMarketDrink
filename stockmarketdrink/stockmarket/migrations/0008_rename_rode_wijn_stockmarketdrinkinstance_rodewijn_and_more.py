# Generated by Django 5.1.1 on 2024-12-07 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmarket', '0007_alter_stockmarketdrinkinstance_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockmarketdrinkinstance',
            old_name='Rode Wijn',
            new_name='RodeWijn',
        ),
        migrations.RenameField(
            model_name='stockmarketdrinkinstance',
            old_name='Witte Wijn',
            new_name='WitteWijn',
        ),
        migrations.AddField(
            model_name='stockmarketdrinkinstance',
            name='Changed',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='stockmarketdrinkinstance',
            name='Data',
            field=models.JSONField(blank=True, default={'Bier1': 'Bier', 'Bier2': 0.3125, 'Bier3': 480, 'Bier4': 0.3125, 'Bier5': [0.3125], 'Bier6': [0], 'Bier7': 1, 'Bier8': 480, 'Fris1': 'Fris', 'Fris2': 0.5, 'Fris3': 144, 'Fris4': 0.5, 'Fris5': [0.5], 'Fris6': [0], 'Fris7': 1, 'Fris8': 144, 'Jenever1': 'Jenever', 'Jenever2': 0.5, 'Jenever3': 130, 'Jenever4': 0.5, 'Jenever5': [0.5], 'Jenever6': [0], 'Jenever7': 1, 'Jenever8': 130, 'RocketShot1': 'RocketShot', 'RocketShot2': 0.63, 'RocketShot3': 90, 'RocketShot4': 0.63, 'RocketShot5': [0.63], 'RocketShot6': [0], 'RocketShot7': 1, 'RocketShot8': 90, 'Rode Wijn1': 'Rode Wijn', 'Rode Wijn2': 0.88, 'Rode Wijn3': 60, 'Rode Wijn4': 0.88, 'Rode Wijn5': [0.88], 'Rode Wijn6': [0], 'Rode Wijn7': 1, 'Rode Wijn8': 60, 'Salmari1': 'Salmari', 'Salmari2': 0.7, 'Salmari3': 90, 'Salmari4': 0.7, 'Salmari5': [0.7], 'Salmari6': [0], 'Salmari7': 1, 'Salmari8': 90, 'Witte Wijn1': 'Witte Wijn', 'Witte Wijn2': 0.7, 'Witte Wijn3': 60, 'Witte Wijn4': 0.7, 'Witte Wijn5': [0.7], 'Witte Wijn6': [0], 'Witte Wijn7': 1, 'Witte Wijn8': 60, 'current_time': 1733575891.637924, 'duration': 2784, 'revenue': 0, 'start_time': 1733575891.637924, 'total_cost': 501.5}),
        ),
    ]