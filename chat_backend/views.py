from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            # ここでセッションやトークンを設定
            return Response({"message": "ログイン成功"}, status=status.HTTP_200_OK)
        return Response({"message": "ユーザー名またはパスワードが間違っています"}, status=status.HTTP_401_UNAUTHORIZED)
