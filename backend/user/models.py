from django.db import models
from django.db.models.fields import validators
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.IntegerChoices):
    ADMIN = 0, 'admin'
    SUPEREDITOR = 1, 'super_editor'
    VIEWER = 2, 'viewer'

class user_account_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='用户编号'
                           )
    name = models.CharField(max_length=60,
                            unique=True,
                            help_text='用户名称'
                            )
    password_hash = models.CharField(max_length=60,
                                     help_text='用户密码哈希值'
                                     )
    role = models.IntegerField(choices=RoleChoices.choices,
                               help_text='权限角色'
                               )
    role_warehouse = models.IntegerField(choices=RoleChoices.choices,
                               help_text='仓储权限角色'
                               )

    def __str__(self):
        return self.name


class user_info(models.Model):
    user = models.OneToOneField(user_account_info, on_delete=models.CASCADE,
                                primary_key=True,
                                db_index=True, related_name='user_info',
                                help_text='用户信息'
                                )
    fullname = models.CharField(max_length=60,null=True,
                                help_text='用户全名'
                                )
    email = models.CharField(max_length=60,null=True,
                             help_text='用户email'
                             )
    phone = models.CharField(max_length=60,null=True,
                             help_text='用户手机'
                             )
    work_id = models.CharField(max_length=60,null=True,
                               help_text='用户工号'
                               )
    avatar = models.CharField(max_length=256, null=True,
                              help_text='图片地址'
                              )
# Create your models here.
