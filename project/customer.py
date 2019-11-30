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
                user = models.Employee.objects.get(e_name=username)
            except:
                message = 'user not exist'
                return render(request, 'login/login.html', {'message': message})
            if user.e_password == password:
                request.session['is_login'] = True
                request.session['user_name'] = user.e_name
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
        title = request.POST.get('title')
        street = request.POST.get('street')
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


# add product
@login
def add_product(request):
    if request.method == 'POST':
        new_price = request.POST.get('price')
        new_product_name = request.POST.get('p_name')
        new_description = request.POST.get('p_description')
        new_quantity = request.POST.get('quantity')
        new_sale = request.POST.get('sale')
        models.Product.objects.create(
            price=new_price,
            p_name=new_product_name,
            p_description=new_description,
            quantity=new_quantity,
            sale=new_sale
        )
        return redirect('index.html')


# delete product
@login
def drop_product(request):
    drop_id = request.GET.get('id')
    drop_obj = models.Product.objects.get(id=drop_id)
    drop_obj.delete()
    return redirect('/product_list/')


# update product
@login
def edit_product(request):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_description = request.POST.get('description')
        new_price = request.POST.get('price')
        new_sale = request.POST.get('sale')
        new_quantity = request.POST.get('quantity')
        edit_id = request.GET.get('id')
        edit_obj = models.Product.objects.get(id=edit_id)
        edit_obj.p_name = new_name
        edit_obj.price = new_price
        edit_obj.p_description = new_description
        edit_obj.sale = new_sale
        edit_obj.quantity = new_quantity
        edit_obj.save()
        return HttpResponse('success')


'''
# all customer
def customer_list(request):
    customer = models.Customer.objects.all()
    cAddress = model.CustomerAddress.objects.all()
    return render(request, 'customer_list.html', {'customer_list': customer})


# all employee
def employee_list(request):
    employee = models.Customer.objects.all()
    eAddress = model.EmployeeAddress.objects.all()
    return render(request, 'employee_list.html', {'product_list': employee})
'''


# delete customer
@login
def del_customer(request):
    delID = request.GET.get('id')
    delCustomer = models.Customer.objects.get(id=delID)
    delCustomer.delete()
    return redirect('/customer_list/')


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


# employee info
@login
def employee_info(request):
    if request.method == 'POST':
        message = "请检查填写的内容！"
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        title = request.POST.get('title')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        e = models.Employee.objects.filter(
            e_name=username,
            e_password=password,
            e_email=email,
            e_phone=phone,
            job_title=title
        )
        models.EmployeeAddress.objects.filter(
            street=street,
            city=city,
            state=state,
            zip_code=zip,
            e_address=e
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


# case aggregation by customer
@login
def case_customer(request):
    if request.method == 'POST':
        name = models.Case.customer.c_name
        models.Case.objects.annotate(ca_num=Count(models.Case.objects.get(models.Case.customer))).order_by('ca_num')
        models.Case.objects.annotate(c_sum=Count(models.Case.objects.get(models.Case.customer.c_name))).\
            values(name, 'c_sum').order_by('c_sum')
        return case_customer


# case aggregation by company
@login
def case_company(request):
    if request.method == 'POST':
        models.Case.objects.annotate(ca_num=Count(models.Case.objects.get(models.Case.customer.company))).\
            order_by('ca_num')
        return case_company


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


# edit step
@login
def edit_step(request):
    if request.method == 'POST':
        new_step = request.POST.get('new_step')
        edit_id = request.GET.get('id')
        edit_obj = models.Resolution.objects.get(id=edit_id)
        edit_obj.step = new_step
        edit_obj.save()
        return HttpResponse('success')
