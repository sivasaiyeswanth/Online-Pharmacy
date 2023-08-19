from django.urls import path

from . import views


urlpatterns = [
    # Other URL patterns...
     path('update_order/', views.update_order, name='update_order'),


     path('',views.interface, name = 'interface'),
     path('salary/', views.salary, name='salary'),
     path('products/', views.products, name='products'),
     path('Address/', views.Address, name = 'Address'),
     path('MyAddress/', views.MyAddress, name = 'MyAddress'),
     path('deliveryagent/',views.register_deliveryagent, name = 'deliveryagent'),
     path('deliveryagenthome/',views.deliveryagent_home, name = 'deliveryagenthome'),
     path('update_order/<str:test_id>',views.updateOrder,name = 'update_order'),
     path('delete_order/<str:test_id>',views.deleteOrder,name = 'delete_order'),
     path('delete_prod/<str:test_id>',views.delete_product,name = 'delete_prod'),
     path('update_prod/<str:test_id>',views.update_prod,name = 'update_prod'),
     path('update_ord/<str:test_id>/<str:test_i>/',views.update_ord,name = 'updatestatus'),
     path('viewprod/<str:test_id>',views.view_prod,name = 'viewprod'),
     path('vieword/<str:test_id>',views.vieword,name = 'vieword'),
     path('sellerview/<str:test_id>',views.seller_view,name = 'sellerview'),
     path('registerpage/',views.registerpage,name = 'register'),
     path('loginpage',views.loginpage, name = 'login'),
     path('logout/', views.logoutUser, name = 'logout'),
     path('user/',views.userPage,name='user-page'),
     path('account/', views.accountSettings, name = 'account'),
     path('payment/<str:test_id>',views.payment, name = 'payment'),
     path('seller/',views.register_seller, name = 'seller'),
     path('sellerhome/',views.seller_home, name = 'sellerhome'),
     path('sellerinventory/',views.seller_inventory, name = 'sellerinventory'),
     path('selleradditem/',views.seller_additem, name = 'selleradditem'),
     path('selleraccount/',views.seller_account, name = 'selleraccount'),
     path('deliveryaccount/',views.delivery_account, name = 'deliveryaccount'),
     path('buyer/', views.buyer, name="buyer"),
     path('item/', views.item, name="item"),
     path('cart/', views.cart, name="cart"),
     path('checkout/', views.checkout, name="checkout"),
     path('updateitem/', views.updateitem, name="updateitem"),
     path('processorder/', views.processorder, name="processorder"),
     path('myaccount/', views.myaccount, name = 'myaccount'),
     path('Track/', views.trackorder, name = 'trackorder'),
     path('selleradditem2/',views.addprod, name = 'selleradditem2'),
     path('search/',views.search,name = 'search'),
     
    
]


# Register your models here.
