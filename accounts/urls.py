from django.urls import path
from accounts.views import login_page,success,failure, register_page,add_to_cart,cart,activate_email,remove_cart,remove_coupon,logout_pg


urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    
    path('activate/<email_token>/', activate_email, name='activate_email'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove-cart/<cart_items_uid>/', remove_cart, name='remove_cart'),
    path('remove-coupon/<cart_id>', remove_coupon, name='remove_coupon'),
    path('logout/',logout_pg,name="logout_pg"),
    path('success/',success,name="payment_success"),
    path('failure/',failure,name="payment_failed")
]
