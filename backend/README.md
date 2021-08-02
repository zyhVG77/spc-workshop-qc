#### 创建工程并运行
```
django-admin startproject mysite
python manage.py runserver
```
#### 创建app并注册
```
python manage.py startapp myapp
INSTALLED_APPS = [
    'myapp.apps.myappConfig',
]
```
#### 更新数据库表
```
$ python manage.py makemigrations myapp
$ python manage.py sqlmigrate myapp 0001
$ python manage.py migrate // 创建数据表

python manage.py shell
```