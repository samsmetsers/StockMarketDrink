from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from plotly.offline import plot
import plotly.io as pio
from .models import StockMarketDrinkInstance
from .forms import StockMarketForm
from .pricing import pricer
import plotly.graph_objects as go
import django.utils.timezone as tz
from django.http import HttpResponse
import json

def CalculatePriceView(request):
    if request.method == 'POST':
        print(request)
        form = StockMarketForm(request.POST)

        game = StockMarketDrinkInstance.objects.get()

        drink_names = []
        quantities_sold = []

        if int(form.data["Bier"]) > 0:
            drink_names.append("Bier")
            quantities_sold.append(int(form.data["Bier"]))

        if int(form.data["WitteWijn"]) > 0:
            drink_names.append("Witte Wijn")
            quantities_sold.append(int(form.data["WitteWijn"]))

        if int(form.data["RodeWijn"]) > 0:
            drink_names.append("Rode Wijn")
            quantities_sold.append(int(form.data["RodeWijn"]))

        if int(form.data["RocketShot"]) > 0:
            drink_names.append("RocketShot")
            quantities_sold.append(int(form.data["RocketShot"]))

        if int(form.data["Jenever"]) > 0:
            drink_names.append("Jenever")
            quantities_sold.append(int(form.data["Jenever"]))

        if int(form.data["Salmari"]) > 0:
            drink_names.append("Salmari")
            quantities_sold.append(int(form.data["Salmari"]))

        if int(form.data["Fris"]) > 0:
            drink_names.append("Fris")
            quantities_sold.append(int(form.data["Fris"]))

        price_holder = pricer.Pricer()
        price_holder.from_json(game.Data)

        total_price = 0.0

        for i in range(len(drink_names)):
            name = drink_names[i]
            quantity = quantities_sold[i]

            total_price += price_holder.drinks[name].price * quantity
        
        total_price = "%s"%(u"\N{euro sign}") + str(round(total_price, 2))
        return render(request, "drink/price.html", {'price': total_price})
    print("Something went wrong")
    return render(request, "drink/price.html", {'price': 0})



def UpdatePricesView(request):
    succes = False

    if request.method == 'POST':
        print("Nu posting")
        form = StockMarketForm(request.POST)

        if form.is_valid():
            game = StockMarketDrinkInstance.objects.get()

            drink_names = []
            quantities_sold = []

            if int(form.data["Bier"]) > 0:
                game.Bier += int(form.data["Bier"])
                drink_names.append("Bier")
                quantities_sold.append(int(form.data["Bier"]))

            if int(form.data["WitteWijn"]) > 0:
                game.WitteWijn += int(form.data["WitteWijn"])
                drink_names.append("Witte Wijn")
                quantities_sold.append(int(form.data["WitteWijn"]))

            if int(form.data["RodeWijn"]) > 0:
                game.RodeWijn += int(form.data["RodeWijn"])
                drink_names.append("Rode Wijn")
                quantities_sold.append(int(form.data["RodeWijn"]))

            if int(form.data["RocketShot"]) > 0:
                game.RocketShot += int(form.data["RocketShot"])
                drink_names.append("RocketShot")
                quantities_sold.append(int(form.data["RocketShot"]))

            if int(form.data["Jenever"]) > 0:
                game.Jenever += int(form.data["Jenever"])
                drink_names.append("Jenever")
                quantities_sold.append(int(form.data["Jenever"]))

            if int(form.data["Salmari"]) > 0:
                game.Salmari += int(form.data["Salmari"])
                drink_names.append("Salmari")
                quantities_sold.append(int(form.data["Salmari"]))

            if int(form.data["Fris"]) > 0:
                game.Fris += int(form.data["Fris"])
                drink_names.append("Fris")
                quantities_sold.append(int(form.data["Fris"]))

            price_holder = pricer.Pricer()
            price_holder.from_json(game.Data)

            price_holder.update_prices(names=drink_names, quantities=quantities_sold)
            game.Data = price_holder.to_json()
            game.save()
            succes = True

        else:
            print(form.errors)
            succes = False
        
        new_form = StockMarketForm()
        return render(request, "drink/inputview.html", {'form': new_form, 'succes': succes})
    else:
        form = StockMarketForm()

    return render(request, "drink/inputview.html", {'form': form, 'succes': succes})

def StockMarketGameView(request):
    game = StockMarketDrinkInstance.objects.get()
    price_holder = pricer.Pricer()
    price_holder.from_json(game.Data)

    bier_price = price_holder.drinks["Bier"].price_array
    bier_time = price_holder.drinks["Bier"].time_array

    witte_wijn_price = price_holder.drinks["Witte Wijn"].price_array

    rode_wijn_price = price_holder.drinks["Rode Wijn"].price_array

    jenever_price = price_holder.drinks["Jenever"].price_array

    salmari_price = price_holder.drinks["Salmari"].price_array

    rocketshot_price = price_holder.drinks["RocketShot"].price_array
   
    fris_price = price_holder.drinks["Fris"].price_array


    min_layout =[max(0, (price_holder.current_time-price_holder.start_time)-300), (price_holder.current_time-price_holder.start_time)+300]
    max_layout = [0.2, np.max(rode_wijn_price).item()+0.1]

    return render(request, 'drink/drinkview.html', {'game': game, "price_holder":price_holder, 'time': bier_time, 'bier': bier_price, 'witte_wijn': witte_wijn_price,
                                                    'rode_wijn': rode_wijn_price, 'jenever': jenever_price, 'salmari': salmari_price,
                                                    'rocketshot': rocketshot_price, 'fris': fris_price, 'min_layout':min_layout, 'max_layout':max_layout})

def ChartView(request):
    game = StockMarketDrinkInstance.objects.get()

    price_holder = pricer.Pricer()
    price_holder.from_json(game.Data)
    
    bier_price = price_holder.drinks["Bier"].price
    new_time = price_holder.drinks["Bier"].time_array[-1] + 5
    witte_wijn_price = price_holder.drinks["Witte Wijn"].price

    rode_wijn_price = price_holder.drinks["Rode Wijn"].price
    rode_wijn_price_array = price_holder.drinks["Rode Wijn"].price_array
    jenever_price = price_holder.drinks["Jenever"].price

    salmari_price = price_holder.drinks["Salmari"].price

    rocketshot_price = price_holder.drinks["RocketShot"].price
   
    fris_price = price_holder.drinks["Fris"].price

    price_holder.drinks["Bier"].price_array.append(bier_price)
    price_holder.drinks["Bier"].time_array.append(new_time)
    price_holder.drinks["Witte Wijn"].price_array.append(witte_wijn_price)
    price_holder.drinks["Rode Wijn"].price_array.append(rode_wijn_price)
    price_holder.drinks["Jenever"].price_array.append(jenever_price)
    price_holder.drinks["Salmari"].price_array.append(salmari_price)
    price_holder.drinks["RocketShot"].price_array.append(rocketshot_price)
    price_holder.drinks["Fris"].price_array.append(fris_price)

    price_holder.current_time += 5

    price_array = [[bier_price], [witte_wijn_price], [rode_wijn_price], [jenever_price], [salmari_price], [rocketshot_price], [fris_price]]

    min_layout =[max(0, (price_holder.current_time-price_holder.start_time)-300), (price_holder.current_time-price_holder.start_time)+300]
    max_layout = [0.2, np.max(rode_wijn_price_array).item()+0.1]

    game.Data = price_holder.to_json()
    game.save()
    response = HttpResponse(status=204, headers={'price_array': json.dumps(price_array), 'min_lay':json.dumps(min_layout), 'max_lay':json.dumps(max_layout)})
    return response