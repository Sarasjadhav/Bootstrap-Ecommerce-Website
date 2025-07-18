from django.db import models
from base.models import Basemodel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Product ,ColorVarient,SizeVarient
from products.models import Coupon

class Profile(Basemodel):
    User=models.OneToOneField(User,on_delete=models.CASCADE,related_name="Profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100);
    profile_image=models.ImageField(upload_to="Profile_images",null=True,blank=True)
    
    def get_cart_count(self):
        return CartItem.objects.filter(cart__user=self.User,cart__ispaid=False).count()

    
    
class Cart(Basemodel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,blank=True,null=True)
    is_paid=models.BooleanField(default=False)  
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    name_of_products=models.TextField(max_length=100,blank=True,null=True)
    currency = models.CharField(max_length=10, default='INR') 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_cart_total(self):
        total=0
        for item in self.cart_items.all():
            total+=item.get_product_price()
        if self.coupon:
            if self.coupon.minimum_amount < total:
                total-=self.coupon.discount_price
            self.amount=total
            self.save
        return total    
    
    def get_product_names(self):
        names = [item.products.Product_name for item in self.cart_items.all() if item.products]
        return ', '.join(names)
    
    def __str__(self):
        return self.user.username
    
    
class CartItem(Basemodel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    products=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    color_varient=models.ForeignKey(ColorVarient,on_delete=models.SET_NULL,blank=True,null=True)
    size_varient=models.ForeignKey(SizeVarient,on_delete=models.SET_NULL,blank=True,null=True)
    
    def get_product_price(self):
        price=[self.products.price]
        if self.color_varient:
            color_varient_price=self.color_varient.price
            price.append(color_varient_price)
        if self.size_varient:
            size_varient_price=self.size_varient.price
            price.append(size_varient_price)
        
        if self.cart.coupon:  
            if self.cart.coupon.minimum_amount < sum(price):
                return sum(price) - self.cart.coupon.discount_price
        return sum(price)
    
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(User=instance, email_token=email_token)
            email = instance.email
            print(f"Profile created for: {instance.email} with token: {email_token}")
            send_account_activation_email(email_token, email)
    except Exception as e:
        print(f"Error in signal: {e}")





