from django import forms
from django.contrib.auth.forms import UserCreationForm   # 정보 저장
from django.contrib.auth.models import User   # 저장을 위한 테이블


class  UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")

