from django.db import models
import uuid
from .pricing import pricer
import pickle

# Create your models here.

class StockMarketDrinkInstance(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bier_verkocht = models.IntegerField(name="Bier", default=0)
    witte_wijn_verkocht = models.IntegerField(name="Witte Wijn", default=0)
    rode_wijn_verkocht = models.IntegerField(name="Rode Wijn", default=0)
    fris_verkocht = models.IntegerField(name="Fris", default=0)
    jenever_verkocht = models.IntegerField(name="Jenever", default=0)
    salmari_verkocht = models.IntegerField(name="Salmari", default=0)
    rocketshot_verkocht = models.IntegerField(name="RocketShot", default=0)
    beurscrash = models.BooleanField(name="BeursCrash", default=False)
    game_data = models.JSONField(name="Data", default=pricer.Pricer().to_json(), blank=True)
