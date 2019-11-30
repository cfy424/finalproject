from project import models


p1 = models.Product.objects.create(p_name='Thinkpad', p_description='Electronic', price=500, quantity=200, sale=1.0)
p1.save()

p2 = models.Product.objects.create(p_name='Levis', p_description='Clothing', price=120, quantity=300, sale=1.0)
p2.save()

p3 = models.Product.objects.create(p_name='BMW', p_description='Car', price=30000, quantity=10, sale=1.0)
p3.save()

p4 = models.Product.objects.create(p_name='M&M', p_description='Sugar', price=8, quantity=10000, sale=1.0)
p4.save()

p5 = models.Product.objects.create(p_name='Parker', p_description='Office', price=21, quantity=500, sale=1.0)
p5.save()

e1 = models.Employee.objects.create(e_name='Alice', e_email='Alice@gmail.com', e_password='1234', e_phone=4124578775, job_title='Sales')
e1.save()

e2 = models.Employee.objects.create(e_name='Connie', e_email='Connie@gmail.com', e_password='1234', e_phone=2348937652, job_title='Sales')
e2.save()

e3 = models.Employee.objects.create(e_name='John', e_email='John@gmail.com', e_password='1234', e_phone=9763284914, job_title='Sales')
e3.save()

e4 = models.Employee.objects.create(e_name='Amy', e_email='Amy@gmail.com', e_password='1234', e_phone=6024720824, job_title='Sales')
e4.save()

e5 = models.Employee.objects.create(e_name='Henry', e_email='Henry@gmail.com', e_password='1234', e_phone=3298741893, job_title='DBA')
e5.save()

c1 = models.Customer.objects.create(c_name='Jerry', c_password='1234', c_email='Jerry@pitt.edu', c_phone='4123279191', income=80000, company='Facebook')
c1.save()

c2 = models.Customer.objects.create(c_name='Tom', c_password='1234', c_email='Tom@gmail.com', c_phone='4123273459', income=70000, company='Amazon')
c2.save()

c3 = models.Customer.objects.create(c_name='Mike', c_password='1234', c_email='Mike@163.com', c_phone='4122571772', income=60000, company='Barclay')
c3.save()

c4 = models.Customer.objects.create(c_name='Jake', c_password='1234', c_email='Jake@gmail.com', c_phone='4123221843', income=50000, company='Audi')
c4.save()

c5 = models.Customer.objects.create(c_name='Rose', c_password='1234', c_email='Rose@pitt.edu', c_phone='4123455621', income=55000, company='Target')
c5.save()

cAddress1 = models.CustomerAddress.objects.create(street='1001 Fifth Avenue', city='Los Angeles', state='CA', zip_code=90001)
cAddress1.save()

cAddress2 = models.CustomerAddress.objects.create(street='1002 Center Street', city='Pittsburgh', state='PA', zip_code=15122)
cAddress2.save()

cAddress3 = models.CustomerAddress.objects.create(street='1003 Kreielsheimer Street', city='Seattle', state='WA', zip_code=98101)
cAddress3.save()

cAddress4 = models.CustomerAddress.objects.create(street='1004 Lombard Street', city='Las Vegas', state='NV', zip_code=89101)
cAddress4.save()

cAddress5 = models.CustomerAddress.objects.create(street='1005 Jamison Street', city='Denver', state='CO', zip_code=80002)
cAddress5.save()

eAddress1 = models.EmployeeAddress.objects.create(street='1234 Yew Street', city='Pittsburgh', state='PA', zip_code=15224)
eAddress1.save()

eAddress2 = models.EmployeeAddress.objects.create(street='2345 Second Avenue', city='Pittsburgh', state='PA', zip_code=15217)
eAddress2.save()

eAddress3 = models.EmployeeAddress.objects.create(street='3456 Center Avenue', city='Pittsburgh', state='PA', zip_code=15215)
eAddress3.save()

eAddress4 = models.EmployeeAddress.objects.create(street='4567 Lima Street', city='Pittsburgh', state='PA', zip_code=15294)
eAddress4.save()

eAddress5 = models.EmployeeAddress.objects.create(street='5678 Third Avenue', city='Pittsburgh', state='PA', zip_code=15213)
eAddress5.save()



