from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'index.html')

# ログイン実装
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success', 'username': username})
    else:
        return JsonResponse({'status': 'error', 'message': 'Login failed'})
    
@require_http_methods(['POST'])
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # email = request.POST.get('email', '')  # メールはオプションで受け取る

    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

    User.objects.create(
        username=username,
        # email=email,
        password=make_password(password))
    return JsonResponse({'status': 'success', 'message': 'User registered successfully'}, status=201)