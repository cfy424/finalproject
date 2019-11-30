from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from project import models
import json

def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = 'please input'
        if username.strip() and password:
            try:
                user = models.Employee.objects.get(e_name=username)
            except:
                message = 'user not exist'
                return render(request, 'login/login.html', {'message': message})
            if user.e_password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.e_id
                request.session['user_name'] = user.e_name
                return redirect('/index/')
            else:
                message = 'incorre password'
                return render(request, 'login/login.html', {'message': message})
        else:
            return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        message = "请检查填写的内容！"
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        title=request.POST.get('title')
        street=request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        same_name_user = models.Employee.objects.filter(e_name=username)
        if same_name_user:
            message = '用户名已经存在'
            return render(request, 'login/register.html', {'message': message})
        same_email_user = models.Employee.objects.filter(e_email=email)
        if same_email_user:
            message = '该邮箱已经被注册了！'
            return render(request, 'login/register.html', {'message': message})
        new_user = models.Employee()
        new_user.e_name = username
        new_user.e_password = password
        new_user.e_email = email
        new_user.e_phone=phone
        new_user.job_title=title
        new_user.save()
        new_address=models.EmployeeAddress()
        new_address.street=street
        new_address.city=city
        new_address.state=state
        new_address.zip_code=zip
        new_address.save()
        return redirect('/login/')

    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    return redirect("/login/")

