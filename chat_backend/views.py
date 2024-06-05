from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import Message, Room
from rest_framework.generics import ListAPIView
import json
import os
from django.conf import settings

from .serializers import RoomSerializer

class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

def index(request):
    return TemplateView.as_view(template_name='index.html')(request)
def list_static_files(request):
    static_dir = os.path.join(settings.BASE_DIR, 'static')  # BASE_DIRはsettings.pyからインポート
    try:
        files_list = os.listdir(static_dir)
        files_string = "<br>".join(files_list)
        return HttpResponse(files_string)
    except Exception as e:
        return HttpResponse(f"Error: {e}")

@require_http_methods(['POST']) 
@ensure_csrf_cookie
def login_view(request):
    try:
        data = json.loads(request.body)
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
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
def check_login_status(request):
    return JsonResponse({'isLoggedIn': request.user.is_authenticated})

@login_required
def get_current_user(request):
    user = request.user
    if user.is_authenticated:
        response_data = {
        'username': user.username,
        # 'email': user.email,
        # その他必要なユーザー情報
        }
        response = JsonResponse(response_data)
        return response
    else:
        print("Debug: User not authenticated, sending error")
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    
@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})

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

@csrf_exempt
@login_required
@require_http_methods(['GET', 'POST'])
def message_view(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            message = data.get('message')
            username = data.get('username', request.user.username)
            room_id = data.get('room_id')

            if message is None or room_id is None:
                return JsonResponse({'status': 'error', 'message': 'Message and room_id are required.'}, status=400)

            # 指定されたroom_idでルームを検索
            room = Room.objects.filter(id=room_id).first()
            if not room:
                return JsonResponse({'status': 'error', 'message': 'Room does not exist.'}, status=404)

            user = User.objects.filter(username=username).first()
            if not user:
                return JsonResponse({'status': 'error', 'message': 'User does not exist.'}, status=404)

            new_message = Message.objects.create(user=user, text=message, room=room)  # メッセージを保存

            return JsonResponse({
                'status': 'success',
                'message': 'Message saved',
                'new_message': {
                    'id': new_message.id,
                    'username': new_message.user.username,
                    'message': new_message.text,
                    # 'room_id': new_message.room.room_id,  # ルームIDを追加
                    'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=201)
        
        elif request.method == 'GET':
            room_id = request.GET.get('room_id')  # idを取得
            if not room_id:
                return JsonResponse({'status': 'error', 'message': 'room_id is required.'}, status=400)

            room = Room.objects.filter(id=room_id).first()
            if not room:
                return JsonResponse({'status': 'error', 'message': 'Room does not exist.'}, status=404)

            messages = Message.objects.filter(room=room).order_by('id').values('id', 'user__username', 'text', 'created_at')  # ルームでフィルタリング
            return JsonResponse(list(messages), safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@csrf_exempt
@login_required
@require_http_methods(['POST'])
def create_room(request):
    try:
        data = json.loads(request.body)
        room_name = data.get('roomName')

        if not room_name:
            return JsonResponse({'status': 'error', 'message': 'Room name is required.'}, status=400)

        new_room = Room.objects.create(name=room_name, created_by=request.user)

        return JsonResponse({
            'status': 'success',
            'message': 'Room created',
            'roomId': new_room.id
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
@login_required
@require_http_methods(['POST'])
def create_default_room(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        room_name = body.get('room_name')
        id = body.get('room_id')
        # print(f'room_id: {id}')
        id = int(id)
        room = Room.objects.filter(id=id).first()
        if room is None:
            # id=0の部屋を作成
            new_room = Room.objects.create(id=id, name=room_name, created_by=request.user)
            return JsonResponse({'status': 'success', 'message': 'Default room created', 'roomId': new_room.id}, status=201)
        else:
            return JsonResponse({'status': 'success', 'message': 'Default room already exists', 'roomId': room.id}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    


@require_http_methods(['POST'])
def logout_view(request):
    # ユーザーをログアウトする
    logout(request)
    # ログアウト後のレスポンスを返す
    return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})