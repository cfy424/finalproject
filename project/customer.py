from datetime import timedelta
from itertools import count

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.db import models
import datetime
from datetime import date
from django.http import Http404
from django.template.defaulttags import now
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from project import models
from django.db.models import Q, Count
from django.db.models import Avg, Max, Min
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
                user = models.Customer.objects.get(c_name=username)
            except:
                message = 'user not exist'
                return render(request, 'login/login.html', {'message': message})
            if user.e_password == password:
                request.session['is_login'] = True
                request.session['user_name'] = user.c_name
                return redirect('/index/')
            else:
                message = 'incorrect password'
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
        phone = request.POST.get('phone')
        income = request.POST.get('income')
        company = request.POST.get('company')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        c = models.Customer.objects.create(
            c_name=username,
            c_password=password,
            c_email=email,
            c_phone=phone,
            income=income,
            company=company
        )
        models.CustomerAddress.objects.create(
            street=street,
            city=city,
            state=state,
            zip_code=zip,
            c_address=c
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


# all product
@login
def product_list(request):
    productList = models.Product.objects.all()
    return render(request, 'login/index.html', {'product_list': productList})


# fuzzy query
@login
def get_product(request):
    search_type = request.POST.get('searchType')
    keyword = request.POST.get('keyword')
    if search_type == 'all':
        getProduct = models.Product.objects.filter(Q(p_name__icontains=keyword)\
                                                  | Q(price__icontains=keyword) | Q(p_description__icontains=keyword) \
                                                  | Q(sale__icontains=keyword) | Q(quantity__icontains=keyword))
    elif search_type == 'name':
        getProduct = models.Product.objects.filter(p_name__icontains=keyword)
    elif search_type == 'price':
        getProduct = models.Product.objects.filter(price__icontains=keyword)
    elif search_type == 'description':
        getProduct = models.Product.objects.filter(p_description__incontains=keyword)
    elif search_type == 'sale':
        getProduct = models.Product.objects.filter(sale__icontains=keyword)
    elif search_type == 'quantity':
        getProduct = models.Product.objects.filter(quantity__icontains=keyword)

    return render(request, "login/index.html", {"param": getProduct, "searchType": search_type, "keyword": keyword})


# search customer info
@login
def customer_info(request):
    if request.method == 'POST':
        message = "请检查填写的内容！"
        cname = request.POST.get('cname')
        password = request.POST.get('password')
        cemail = request.POST.get('email')
        cphone = request.POST.get('phone')
        cincome = request.POST.get('income')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        Zip = request.POST.get('zip')

        c = models.Customer.objects.filter(
            c_name=cname,
            cpassword=password,
            c_email=cemail,
            c_phone=cphone,
            income=cincome
        )
        models.CustomerAddress.objects.filter(
            street=street,
            city=city,
            state=state,
            zip_code=Zip,
            c_address=c
        )


# order history
@login
def history_info(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        time = request.POST.get('time')
        pname = request.POST.get('pname')
        cname = request.POST.get('cname')

        o = models.OrderHistory.objects.filter(
            o_status=status,
            o_time=time
        )

        models.Customer.objects.filter(
            c_name=cname,
            order_history=o
        )

        models.Product.objects.filter(
            p_name=pname,
            product=o
        )


# history by customer
@login
def history_customer(request):
    if request.method == 'POST':
        pass


# case_info
@login
def case_info(request):
    if request.method == 'POST':
        ca_summary = request.POST.get('summary')
        description = request.POST.get()
        time = request.POST.get()
        status = request.POST.get()
        ca_comment = request.POST.get()
        ca_customer = request.POST.get()
        ca_product = request.POST.get()
        ca_employee = request.POST.get()

        a = models.Case.objects.filter(
            summary=ca_summary,
            ca_description=description,
            ca_time=time,
            ca_status=status,
            comment=ca_comment,
        )
        models.Customer.objects.filter(
            c_name=ca_customer,
            customer=a
        )
        models.Employee.objects.filter(
            e_name=ca_employee,
            employee=a
        )
        models.Product.objects.filter(
            p_name=ca_product,
            product=a
        )


# search by time
@login
def case_time(request):
    if request.method == 'POST':
        case_year = request.POST.get('year')
        case_month = request.POST.get('month')
        case_day = request.POST.get('day')
        models.Case.objects.filter(date__year=case_year)
        models.Case.objects.filter(date__month=case_month)
        models.Case.objects.filter(date__day=case_day)
        return case_time


# search by status
@login
def case_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        models.Case.objects.filter(ca_status=status)
        return case_status


# case aggregation by product
@login
def case_product(request):
    if request.method == 'POST':
        models.Case.objects.annotate(p_num=Count(models.Case.objects.get(models.Case.product))).order_by('p_num')
        return case_product


# edit case
@login
def edit_case(request):
    if request.method == 'POST':
        new_status = request.POST.get('ca_status')
        new_comment = request.POST.get('ca_comment')
        edit_id = request.GET.get('id')
        edit_obj = models.Case.objects.get(id=edit_id)
        edit_obj.ca_status = new_status
        edit_obj.comment = new_comment
        edit_obj.save()
        return HttpResponse('success')


# resolution info
@login
def resolution_info(request):
    if request.method == 'POST':
        rname = request.POST.get('rname')
        r_step = request.POST.get('rstep')
        r_product = request.POST.get('rporduct')
        r_cname = request.POST.get('cname')
        r_employee = request.POST.get('remployee')
        r = models.Resolution.objects.filter(
            resolution_name=rname,
            step=r_step
        )
        models.Customer.objects.filter(
            c_name=r_cname,
            customer=r
        )
        models.Employee.objects.filter(
            e_name=r_employee,
            employee=r
        )
        models.Product.objects.filter(
            p_name=r_product,
            product=r
        )


