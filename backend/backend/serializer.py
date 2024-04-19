from django.contrib.auth.models import User
from rest_framework import serializers

class AuthTokenSerializer(serializers.Serializer):
  username = serializers.CharField(label="Username")
  password = serializers.CharField(label="Password", style={'inputtype':'password'}, trim_whitespace=False)

  def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # ここでユーザー認証のロジックを追加（例: authenticate(user=username, password=password)）
            # 認証成功時はユーザーオブジェクトをattrsに追加する
            pass
        else:
            msg = 'Username and password required'
            raise serializers.ValidationError(msg, code='authorization')
        return attrs