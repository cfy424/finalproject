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


# all product
def product_list(request):
    product = models.Product.objects.all()
    return render(request, 'product_list.html', {'product_list': product})


# fuzzy query
def get_product(request):
    search_type = request.POST.get('searchType')
    keyword = request.POST.get('keyword')
    if search_type == 'name':
        getProduct = models.Product.objects.filter(p_name__icontains=keyword)
    elif search_type == 'price':
        getProduct = models.Product.objects.filter(price__icontains=keyword)
    elif search_type == 'description':
        getProduct = models.Product.objects.filter(p_description=keyword)
    elif search_type == 'sale':
        getProduct = models.Product.objects.filter(sale=keyword)
    return render(request, "product_list.html", {"param": getProduct, "searchType": search_type, "keyword": keyword})


# add product
def add_product(request):
    if request.method == 'POST':
        new_price = request.POST.get('price')
        new_product_name = request.POST.get('p_name')
        new_description = request.POST.get('p_description')
        new_quantity = request.POST.get('quantity')
        new_sale = request.POST.get('sale')
        models.Product.objects.create(
            price=new_price, p_name=new_product_name,
            p_description=new_description, quantity=new_quantity,sale=new_sale
                                      )
        return redirect('/product_list/')


# delete product
def drop_product(request):
    drop_id = request.GET.get('p_id')
    drop_obj = models.Product.objects.get(p_id=drop_id)
    drop_obj.delete()
    return redirect('/product_list/')


# update product
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
        return redirect('/product_list/')


# all customer
def customer_list(request):
    customer = models.Customer.objects.all()
    return render(request, 'customer_list.html', {'customer_list': customer})


# all employee
def employee_list(request):
    employee = models.Customer.objects.all()
    return render(request, 'employee_list.html', {'product_list': employee})



# delete customer
def del_customer(request):
    if request.method == 'POST':
        delID = models.Customer.objects.get('c_id')
        delCustomer = models.Customer.objects.get(c_id=delID)
        delCustomer.delete()
    return redirect('/customer_list/')

