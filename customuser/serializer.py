from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=True, validators=[MinLengthValidator(8, '8자리 이상으로 설정해주세요')])

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password' : {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):

    #만약에 이게 없으면 로그인이 안되나?
    #일단 한번 해보자 ㄱㄱ 안되네 왜 안되지?
    #이유가 무엇일까? 왜지, 역직렬화를 위한 필드를 지정해야 하는데
    #시리얼라이저에서는 모델에 대응하는 필드를 필수적으로 만들어야 한다
    #그 이유는 필드에 따라 validation이 다르게 수행되기 때문이지
    #modelserializer는 그것을 편하게 만들 뿐이다.

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("잘못된 토큰입니다. 로그인 할 수 없어요.")

class UsernameUniqueSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    #username = serializers.CharField(max_length=255)
    class Meta:
        model = User
        #시리얼라이저 필드중에서 단 한개만 가져오겠다 이거지뭐
        fields = ('username',)
