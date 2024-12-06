from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from plotly.offline import plot
from .models import StockMarketDrinkInstance
from .forms import StockMarketForm
from .pricing import pricer
import plotly.graph_objects as go
import django.utils.timezone as tz
import datetime
import pickle

def UpdatePricesView(request):
    succes = False

    if request.method == 'POST':
        form = StockMarketForm(request.POST)

        if form.is_valid():
            game = StockMarketDrinkInstance.objects.get()

            drink_names = []
            quantities_sold = []

            if int(form.data["Bier"]) > 0:
                game.Bier += int(form.data["Bier"])
                drink_names.append("Bier")
                quantities_sold.append(int(form.data["Bier"]))

            if int(form.data["Witte Wijn"]) > 0:
                #game.Witte_Wijn += int(form.data["Witte Wijn"])
                drink_names.append("Witte Wijn")
                quantities_sold.append(int(form.data["Witte Wijn"]))

            if int(form.data["Rode Wijn"]) > 0:
                #game.Rode_Wijn += int(form.data["Rode Wijn"])
                drink_names.append("Rode Wijn")
                quantities_sold.append(int(form.data["Rode Wijn"]))

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

            print("Hello")
            game.save()
            succes = True

        else:
            print(form.errors)
            succes = False
        
        new_form = StockMarketForm
        return render(request, "drink/inputview.html", {'form': new_form, 'succes': succes})
    else:
        form = StockMarketForm()

    return render(request, "drink/inputview.html", {'form': form, 'succes': succes})

def StockMarketGameView(request):
    game = StockMarketDrinkInstance.objects.get()
    price_holder = pricer.Pricer()
    price_holder.from_json(game.Data)

    figure = go.FigureWidget()
    config = {'displaylogo': False}
    # figure.update_layout(modebar={
    #         'orientation': 'v'}, 
    #     template="plotly_white")
    
    seconds = np.arange(0, price_holder.duration, 300)

    figure.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis = dict(
        tickmode = 'array',
        tickvals =  seconds)
    )
        
    bier_price = price_holder.drinks["Bier"].price_array
    bier_time = price_holder.drinks["Bier"].time_array

    witte_wijn_price = price_holder.drinks["Witte Wijn"].price_array
    witte_wijn_time = price_holder.drinks["Witte Wijn"].time_array

    rode_wijn_price = price_holder.drinks["Rode Wijn"].price_array
    rode_wijn_time = price_holder.drinks["Rode Wijn"].time_array

    jenever_price = price_holder.drinks["Jenever"].price_array
    jenever_time = price_holder.drinks["Jenever"].time_array

    salmari_price = price_holder.drinks["Salmari"].price_array
    salmari_time = price_holder.drinks["Salmari"].time_array

    rocketshot_price = price_holder.drinks["RocketShot"].price_array
    rocketshot_time = price_holder.drinks["RocketShot"].time_array
   
    fris_price = price_holder.drinks["Fris"].price_array
    fris_time = price_holder.drinks["Fris"].time_array


    figure.add_trace(go.Scatter(x=bier_time, y=bier_price, name="Pils", text=[""]*(len(bier_time)-1) + ["Pils"], mode='markers, lines, text'))
    figure.add_trace(go.Scatter(x=witte_wijn_time, y=witte_wijn_price, name="Witte Wijn", text=[""]*(len(witte_wijn_time)-1) + ["Witte Wijn"], mode='markers, lines, text'))
    figure.add_trace(go.Scatter(x=rode_wijn_time, y=rode_wijn_price, name="Rode Wijn",  text=[""]*(len(rode_wijn_time)-1) + ["Rode Wijn"], mode='markers, lines, text'))
    figure.add_trace(go.Scatter(x=jenever_time, y=jenever_price, name="Jenever",  text=[""]*(len(jenever_time)-1) + ["Jenever"], mode='markers, lines, text'))
    figure.add_trace(go.Scatter(x=salmari_time, y=salmari_price, name="Salmari",  text=[""]*(len(salmari_time)-1) + ["Salmari"], textposition="top center", mode='markers, lines, text'))
    figure.add_trace(go.Scatter(x=rocketshot_time, y=rocketshot_price, name="RocketShot",  text=[""]*(len(rocketshot_time)-1) + ["RocketShot"], mode='markers, lines, text'))
    figure.add_trace(go.Scatter(x=fris_time, y=fris_price, name="Fris", text=[""]*(len(fris_time)-1) + ["Fris"], textposition="bottom center", mode='markers, lines, text'))


    figure.update_xaxes(range=[0, 300])
    figure.update_yaxes(range=[0, 1.5])
    plt = plot(figure, output_type="div", config=config)



    return render(request, 'drink/drinkview.html', {'price_holder':price_holder, 'plot_div':plt, 'game': game})