from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import Message
import json

def index(request):
    return render(request, 'index.html')

@require_http_methods(['POST'])
def login_view(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')

    # デバッグ用
    # print("Username:", username)
    # print("Password:", password)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success', 'username': username})
    else:
        return JsonResponse({'status': 'error', 'message': 'Login failed'})
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)


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

@require_http_methods(['GET', 'POST'])
def message_view(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            message = data.get('message')
            Message.objects.create(username=username, text=message)
            return JsonResponse({'status': 'success', 'message': 'Message saved'}, status=201)
        elif request.method == 'GET':
            message = Message.objects.all().order_by('-id').values('id', 'username', 'text')
            return JsonResponse(list(message), safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
