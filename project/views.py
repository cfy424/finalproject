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

        e = models.Employee.objects.create(
            e_name=username,
            e_password=password,
            e_email=email,
            e_phone=phone,
            job_title=title
        )
        models.EmployeeAddress.objects.create(
            street=street,
            city=city,
            state=state,
            zip_code=zip,
            e_address=e
        )

        return redirect('/login/')

    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")

