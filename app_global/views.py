from django.shortcuts import render
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date, timedelta, timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

def home(request):
    return render(request, 'home.html')
