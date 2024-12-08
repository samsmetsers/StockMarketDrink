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
import datetime
from django.http import HttpResponse
import json

def RemoveGame(request):
    game = StockMarketDrinkInstance.objects.get()
    game.delete()

    return redirect('/start/')

def StartView(request):
    game_in_progress = True
    if len(StockMarketDrinkInstance.objects.all()) > 0:
        game = StockMarketDrinkInstance.objects.get()

        price_holder = pricer.Pricer()
        price_holder.from_json(game.Data)

        if datetime.datetime.now().timestamp() - price_holder.start_time > 3600:
            game_in_progress = False
    
    print(game_in_progress)
    return render(request, 'drink/startview.html', {'in_progress': game_in_progress})

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
        form = StockMarketForm(request.POST)

        if form.is_valid():
            game = StockMarketDrinkInstance.objects.get()

            drink_names = []
            quantities_sold = []

            if form["BeursCrash"].value():
                game.BeursCrash = True
                game.save()
                succes = True
                new_form = StockMarketForm()
                return render(request, "drink/inputview.html", {'form': new_form, 'succes': succes})
            

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
    if not len(StockMarketDrinkInstance.objects.all()) > 0:
        game = StockMarketDrinkInstance()
        game.save()
    else:
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

    prices = [round(bier_price[-1], 2), round(witte_wijn_price[-1],2), round(rode_wijn_price[-1],2), round(jenever_price[-1],2),
               round(salmari_price[-1], 2), round(rocketshot_price[-1], 2), round(fris_price[-1],2)]

    max_price = np.max(prices)
    min_price = np.min(prices)

    min_layout =[max(0, (price_holder.current_time-price_holder.start_time)-900), (price_holder.current_time-price_holder.start_time)+900]
    max_layout = [min_price.item() - 0.05, max_price.item()+0.05]

    return render(request, 'drink/drinkview.html', {'game': game, "price_holder":price_holder, 'time': bier_time, 'bier': bier_price, 'witte_wijn': witte_wijn_price,
                                                    'rode_wijn': rode_wijn_price, 'jenever': jenever_price, 'salmari': salmari_price,
                                                    'rocketshot': rocketshot_price, 'fris': fris_price, 'min_layout':min_layout, 'max_layout':max_layout, 'prices':prices})

def ChartView(request):
    game = StockMarketDrinkInstance.objects.get()

    price_holder = pricer.Pricer()
    price_holder.from_json(game.Data)
    
    crash = False

    if game.BeursCrash:
        crash=True
        game.BeursCrash=False

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

    price_holder.current_time = datetime.datetime.now().timestamp()

    price_array = [[bier_price], [witte_wijn_price], [rode_wijn_price], [jenever_price], [salmari_price], [rocketshot_price], [fris_price]]
    
    prices = [round(bier_price, 2), round(witte_wijn_price, 2), round(rode_wijn_price, 2), round(jenever_price,2), round(salmari_price,2), round(rocketshot_price, 2), round(fris_price,2)]
    max_price = np.max(prices)
    min_price = np.min(prices)

    min_layout =[max(0, (price_holder.current_time-price_holder.start_time)-900), (price_holder.current_time-price_holder.start_time)+900]
    max_layout = [min_price.item() - 0.05, max_price.item()+0.1]

    game.Data = price_holder.to_json()
    game.save()
    response = HttpResponse(status=204, headers={'price_array': json.dumps(price_array), 'min_lay':json.dumps(min_layout), 'max_lay':json.dumps(max_layout), 'new_time':json.dumps(price_holder.current_time- price_holder.start_time), 'crash':json.dumps(crash), 'prices':json.dumps(prices)})
    return response