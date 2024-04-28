from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json

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


@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    # email = request.POST.get('email', '')  # メールはオプションで受け取る
    print(json.dumps({'username': username, 'password': password}))

    if not username or not password:
        return JsonResponse({'status': 'error', 'message': 'Username or password cannot be empty'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

    User.objects.create(
        username=username,
        # email=email,
        password=make_password(password))
    return JsonResponse({'status': 'success', 'message': 'User registered successfully'}, status=201)

@csrf_exempt
@require_http_methods(['POST'])
def check_username(request):
    data = json.loads(request.body)
    username = data.get('username')
    if username and User.objects.filter(username=username).exists():
        return JsonResponse({'isValid': False, 'message': 'This username is already taken'}, status=400)
    return JsonResponse({'isValid': True})