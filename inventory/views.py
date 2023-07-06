from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db.models import Q
from .models import *	
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django_tenants.utils import schema_context

# from reportlab.pdfgen import canvas
# from weasyprint import HTML
# from weasyprint.fonts import FontConfiguration
from django.template.loader import render_to_string



# Create your views here.
def get_profit(tr):
	res = 0 
	for t in tr:
		if t.type == 0 :
			res += t.amt 
	return res 			

def get_expenses(tr):
	res = 0 
	for t in tr:
		if t.type == 1 :
			res += t.amt 
	return res

@login_required(login_url='home:login')
def dashboard(request):
	with schema_context(request.user.username ):
		
		today 	= datetime.date.today()

		month = []
		for i in range(1, 13):
			tr 	= Transaction.objects.filter(date__month=i, date__year=today.year)	
			pro = get_profit(tr)
			exp = get_expenses(tr)
			month.append(int(pro-exp))
		
		tr = Transaction.objects.filter(date__month=today.month, date__year=today.year)
		income 	= get_profit(tr)
		expenses = get_expenses(tr)

		try:
			profit_percentage = int(((income-expenses) / expenses ) * 100)
		except ZeroDivisionError:
			profit_percentage = 100 

		dict = { 

			"initial" 	: get_object_or_404(Accounts, name=request.user.username) ,
			"income"   	: income ,
			"expenses"	: expenses ,
			"profit_percentage"	: profit_percentage , 
			"loss_percetage"	: 100 - profit_percentage ,  
		}

		return render(request, 'inventory/dashboard.html', { 'dict' : dict , 'trans' : tr , 'month' : month })



@login_required(login_url='home:login')
def add_amount(request):
	with schema_context(request.user.username ):
		ac = get_object_or_404(Accounts, name=request.user.username)
		if request.method == "POST":
			form = AccountForm(request.POST, instance=ac)
			if form.is_valid():
				form.save()
				messages.success(request, 'Accounts Updated')
				return redirect('inventory:dashboard')
			else:
				messages.error(request, 'Accounts is not Updated')
				messages.error(request, form.errors)
		else:
			form = AccountForm(instance=ac)
		header = "Initial Account Balance"
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


# _____________________ For Transactions _______________________________

@login_required(login_url='home:login')
def view_credit(request):
	with schema_context(request.user.username ):
		tr 	   = Transaction.objects.filter(type=0)
		header = "Credited Transactions Details"
		return render(request, 'inventory/transaction.html', { 'trans' : tr, "header" : header })


@login_required(login_url='home:login')
def view_debit(request):
	with schema_context(request.user.username ):
		tr 	   = Transaction.objects.filter(type=1)
		header = "Debited Transactions Details"
		return render(request, 'inventory/transaction.html', { 'trans' : tr, "header" : header })

@login_required(login_url='home:login')
def view_all_transaction(request):
	with schema_context(request.user.username ):
		tr 	   = Transaction.objects.all()
		header = "All Transactions Details"
		return render(request, 'inventory/transaction.html', { 'trans' : tr, "header" : header })

# Have to complete accounts 
@login_required(login_url='home:login')
def add_transaction(request):
	with schema_context(request.user.username ):
		form=TransactionForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=TransactionForm(request.POST)
			if form.is_valid():
				amt  = form.cleaned_data.get('amt')
				type = form.cleaned_data.get('type')
				des  = form.cleaned_data.get('description')
				ac 	 = get_object_or_404(Accounts, name=request.user.username)

				if type == 1 and ac.is_available(amt) == False :
					messages.error(request, 'Sorry, No such Amount')	
					messages.error(request, 'Salary Not updated for {}'.format(emp))	
					return redirect('inventory:salary_cal')

				if type == 1 :
					ac.reduce_amt(amt)
				else:
					ac.increase_amt(amt)
				ac.save()

				form.save()
				messages.success(request, des )
				return redirect('inventory:dashboard')
			else:
				messages.error(request, 'Transaction Failed.')
				messages.error(request, form.errors)
		header = "New Transaction" 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


	
# _____________________ For Employee _______________________________

@login_required(login_url='home:login')
def employee(request):
	with schema_context(request.user.username ):
	#with connection.cursor() as cursor:
		#cursor.execute(f"SET search_path to " + )
		Emps = Employee.objects.all()
		return render(request, 'inventory/employee.html', { 'Emps': Emps })   
@login_required(login_url='home:login')
def add_employee(request):
	with schema_context(request.user.username ):
		form=EmployeeForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=EmployeeForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Employee Created.')
				return redirect('inventory:employee')
			else:
				messages.error(request, 'Employee Not Created.')
				messages.error(request, form.errors)
		header = "Create Employee here" 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

		
@login_required(login_url='home:login')
def emp_edit(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		if request.method == "POST":
			form = EmployeeForm(request.POST, instance=emp)
			if form.is_valid():
				form.save()
				messages.success(request, '{} updated'.format(emp.name))
				return redirect('inventory:employee')
			else:
				messages.error(request, '{} is not updated'.format(emp.name))
				messages.error(request, form.errors)
		else:
			form = EmployeeForm(instance=emp)
		header = "{} Details".format(emp)
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })

@login_required(login_url='home:login')
def delete_employee(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		messages.success(request, '{} is deleted'.format(emp))
		emp.delete()
		return redirect('inventory:employee')

@login_required(login_url='home:login')
def view_works(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		wk = Work.objects.filter(emp=emp_id)
		return render(request, 'inventory/view_works.html', { 'wk' : wk, 'emp' : emp })

@login_required(login_url='home:login')
def add_work(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		if request.method=="POST":
			form=WorkForm(request.POST)
			if form.is_valid():
				form = form.save(commit=False)
				form.emp = emp 
				if(form.material.is_available(form.weight)):
					form.product.add_product(form.weight)
					form.material.reduce(form.weight)
					try:
						raw_waste = Products.objects.get(name='raw_waste')
					except ObjectDoesNotExist:
						raw_waste = Products(name='raw_waste', cost=0, wages=0, weight=0)

					w = ( form.weight / form.material.getmake()) - form.weight 

					raw_waste.add_product(w)
					raw_waste.save()

					emp.add_bonus(form.product.get_wages() * form.weight)
					emp.save()
					form.save()
					messages.success(request, 'Work updated for {}'.format(emp))
					return view_works(request, emp_id)
				else:
					messages.error(request, 'There is no such amount of raw materials to make this product.')
			messages.error(request, 'Work is Not updated for {}.'.format(emp))

		header = "Add work for {}".format(emp)
		form = WorkForm(initial={'emp': emp })
		return render(request, 'inventory/add_common.html', {'form' : form, 'header' : header })


# _____________________ For ProductS _______________________________

@login_required(login_url='home:login')
def product_details(request):
	with schema_context(request.user.username ):
		pro = Products.objects.all()
		return render(request, 'inventory/product_details.html', { 'pro': pro })	

@login_required(login_url='home:login')
def add_product(request):
	with schema_context(request.user.username ):
		form=ProductForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=ProductForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Product Created.')
				return redirect('inventory:product_details')
			else:
				messages.error(request, 'Product not Created.')
				messages.error(request, form.errors)
		header = 'Create new Product'
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

@login_required(login_url='home:login')
def edit_product(request, pro_id):
	with schema_context(request.user.username ):
		pro = get_object_or_404(Products, pk=pro_id)
		if request.method == "POST":
			form = ProductForm(request.POST, instance=pro)
			if form.is_valid():
				form.save()
				messages.success(request, '{} updated.'.format(pro))
				return redirect('inventory:product_details')
		else:
			form = ProductForm(instance=pro)
		header = "{} Details".format(pro) 
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


@login_required(login_url='home:login')
def delete_product(request, pro_id):
	with schema_context(request.user.username ):
		pro = get_object_or_404(Products, pk=pro_id)
		messages.success(request, '{} is deleted'.format(pro))
		pro.delete()
		return redirect('inventory:product_details')


# _____________________ For Salary _______________________________

@login_required(login_url='home:login')
def get_total(request):
	with schema_context(request.user.username ):
		emp = Employee.objects.all()
		for e in emp :
			e.total = e.bonus + e.basicSalary 
			e.save()

@login_required(login_url='home:login')
def salary_details(request, emp_id): # for single employee 
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		sal = Salary.objects.filter(emp=emp)
		return render(request, 'inventory/salary_details.html', {'sal': sal, 'emp' : emp } )


@login_required(login_url='home:login')
def pay_now(request, emp_id, isall=False):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		ac = get_object_or_404(Accounts, name=request.user.username)

		if ac.is_available(emp.total) == False :
			messages.error(request, 'Sorry, No such Amount')	
			messages.error(request, 'Salary Not updated for {}'.format(emp))	
			return redirect('inventory:salary_cal')

		s 	= Salary(emp=emp, basicSalary=emp.basicSalary, bonus=emp.bonus, total=emp.total)
		s.save()
		emp.isPaid 	= True
		emp.bonus 	= 0  
		emp.lastSalary = now()
		emp.save()

		ac.reduce_amt(s.total)

		des = "Salary payed to {}".format(emp)
		Transaction(amt=s.total, description=des, type=1).save()

		if isall :
			return  
		messages.success(request, 'Payed to {}'.format(emp))	
		return redirect('inventory:salary_cal')


@login_required(login_url='home:login')
def pay_all(request):
	with schema_context(request.user.username ):
		emp = Employee.objects.all()
		ac = get_object_or_404(Accounts, name=request.user.username)
		
		t = 0 
		for e in emp :
			if e.isPaid == 0 :
				t += e.total 

		if ac.is_available(t) == False :
			messages.error(request, 'Sorry (・_・), No such Amount')	
			messages.error(request, 'Salary Not updated')	
			return redirect('inventory:salary_cal')

		for e in emp :
			if e.isPaid == 0 :
				pay_now(request, e.id, True)
		messages.success(request, 'Payed All')
		return redirect('inventory:salary_cal')


@login_required(login_url='home:login')
def salary_cal(request): # salary details for all employee
	with schema_context(request.user.username ):
		get_total(request) 	
		emp = Employee.objects.all()
		for e in emp : 
			if ( now().date() - e.lastSalary > timedelta(days=7) ) :
				e.isPaid = False 
				e.save()
		return render(request, 'inventory/salary_cal.html', {'emp' : emp })


# _____________________ For customer _______________________________

@login_required(login_url='home:login')
def customer(request):
	with schema_context(request.user.username ):
		cus = Customer.objects.all()
		return render(request, 'inventory/customer.html', { 'cus': cus })	

@login_required(login_url='home:login')
def add_customer(request):
	with schema_context(request.user.username ):
		form=CustomerForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=CustomerForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Customer Created.')
				return redirect('inventory:customer')
			else:
				messages.error(request, 'Customer not Created.')
				messages.error(request, form.errors)
		header = 'Create customer' 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def cust_edit(request, cus_id):
	with schema_context(request.user.username ):
		cus = get_object_or_404(Customer, pk=cus_id)
		if request.method == "POST":
			form = CustomerForm(request.POST, instance=cus)
			if form.is_valid():
				form.save()
				messages.success(request, '{} updated.'.format(cus))
				return redirect('inventory:customer')
			else:
				messages.error(request, 'Customer is not updated.')
				messages.error(request, form.errors)
		else:
			form = CustomerForm(instance=cus)
		header = "{} views".format(cus)
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


@login_required(login_url='home:login')
def delete_customer(request, cus_id):
	with schema_context(request.user.username ):
		cus = get_object_or_404(Customer, pk=cus_id)
		messages.success(request, '{} is deleted'.format(cus))
		cus.delete()
		return redirect('inventory:customer')

# _____________________ For Orders _______________________________
			

@login_required(login_url='home:login')
def order_all(request): # view all orders
	with schema_context(request.user.username ):
		return render(request, 'inventory/order.html', {'order' : Orders.objects.all() })


@login_required(login_url='home:login')
def order_not_delivered(request): # view not delivered orders
	with schema_context(request.user.username ):
		return render(request, 'inventory/order.html', {'order' : Orders.objects.filter(isDelivered=False) })


@login_required(login_url='home:login')
def order_delivered(request): # view delivered orders
	with schema_context(request.user.username ):
		return render(request, 'inventory/order.html', {'order' : Orders.objects.filter(isDelivered=True) })


@login_required(login_url='home:login')
def order_list(request, cus_id): # for particular customer 
	with schema_context(request.user.username ):
		cus = get_object_or_404(Customer, pk=cus_id)
		order = Orders.objects.filter(cus=cus_id)
		return render(request, 'inventory/order.html', {'order' : order})



@login_required(login_url='home:login')
def order_details(request, ord_id): # particular order details 
	with schema_context(request.user.username ):
		order = get_object_or_404(Orders, pk=ord_id)
		items = OrderItems.objects.filter(order=ord_id)
		return render(request, 'inventory/order_details.html', {'items' : items, 'order' : order })	


# def download_order(request, ord_id): # Billing download for 
# 	with schema_context(request.user.username ):
# 		order = get_object_or_404(Orders, pk=ord_id)
# 		items = OrderItems.objects.filter(order=ord_id)

# 		filename = 'Gi_' + str(order.cus.name) + "_" + str(order.id) 
# 		response = HttpResponse(content_type="application/pdf/force-download")
# 		response['Content-Disposition'] = "inline; filename={}.pdf".format(filename)
		
# 		html = render_to_string('inventory/order_details.html', {'items' : items, 'order' : order })
# 		font_config = FontConfiguration()

# 		HTML(string=html).write_pdf(response, font_config=font_config)

# 		return response

@login_required(login_url='home:login')
def order_now(request, cus_id): # for booking order 
	with schema_context(request.user.username ):
		if request.method == 'POST':
			formset = OrderFormset(request.POST)
			if formset.is_valid() :
				cus 	= get_object_or_404(Customer, pk=cus_id)
				total 	= 0 
				order 	= Orders(cus=cus, total_amt=total, Odate=now())
				order.save() 
				for form in formset: 
					if form.cleaned_data.get('product') and form.cleaned_data.get('weight'):
						product = form.cleaned_data.get('product')
						weight 	= form.cleaned_data.get('weight')
						total  += ( product.cost * weight ) 
						items 	= OrderItems(order=order,product=product, weight=weight) 
						items.save()

				if total : 
					order.total_amt = total 
					order.save() 
					messages.success(request, 'Order Booked.')
					return redirect('inventory:customer')
				else :
					messages.error(request, "Order not booked")

			else:
				for e in formset.errors :
					messages.error(request, e )
		else:
			formset = OrderFormset(request.GET or None)
		return render(request, 'inventory/order_now.html', { 'formset': formset })


@login_required(login_url='home:login')
def delivered(request, ord_id): # completing the order 
	with schema_context(request.user.username ):
		order 			  = get_object_or_404(Orders, pk=ord_id)
		items 			  = OrderItems.objects.filter(order=order)
		for i in items :
			if(i.product.is_available(i.weight) == False):
				messages.error(request, '{} is Out of Stock!'.format(i.product.name))
				messages.error(request, 'Order cannot be deliver.')
				return redirect('inventory:order_all')

		for i in items :
			i.product.reduce_product(i.weight)

		ac = get_object_or_404(Accounts, name=request.user.username)
		ac.increase_amt(order.total_amt)
		ac.save()

		des = "Order Completed for {}".format(order.cus)
		Transaction(amt=order.total_amt, description=des, type=0).save()

		order.Ddate 	  = now()
		order.isDelivered = True
		order.save()
		messages.success(request, 'Order Completed.')
		return redirect('inventory:order_all')


# _____________________ For Supplier _______________________________


@login_required(login_url='home:login')
def supplier(request):
	with schema_context(request.user.username ):
		Sup = Supplier.objects.all()
		return render(request, 'inventory/supplier.html', { 'Sup': Sup })


@login_required(login_url='home:login')
def add_supplier(request):
	with schema_context(request.user.username ):
		form=SupplierForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=SupplierForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Supplier Created.')
				return redirect('inventory:supplier')
				
			else:
				print(form.errors)
				messages.error(request, 'Supplier not Created.')
				messages.error(request, form.errors)
				
		header = 'Add Supplier'
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def sup_edit(request, sup_id):
	with schema_context(request.user.username ):
		sup = get_object_or_404(Supplier, pk=sup_id)
		form = SupplierForm(instance=sup)
		if request.method == "POST":
			form = SupplierForm(request.POST, instance=sup)
			if form.is_valid():
				form.save()
				messages.success(request, '{} Modified.'.format(sup))
				return redirect('inventory:supplier')
			else:
				messages.error(request, '{} not altered.'.format(sup))
				messages.error(request, form.errors)
		header = "Modify {}".format(sup)
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })	


@login_required(login_url='home:login')
def delete_supplier(request, sup_id):
	with schema_context(request.user.username ):
		sup = get_object_or_404(Supplier, pk=sup_id)
		messages.success(request, '{} deleted.'.format(sup))
		sup.delete()
		return redirect('inventory:supplier')		


@login_required(login_url='home:login')
def buy_material(request):
	with schema_context(request.user.username ):
		form=MaterialsOrderForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=MaterialsOrderForm(request.POST)
			if form.is_valid():
				material = form.cleaned_data.get('material')
				sup 	 = form.cleaned_data.get('sup')
				weight 	 = form.cleaned_data.get('weight')
				rm 		 = get_object_or_404(raw_materials, name=material)
				sup  	 = get_object_or_404(Supplier, name=sup)
				ac 		 = get_object_or_404(Accounts, name=request.user.username)
				if ac.is_available(rm.cost * weight ) == False :
					messages.error(request, 'Sorry (・_・), No such Amount')	
					messages.error(request, '{} is not Purchased'.format(material))	
					return redirect('inventory:materials')

				ac.reduce_amt(rm.cost * weight)

				des = "{} is Purchased from {}".format(material, sup )
				Transaction(amt=rm.cost * weight, description=des, type=1).save()

				rm.update_weight(weight)
				rm.save() 

				materials_order(sup=sup, material=rm, weight=weight, total_amt=rm.cost * weight).save()

				messages.success(request, des)
				return redirect('inventory:view_purchase')
			else:
				messages.error(request, form.errors)
		header = 'Buy Raw Materials'
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def view_purchase(request):
	with schema_context(request.user.username ):
		mat = materials_order.objects.all()
		return render(request, 'inventory/view_purchase.html', { 'mat': mat })


# _____________________ For Raw Materials _______________________________


@login_required(login_url='home:login')
def materials(request):
	with schema_context(request.user.username ):
		mat = raw_materials.objects.all()
		return render(request, 'inventory/materials.html', { 'mat': mat })


@login_required(login_url='home:login')
def add_material(request):
	with schema_context(request.user.username ):
		form=MaterialsForm()
		if request.method=="POST":
			form=MaterialsForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Raw Material is Created.')
				return redirect('inventory:materials')
			else:
				messages.error(request, 'Material is not created')
				messages.error(request,  form.errors)
		header = "Add New Raw Material" 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def material_edit(request, mat_id):
	with schema_context(request.user.username ):
		mat = get_object_or_404(raw_materials, pk=mat_id)
		if request.method == "POST":
			form = MaterialsForm(request.POST, instance=mat)
			if form.is_valid():
				form.save()
				messages.success(request, '{} is updated'.format(mat))
				return redirect('inventory:materials')
			else:
				messages.error(request,  form.errors)
		form 	= MaterialsForm(instance=mat)
		header  = "Update {}".format(mat)   
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


@login_required(login_url='home:login')
def delete_material(request, mat_id):
	with schema_context(request.user.username ):
		mat = get_object_or_404(raw_materials, pk=mat_id)
		messages.success(request, '{} is deleted'.format(mat))
		mat.delete()
		return redirect('inventory:materials')