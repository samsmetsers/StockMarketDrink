from django.forms import ModelForm
from .models import StockMarketDrinkInstance

class StockMarketForm(ModelForm):
    class Meta:
        model = StockMarketDrinkInstance
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
