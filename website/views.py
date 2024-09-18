from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs): # 오버라이딩
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

import matplotlib
matplotlib.use('Agg') # Canvas는 웹에서 시각화를 위한 패키지
import matplotlib.pyplot as plt
from django.http import HttpResponse
import numpy as np
import pandas as pd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg

from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # 자동으로 로그인
            messages.success(request,"등록성공")
            return redirect("/")
        messages.error(request, "등록실패, 잘못된 정보가 있습니다.")
    form = NewUserForm() # 빈폼 : 입력
    return render(request = request, template_name = 'registration/register.html', context={'register_form':form})

def home(request):
    return render(request, 'home.html')
