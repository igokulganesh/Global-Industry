from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from tenants.models import Client, Domain
from inventory.models import Accounts
import re 
from django.shortcuts import get_object_or_404
from django.db import connection
from django_tenants.utils import schema_context
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		name 	 = request.POST['name']
		email 	 = request.POST['email']
		phno 	 = request.POST['phno'] # Storing phno in last_name

		
		# Function checks if the string contains any special character 
		regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

		if(regex.search(username) != None):
			messages.error(request,'username must not conatain any special name')
			messages.info(request,'Try Another Username')
			return redirect('home:register')

		if bool(re.search(r"\s", username))  == True :
			messages.error(request,'username must not conatain space')
			messages.info(request,'Try Another Username')
			return redirect('home:register')

		if username.islower() != True :
			messages.error(request,'username must be lower case only')
			messages.info(request,'Try Another Username')
			return redirect('home:register')

		if User.objects.filter(username=username).exists() :
			messages.error(request,'Username is aldready taken')
			messages.info(request,'Try Another Username')
			return redirect('home:register')

		user = User.objects.create_user(username=username, password=password, first_name=name, last_name=phno, email=email)
		user.save() 

		tenant = Client.objects.create(user=user, schema_name= user.username)
		tenant.save()
		domain = Domain()
		domain.domain = tenant.schema_name + ".global.localhost"
		domain.tenant = tenant 
		domain.is_primary = True
		domain.save()

		messages.success(request,'Account created successfully for {}'.format(name))


		with schema_context(username):
			ac = Accounts(name=username, money=0).save()

		return redirect('home:login')
	return render(request,'login.html')
	
def login(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			messages.success(request,'{},  Welcome :)'.format(user))
			# url = "http://" + username + ".global.localhost:8000/welcome/"
			# return redirect(url)
			# with connection.cursor() as cursor:
			# 	cursor.execute(f"SET search_path to " + username)
			#	cursor.execute(f"ALTER ROLE django_user SET search_path TO " + request.user.username + " ,public" )
			return redirect('inventory:dashboard')
		else:
			messages.error(request,'Username or password incorrect')
		
	return render(request,'login.html')


def logoutUser(request):
	logout(request)
	return redirect('home:index')

@login_required(login_url='home:login')
def profile(request):
	form = UserForm(instance=request.user)
	if request.method == "POST":
		form = UserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, '{} Modified.'.format(request.user))
			return redirect('inventory:dashboard')
		else:
			messages.error(request, '{} not altered.'.format(request.user))
			messages.error(request, form.errors)
	header = "edit {}".format(request.user)
	return render(request, 'profile.html', {'form': form, 'header' : header })

@login_required(login_url='home:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('inventory:dashboard')
        else:
            messages.error(request, 'Please correct the errors below')
            messages.error(request, form.errors) 
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })	
	