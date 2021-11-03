from django.http.request import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout

import numpy as np
from matplotlib import pyplot as plt
import math
import io
import base64
import re
from urllib.parse import urlencode

def signupview(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_set = get_user_model().objects.filter(username=username)
        duplicate = False

        for user in user_set:
            duplicate = True

        if duplicate:
            return render(request, "signup.html", {"error" : "既に同じ名前のユーザーが存在します"})
        else:
            get_user_model().objects.create_user(username, "", password)
            return redirect("login")

def loginview(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("tiling", type="line")
        else:
            return render(request, "login.html", {"error" : "ログインに失敗しました"})

def logoutview(request):
    logout(request)
    return redirect("login")

def tilingview(request, type):
    if request.GET.get("error"):
        error = request.GET.get("error")
    else:
        error = ""
    return render(request, "tiling.html", {"type" : type, "error" : error})

def displayview(request, type):
    validation = True
    integer = re.compile(r"^[+]?\d+$")
    decimal = re.compile(r"^[+-]?\d+(?:\.\d+)?$")

    if type == "line":
        if decimal.search(request.POST["horizontal_tilt"]):
            horizontal_tilt = float(request.POST["horizontal_tilt"])
        else:
            validation = False

        if decimal.search(request.POST["horizontal_interval"]):    
            horizontal_interval = float(request.POST["horizontal_interval"])
        else:
            validation = False
        
        if decimal.search(request.POST["vertical_tilt"]):
            vertical_tilt = float(request.POST["vertical_tilt"])
        else:
            validation = False
        
        if decimal.search(request.POST["vertical_interval"]):
            vertical_interval = float(request.POST["vertical_interval"])
        else:
            validation = False
        
        if integer.search(request.POST["horizontal_max"]):
            horizontal_max = int(request.POST["horizontal_max"])
        else:
            validation = False
        
        if integer.search(request.POST["vertical_max"]):
            vertical_max = int(request.POST["vertical_max"])
        else:
            validation = False
        
        if not validation:
            redirect_url = reverse("tiling", kwargs={"type" : "line"})
            parameters = urlencode({"error" : "値を正しく入力してください"})
            url = f"{redirect_url}?{parameters}"
            return redirect(url)

        for n in range(0, horizontal_max+1):
            for m in range(0, vertical_max+1):
                x_1 = np.linspace(m*vertical_interval, (m+1)*vertical_interval, 100)
                y_1 = horizontal_tilt * x_1 + n * horizontal_interval
                plt.plot(x_1, y_1)

                y_2 = np.linspace(n*horizontal_interval, (n+1)*horizontal_interval, 100)
                x_2 = vertical_tilt * y_2 + m * vertical_interval
                plt.plot(x_2, y_2)
    
    elif type == "parabola":
        if decimal.search(request.POST["parabola_tilt"]):
            parabola_tilt = float(request.POST["parabola_tilt"])
        else:
            validation = False
        
        if decimal.search(request.POST["horizontal_interval"]):
            horizontal_interval = float(request.POST["horizontal_interval"])
        else:
            validation = False
        
        if decimal.search(request.POST["vertical_interval"]):
            vertical_interval = float(request.POST["vertical_interval"])
        else:
            validation = False
        
        if integer.search(request.POST["horizontal_max"]):
            horizontal_max = int(request.POST["horizontal_max"])
        else:
            validation = False
        
        if integer.search(request.POST["vertical_max"]):
            vertical_max = int(request.POST["vertical_max"])
        else:
            validation = False
        
        if not validation:
            redirect_url = reverse("tiling", kwargs={"type" : "parabola"})
            parameters = urlencode({"error" : "値を正しく入力してください"})
            url = f"{redirect_url}?{parameters}"
            return redirect(url)

        d = ((parabola_tilt * horizontal_interval)**2) / 4 

        for n in range(0, horizontal_max+1):    
            for m in range(0, vertical_max+1):  
                # タイルの下側の境界線 y=a(x-(nb+0.5b))^2+mc-ab^2/4 (nb<=x<=(n+1)b)
                x_1 = np.linspace(n*horizontal_interval, (n+1)*horizontal_interval, 100)
                y_1 = parabola_tilt * ((x_1 - (n*horizontal_interval + 0.5*horizontal_interval))**2) + m*vertical_interval - d
                plt.plot(x_1, y_1)
                
                # タイルの左側の境界線 x=nb (mc<=y<=(m+1)c)
                x_2 = np.linspace(n*horizontal_interval, n*horizontal_interval, 100)
                y_2 = np.linspace(m*vertical_interval, (m+1)*vertical_interval, 100)
                plt.plot(x_2, y_2)

    elif type == "wave":
        if decimal.search(request.POST["vertical_interval"]):
            vertical_interval = float(request.POST["vertical_interval"])
        else:
            validation = False
        
        if integer.search(request.POST["waves_number"]):
            waves_number = int(request.POST["waves_number"])
        else:
            validation = False
        
        if integer.search(request.POST["horizontal_max"]):
            horizontal_max = int(request.POST["horizontal_max"])
        else:
            validation = False
        
        if integer.search(request.POST["vertical_max"]):
            vertical_max = int(request.POST["vertical_max"])
        else:
            validation = False
        
        if not validation:
            redirect_url = reverse("tiling", kwargs={"type" : "wave"})
            parameters = urlencode({"error" : "値を正しく入力してください"})
            url = f"{redirect_url}?{parameters}"
            return redirect(url) 

        for n in range(0, vertical_max+1):    
            for m in range(0, horizontal_max+1):  
                # タイルの下側の境界線 y=sinx+na (2mbπ<=x<=2(m+1)bπ)
                x_1 = np.linspace(2*m*waves_number*math.pi, 2*(m+1)*waves_number*math.pi)
                y_1 = np.sin(x_1) + n*vertical_interval
                plt.plot(x_1, y_1)

                # タイルの左側の境界線 x=2mbπ (na<=y<=(n+1)a)
                x_2 = np.linspace(2*m*waves_number*math.pi, 2*m*waves_number*math.pi, 100)
                y_2 = np.linspace(n*vertical_interval, (n+1)*vertical_interval, 100)
                plt.plot(x_2, y_2)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=200)
    png = buffer.getvalue()
    graph = base64.b64encode(png)
    graph = graph.decode("utf-8")
    buffer.close()
    plt.cla()

    if type == "line":
        return render(request, "display.html", {"graph" : graph, "type" : type, 
                                                "horizontal_tilt" : horizontal_tilt, 
                                                "horizontal_interval" : horizontal_interval, 
                                                "vertical_tilt" : vertical_tilt, 
                                                "vertical_interval" : vertical_interval, 
                                                "horizontal_max" : horizontal_max, 
                                                "vertical_max" : vertical_max})
    elif type == "parabola":
        return render(request, "display.html", {"graph" : graph, "type" : type,
                                                "parabola_tilt" : parabola_tilt, 
                                                "horizontal_interval" : horizontal_interval,
                                                 "vertical_interval" : vertical_interval, 
                                                 "horizontal_max" : horizontal_max, 
                                                 "vertical_max" : vertical_max})
    elif type == "wave":
        return render(request, "display.html", {"graph" : graph, "type" : type,
                                                "vertical_interval" : vertical_interval,
                                                 "waves_number" : waves_number, 
                                                 "horizontal_max" : horizontal_max, 
                                                 "vertical_max" : vertical_max})





    
