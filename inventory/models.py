import datetime
from django.utils.timezone import now
from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.

# models.DateField(auto_now_add=True) use this 

CREDIT 	= 0 # means incoming
DEBIT 	= 1 # means Outgoing
Transaction_Type = [(CREDIT, 'Credit'), (DEBIT, 'Debit')]

class Accounts(models.Model): # company Account 
	name  = models.CharField("User Name", max_length=30)
	money = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Account Balance")

	def __str__(self):
		return str(self.money)

	def is_available(self, m):
		return (self.money-m >= 0 )

	def reduce_amt(self, m):
		self.money -= m 
		self.save()

	def increase_amt(self, m):
		self.money += m 
		self.save()

class Transaction(models.Model):	
	amt 		= models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Transaction Amount")
	description = models.CharField("Transaction Description", max_length=200)
	TYPE_CREDIT = 0
	TYPE_DEBIT 	= 1
	TYPE_CHOICES= [(TYPE_CREDIT, 'CREDIT'), (TYPE_DEBIT, 'DEBIT') ]
	type		= models.BooleanField(choices=TYPE_CHOICES,)
	date  		= models.DateField('date of Transaction',default=datetime.date.today)

	def __str__(self):
		return self.description 


class raw_materials(models.Model): # commpany Stock 
	name 	 = models.CharField("Material Name", max_length=30)
	cost 	 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cost of the material")
	weight 	 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Currently Available")
	make     = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Product Make percentage")

	def __str__(self):
		return self.name 

	def getmake(self): # it will return 0-1 value for 0-100 percentage 
		return self.make/100 

	def is_available(self, w): # use before reduce
		if(self.weight >= w/self.getmake()):
			return True 
		return False 

	def reduce(self, w): # use for update work 
		self.weight -= w/self.getmake() 
		self.save() 

	def update_weight(self, weight):
		self.weight += weight 
		self.save()

class Products(models.Model):
	name 	= models.CharField("Product Name", max_length=30)
	cost 	= models.DecimalField(max_digits=10, decimal_places=2,) # cost per Kg
	wages 	= models.DecimalField(max_digits=10, decimal_places=2, ) # wages per Kg
	weight 	= models.DecimalField(max_digits=10, decimal_places=2, ) # weight of the products in kg

	def is_available(self, w): # use before reduce_product 
		return ((self.weight - w) >= 0)

	def reduce_product(self, w): # use for customer delivery  
		self.weight -= w
		self.save()

	def add_product(self, w): # Employee add products AND raw waste will add
		self.weight += w
		self.save()

	def get_wages(self):
		return self.wages 

	def __str__(self):
		return self.name 

class Employee(models.Model):
	name 		= models.CharField("Employee Name", max_length=30)

	# Salary info 
	basicSalary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	bonus 		= models.DecimalField(max_digits=10, decimal_places=2, default=0)
	total 		= models.DecimalField(max_digits=10, decimal_places=2, default=0) # basic + bonus
	isPaid 		= models.BooleanField(default=False)
	lastSalary 	= models.DateField('last salary updated date',)

	DESIGNATION_CEO= 'Manager'
	DESIGNATION_WORKER= 'Worker'
	DESIGNATION_SUPERVISER= 'Superviser'
	DESIGNATION_MARKETING= 'MarketingHead'
	DESIGNATION_OTHERS= 'Others'
	DESIGNATION_CHOICES= [(DESIGNATION_WORKER, 'Worker'),(DESIGNATION_CEO,'Manager'),(DESIGNATION_SUPERVISER,'Superviser'),(DESIGNATION_MARKETING,'MarketingHead'),(DESIGNATION_OTHERS,'others') ]
	
	designation = models.CharField(choices=DESIGNATION_CHOICES, max_length=200,default='Others' )
	address = models.CharField(max_length=70)
	phone = models.CharField("Phone Number", max_length=11)
	dob = models.DateField('date of birth',  )
	doj = models.DateField('date of Joined',  )

	GENDER_MALE 	= 0
	GENDER_FEMALE 	= 1
	GENDER_OTHERS 	= 2
	GENDER_CHOICES 	= [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_OTHERS, 'Others') ]
	gender 			= models.IntegerField(choices=GENDER_CHOICES,default=2)

	def __str__(self):
		return self.name ; 

	def update_work(self, weight):
		self.product.add_product(weight)
		self.salary.add_amount(weight * product.wage)
		self.save()

	def add_bonus(self, amt):
		self.bonus += amt 
		self.isPaid = 0 
		self.save()

class Salary(models.Model):
	emp 		= models.ForeignKey(Employee, on_delete=models.CASCADE)
	basicSalary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	bonus 		= models.DecimalField(max_digits=10, decimal_places=2, default=0)
	total 		= models.DecimalField(max_digits=10, decimal_places=2, default=0) # basic + bonus
	paidDate 	= models.DateField('Date of payment', default=datetime.date.today,)

class Work(models.Model):
	emp 	 = models.ForeignKey(Employee, on_delete=models.CASCADE)
	product  = models.ForeignKey(Products, on_delete=models.CASCADE)
	material = models.ForeignKey(raw_materials, on_delete=models.CASCADE)
	weight 	 = models.DecimalField(max_digits=12, decimal_places=2,  default=0.0,)


# ____________________ For Customer and Orders models ________________________

class Customer(models.Model):
	name 	= models.CharField("Customer Name", max_length=30 )
	address = models.CharField(max_length=70)
	phone 	= models.CharField("Phone Number", max_length=11)

	def __str__(self):
		return self.name ; 


class Orders(models.Model):

	"""
	Contains a list of orders. 
	One row per order. 
	Each order is placed by a customer and has a Customer_ID - which can be used to link back to the customer record.
	
	""" 
	cus 		= models.ForeignKey(Customer, on_delete=models.CASCADE)
	Odate 		= models.DateField('Date of Ordered', default=datetime.date.today)
	Ddate 		= models.DateField('Delivered Date',default=datetime.date.today )
	total_amt 	= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
	isDelivered = models.BooleanField(default=False)

	def __str__(self):
		return "Order of " + self.cus 


class OrderItems(models.Model):

	"""
	Contains a list of order items. 
	One row for each item on an order - so each Order can generate multiple rows in this table. 
	Each item ordered is a product from your inventory, so each row has a product_id, which links to the products table.
	
	"""
	order 		= models.ForeignKey(Orders, on_delete=models.CASCADE)
	product 	= models.ForeignKey(Products, on_delete=models.CASCADE)
	weight		= models.DecimalField(max_digits=10, decimal_places=2) # weight of the products in kg


# ____________________ For Supplier and Materials models ________________________

class Supplier(models.Model):
	name 	= models.CharField("Supplier Name", max_length=30)
	address = models.CharField(verbose_name="Address of the supplier",max_length=70)
	phone 	= models.CharField("Phone Number", max_length=11)

	def __str__(self):
		return self.name ;

class materials_order(models.Model): # for purchasing raw materials                            
	sup 	 = models.ForeignKey(Supplier, on_delete=models.CASCADE)	
	material = models.ForeignKey(raw_materials, on_delete=models.CASCADE)	
	weight 	 = models.DecimalField(max_digits=10, decimal_places=2)	

	total_amt= models.DecimalField(max_digits=10, decimal_places=2, default=0)
	date 	 = models.DateField('Date Of purchase', default=datetime.date.today )

	def __str__(self):
		return "{} is buyed from {}".format(self.material, self.sup)


