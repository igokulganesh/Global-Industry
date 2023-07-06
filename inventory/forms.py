from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import *

TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'
ORDERING_FIELD_NAME = 'ORDER'
DELETION_FIELD_NAME = 'DELETE'

# default minimum number of forms in a formset
DEFAULT_MIN_NUM = 0

# default maximum number of forms in a formset, to prevent memory exhaustion
DEFAULT_MAX_NUM = 1000
class DateInput(forms.DateInput):
	input_type='date'

class EmployeeForm(forms.ModelForm):
	def __init__(self,data=None,files=None,request=None,recipient_list=None,*args,**kwargs):
		super().__init__(data=data,files=files,*args,**kwargs)
		self.fields['name'].widget.attrs['placeholder']='Enter the name'
		self.fields['address'].widget.attrs['placeholder']='Enter the address'
		self.fields['phone'].widget.attrs['placeholder']='Enter the phone no'
		self.fields['gender'].widget.attrs['placeholder']='select '

		
	class Meta:
		model=Employee
		fields=('name','designation','address','phone','dob','doj','basicSalary','gender', 'lastSalary', 'bonus', )
		widgets={
		     'dob':DateInput(),
		     'doj':DateInput(),
		     'lastSalary':DateInput(),
		   
		     
		}

class CustomerForm(forms.ModelForm):
	class Meta:
		model=Customer
		fields=('name','address','phone')
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the  name'}),
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the addres'}),
		'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the phone no'}),

		}		

class WorkForm(forms.ModelForm):
	#emp = forms.IntegerField(widget=forms.HiddenInput())
	product = forms.ModelChoiceField(queryset=Products.objects.all(),  empty_label="Select the Product", required=True)
	material = forms.ModelChoiceField(queryset=raw_materials.objects.all(),  empty_label="Select the material", required=True)
	weight  = forms.DecimalField(max_digits=10, decimal_places=2 ,required=True, 
		widget = forms.NumberInput(attrs={ 'step': 0.50,'placeholder': 'Enter Quantity  (in kg)'}),
		label = 'Quantity'
		)
	class Meta:
		model=Work
		#fields=('product', 'weight')
		exclude= ["emp"]

class ProductForm(forms.ModelForm):
	class Meta:
		model=Products
		fields=('name','cost','wages','weight')
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the product name'}),
		'cost':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'Enter the cost per kg'}),
		'wages':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'Enter the wages per kg'}),
		'weight':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'Enter the weight in kg'}),
		}

class OrderForm(forms.ModelForm): 
	class Meta:
		model=Orders
		fields=('cus',)

class OrderNowForm(forms.Form):
	product = forms.ModelChoiceField(queryset=Products.objects.all(),  empty_label="Select the Product", required=True)
	weight  = forms.DecimalField(max_digits=10, decimal_places=2 ,required=True, 
		widget = forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity  (in kg)'}),
		label = 'Quantity'
		)

OrderFormset = formset_factory(OrderNowForm, extra=1)


# class OrderNowForm(forms.ModelForm):
# 	class Meta:
# 		model 	= OrderItems
# 		fields 	= ('product', 'weight', )
# 		labels 	= 	{
#             			'product': 'Choose the Product', 
#             			'weight' : 'Quantity (in kg)' 
#         		  	}

# 		widgets =  {
#             			#'product': forms.ModelChoiceField(attrs={ 'class': 'form-control','placeholder': 'Select Product'}), 
#             			'weight' : forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity'})
#          			}


# OrderModelFormset = modelformset_factory(
#     OrderItems,
#     fields=('product', 'weight', ),
#     extra=1,
# 	widgets = 	{
#         			'weight'  : forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity'})
#          		}
# )




	#def __init__(self,data=None,files=None,request=None,recipient_list=None,*args,**kwargs):
	#	super().__init__(data=data,files=files,*args,**kwargs)
	#	self.fields['name'].widget.attrs['placeholder']='name'
	#	self.fields['address'].widget.attrs['placeholder']='address'
	#	self.fields['phone'].widget.attrs['placeholder']='phone'

 
class SupplierForm(forms.ModelForm):	
 	class Meta:
 		model=Supplier
 		fields=('name','address','phone',)
 		widgets={
 		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the  name'}),
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the addres'}),
		'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the phone no'}),

		}
	
		
		

class SupplierForm(forms.ModelForm):	
	class Meta:
		model=Supplier
		fields=('name','address','phone',)
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the  name'}),
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the addres'}),
		'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the phone no'}),

		}
       		

class MaterialsForm(forms.ModelForm):
	class Meta:
		model  = raw_materials
		fields = '__all__'
		labels={
		'name':'Name of the material',
		'cost':'Cost of the material',
		'weight':'Available amount',
		'make':'Product make percentage',
		}
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the material name'}),
		'cost':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'Enter the cost'}),
		'weight':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'Enter the available amount'}),
		'make':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'Enter the make percentage'}),


		}

	def __init__(self, *args, **kwargs):
		super(MaterialsForm, self).__init__(*args, **kwargs)
		for key in self.fields:
			self.fields[key].required = True

class MaterialsOrderForm(forms.ModelForm):
	sup = forms.ModelChoiceField(queryset=Supplier.objects.all(),  empty_label="Select the supplier", required=True,label='Supplier')
	material = forms.ModelChoiceField(queryset=raw_materials.objects.all(),  empty_label="Select the material", required=True)
	weight  = forms.DecimalField(max_digits=10, decimal_places=2 ,required=True, 
	 	widget = forms.NumberInput(attrs={ 'step': 0.50,'placeholder': 'Enter Quantity  (in kg)'}),
	 	label = 'Quantity'
	 	)
	class Meta:
		model  = materials_order
		fields = ('sup', 'material', 'weight')


class AccountForm(forms.ModelForm):
	money = forms.DecimalField(
		max_digits=15, decimal_places=2 ,required=True, 
		widget = forms.NumberInput(attrs={ 'step': 50.00,'class':'form-control','placeholder': 'Enter Inital Account balance'}),
		label = "Company's Inital Amount" 
	)
	class Meta:
		model  = Accounts
		fields = ('money',)


class TransactionForm(forms.ModelForm):

	class Meta:
		model  = Transaction
		fields = '__all__'
		widgets={
		  'date':DateInput()
		}