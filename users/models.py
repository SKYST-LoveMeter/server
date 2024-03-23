from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, username, password, real_name, **kwargs):
        user = self.model(
            username=username,
            real_name=real_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username=None, password=None, **extra_fields):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        superuser = self.create_user(
            username=username,
            password=password,
            real_name="admin", # superuser 만들 때 create_user를 부르기 때문에 nickname도 넘겨줘야됨
        )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    real_name = models.CharField(max_length=20)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 헬퍼 클래스 사용
    objects = UserManager()

    USERNAME_FIELD = 'username'
