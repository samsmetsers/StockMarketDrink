from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from plotly.offline import plot
from .models import StockMarketDrinkInstance
from .pricing import pricer
import plotly.graph_objects as go
import django.utils.timezone as tz
import datetime
import pickle


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

    figure.add_trace(go.Scatter(x=bier_time, y=bier_price, name="Pils", mode='markers'))
    figure.add_trace(go.Scatter(x=witte_wijn_time, y=witte_wijn_price, name="Witte Wijn", mode='markers'))
    figure.update_xaxes(range=[0, price_holder.duration])
    figure.update_yaxes(range=[0, 3.0])
    plt = plot(figure, output_type="div", config=config)



    return render(request, 'drink/drinkview.html', {'price_holder':price_holder, 'plot_div':plt, 'game': game})