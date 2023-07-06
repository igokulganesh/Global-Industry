from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('add_amount/',views.add_amount, name='add_amount'),
    path('add_transaction/',views.add_transaction, name='add_transaction'),
    path('view_credit/',views.view_credit, name='view_credit'),
    path('view_debit/',views.view_debit, name='view_debit'),
    path('view_all_transaction/',views.view_all_transaction, name='view_all_transaction'),


    # For Employee 
    path('employee/',views.employee,name='employee'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('<int:emp_id>/emp_edit/', views.emp_edit, name='emp_edit'),
 	path('<int:emp_id>/delete_employee/', views.delete_employee, name='delete_employee'),
 	path('<int:emp_id>/view_works/', views.view_works, name='view_works'),
 	path('<int:emp_id>/add_work/', views.add_work, name='add_work'),

    # For Salary
    path('<int:emp_id>/pay_now/', views.pay_now, name='pay_now'),
    path('salary_cal/',views.salary_cal,name='salary_cal'),
    path('pay_all/',views.pay_all,name='pay_all'),
    path('<int:emp_id>/salary_details/', views.salary_details, name='salary_details'),


 	# For Customer
 	path('customer/',views.customer,name='customer'),
 	path('add_customer/',views.add_customer,name='add_customer'),
 	path('<int:cus_id>/cust_edit/', views.cust_edit, name='cust_edit'),
 	path('<int:cus_id>/delete_customer/', views.delete_customer, name='delete_customer'),

 	# For orders
    path('order_all/',views.order_all,name='order_all'),
    path('order_not_delivered/',views.order_not_delivered,name='order_not_delivered'),
    path('order_delivered/',views.order_delivered,name='order_delivered'),
    path('<int:cus_id>/order_list/', views.order_list, name='order_list'),
    path('<int:cus_id>/order_now/', views.order_now, name='order_now'),
    path('<int:ord_id>/order_details/', views.order_details, name='order_details'),
    path('<int:ord_id>/delivered/', views.delivered, name='delivered'),
   # path('<int:ord_id>/download_order/', views.download_order, name='download_order'),

 		
 	# For product 
 	path('product_details/',views.product_details,name='product_details'),
 	path('add_product/',views.add_product,name='add_product'),
 	path('<int:pro_id>/edit_product/', views.edit_product, name='edit_product'),
 	path('<int:pro_id>/delete_product/', views.delete_product, name='delete_product'),


 	# For Supplier
 	path('supplier/',views.supplier,name='supplier'),
 	path('add_supplier/',views.add_supplier,name='add_supplier'),
 	path('<int:sup_id>/sup_edit/', views.sup_edit, name='sup_edit'),
    path('<int:sup_id>/delete_supplier/',views.delete_supplier,name='delete_supplier'),

    # For Raw Materials
    path('materials/',views.materials,name='materials'),
    path('add_material/',views.add_material,name='add_material'),
    path('<int:mat_id>/material_edit/', views.material_edit, name='material_edit'),
    path('<int:mat_id>/delete_material/', views.delete_material, name='delete_material'),

    path('view_purchase/',views.view_purchase,name='view_purchase'),
    path('buy_material/',views.buy_material,name='buy_material'),

]