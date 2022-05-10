from hashlib import new
from multiprocessing import Event
from unittest import result
from django.shortcuts import redirect, render
from matplotlib import ticker
from .models import Acao
from .utils import get_plot
from datetime import datetime
import requests
import json
import matplotlib.pyplot as plt
import re

def index(request, usuario):

    global symbol 
    symbol = request.POST.get('nomeAcao')
    global symbolDelete
    symbolDelete = request.POST.get('deleteAcao')
    global symbolGrafico
    symbolGrafico = request.POST.get('visualizaGrafico') or 'petr4'
    acoes = Acao.objects.all()
    logout = request.POST.get('logout')
    
    datas_unix = []

    dados_plot = []
    datas_valores = []

    if symbol:

        def recebeDadosApi():
        
            url = "https://brapi.ga/api/quote/" + symbol + "?interval=1d&range=1mo"
            response = requests.request("GET", url)
            data = json.loads(response.text)

            for x in data['results'][0]['historicalDataPrice']:
                if  x['open'] != 0:
                    dados_plot.append(x['open'])
                    datas_unix.append(x['date'])

            return data

        new_data = recebeDadosApi()    
        
        for y in datas_unix:
            datas_valores.append(datetime.utcfromtimestamp(y).strftime('%d-%m-%Y'))
        
        if 'nomeAcao' in request.POST:
            if not (Acao.objects.filter(ticker=symbol.upper())):
                
                queryset_nome = new_data['results'][0]['longName']
                queryset_ticker = new_data['results'][0]['symbol']
                preco = new_data['results'][0]['regularMarketPrice']

                AddAcao = Acao(ticker=queryset_ticker, nome=queryset_nome, preco=preco)
                AddAcao.save()
        
        return render(request,"web/home.html", {
            'nome': new_data['results'][0]['longName'],
            'ticker': new_data['results'][0]['symbol'],
            'preco': new_data['results'][0]['regularMarketPrice'],
            'acoes': acoes,
            'usuario': usuario,
            'chart': get_plot(datas_valores, dados_plot)
        })

    elif symbolDelete:
        if 'deleteAcao' in request.POST:
                deleteUrl = symbolDelete
                deleteAcao = Acao.objects.filter(ticker= deleteUrl.upper())
                deleteAcao.delete()

        return render(request,"web/home.html", {
            'acoes': acoes,
            'usuario': usuario,
            'chart': get_plot(datas_valores, dados_plot)
        })
    
    elif symbolGrafico:

        def recebeDadosApi():
        
            url = "https://brapi.ga/api/quote/" + symbolGrafico + "?interval=1d&range=1mo"
            response = requests.request("GET", url)
            data = json.loads(response.text)

            for x in data['results'][0]['historicalDataPrice']:
                if  x['open'] != 0:
                    dados_plot.append(x['open'])
                    datas_unix.append(x['date'])

            return data

        new_data = recebeDadosApi()

        for y in datas_unix:
            datas_valores.append(datetime.utcfromtimestamp(y).strftime('%d-%m-%Y'))

        return render(request,"web/home.html", {
            'acoes': acoes,
            'ticker': new_data['results'][0]['symbol'],
            'usuario': usuario,
            'chart': get_plot(datas_valores, dados_plot)
        })
    
    elif logout:
        return redirect('login')

    else:

        def recebeDadosApi():
        
            url = "https://brapi.ga/api/quote/" + symbolGrafico + "?interval=1d&range=1mo"
            response = requests.request("GET", url)
            data = json.loads(response.text)

            for x in data['results'][0]['historicalDataPrice']:
                if  x['open'] != 0:
                    dados_plot.append(x['open'])
                    datas_unix.append(x['date'])

            return data

        new_data = recebeDadosApi()

        for y in datas_unix:
            datas_valores.append(datetime.utcfromtimestamp(y).strftime('%d-%m-%Y'))

        return render(request,"web/home.html", {
            'acoes': acoes,
            'usuario': usuario,
            'chart': get_plot(datas_valores, dados_plot)
        })

def login(request):

    user = request.POST.get('usuario')

    if request.method == 'POST':
        return redirect('index', usuario=user)

    return render(request, "web/login.html")