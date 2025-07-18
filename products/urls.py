from django.urls import path
from .views import get_products, product_list

urlpatterns = [
    path('<slug>',get_products , name='get_product'), #name (get_product) is used in the template(url)
    path('', product_list, name='product_list'),
    
]