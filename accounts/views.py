from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from django.shortcuts import redirect
from products.models import Product,SizeVarient
from .models import Cart, CartItem
from products.models import ProductImage,Coupon
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings



def login_page(request):
    if request.method=="POST":
        email=request.POST.get('email') 
        password=request.POST.get('Password')
        
        user_obj=User.objects.filter(username=email)
        if not user_obj.exists():
            messages.error(request,"Account Not exists")
            return HttpResponseRedirect(request.path_info)
        if not user_obj[0].Profile.is_email_verified:
            messages.error(request,"Email is not verified")
            return HttpResponseRedirect(request.path_info)
        
        user_obj=authenticate(username=email,password=password)
        
        if user_obj:
            login(request,user_obj)
            return HttpResponseRedirect('/')
        else:
            messages.error(request,"Invalid Credentials")
        
    return render(request,'accounts/login.html')

def register_page(request):
    if request.method=="POST":
        first_name=request.POST.get('First_Name')
        last_name=request.POST.get('Last_Name')
        email=request.POST.get('Email')
        password=request.POST.get('Password')
        
        user_obj=User.objects.filter(username=email)
        if user_obj.exists():
            messages.error(request,"Email already exists")
            return HttpResponseRedirect(request.path_info)
        else:
            user=User.objects.create(username=email,first_name=first_name,last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            messages.success(request,"An email has been sent to your email address")
      
    return render(request,"accounts/register.html")

def logout_pg(request):
    logout(request)
    return redirect("/")
    

def activate_email(requset,email_token):
    try:
        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save() 
        messages.success(requset,"Email verified")
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid Token")

@login_required(login_url="login/")
def add_to_cart(request, slug):
    try:
        varient = request.GET.get('varient')
        product = get_object_or_404(Product, slug=slug)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

        cart_item = CartItem.objects.create(cart=cart, products=product)

        if varient:
            try:
                size_varient = get_object_or_404(SizeVarient, size_name=varient)
                cart_item.size_varient = size_varient
                cart_item.save()
            except Exception as e:
                print(f"Error adding size variant: {e}")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        return redirect('/')
    
@login_required(login_url="login/")
def remove_cart(request,cart_items_uid):
    try:
        cart_items=CartItem.objects.get(uid=cart_items_uid)
        cart_items.delete()
    except Exception as e:
        print(f"Error in remove_cart: {e}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required(login_url="login/")
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No products available in the cart.")
            return render(request, 'accounts/cart.html', {'cart_items': [], 'cart': None})

        for cart_item in cart_items:
            product_images = ProductImage.objects.filter(product=cart_item.products)
            cart_item.product_images = product_images.first() if product_images.exists() else None

        if request.method == "POST":
            coupon_code = request.POST.get('coupon')
            coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon_code).first()

            if not cart_items.exists():
                messages.warning(request, "Cannot apply coupon to an empty cart.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if not coupon_obj:
                messages.warning(request, "Invalid Coupon")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if cart.coupon:
                messages.warning(request, "Coupon already applied")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if cart.get_cart_total() < coupon_obj.minimum_amount:
                messages.warning(request, f'Amount should be greater than {coupon_obj.minimum_amount}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            if coupon_obj.is_expired:
                messages.warning(request, "Coupon is expired")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            cart.coupon = coupon_obj
            cart.save()
            messages.success(request, "Coupon applied successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        cart_total = cart.get_cart_total()
        if cart_total < 1:  
            return render(request, 'accounts/cart.html', {'cart_items': cart_items, 'cart': cart})

        cart.amount = cart.get_cart_total()
        cart.name_of_products = cart.get_product_names()
        cart.save()
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create({
        'amount': int(cart.get_cart_total() * 100),  
        'currency': 'INR',
        'payment_capture': '1'
        })
        cart.razorpay_order_id = payment['id']
        cart.save()

        print(f"Payment created successfully. Order ID: {payment['id']}")  # Add debug
        print(f"Payment response: {payment}")


        return render(request, 'accounts/cart.html', {
    'cart_items': cart_items,
    'cart': cart,
    'payment': payment, 
    'discount_price': cart.coupon.discount_price if cart.coupon else 0
})

    except Cart.DoesNotExist:
        messages.warning(request, "No products available in the cart.")
        return render(request, 'accounts/cart.html', {'cart_items': [], 'cart': None})
@login_required(login_url="login/")
def remove_coupon(request, cart_id):
    try:
        cart = Cart.objects.get(uid=cart_id)
        if cart.coupon:
            cart.coupon = None
            cart.save()
            messages.success(request, "Coupon removed successfully")
        else:
            messages.warning(request, "No coupon applied")
    except Exception as e:
        print(f"Error in remove_coupon: {e}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def success(request):
    try:
        razorpay_order_id = request.GET.get('razorpay_order_id')
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_signature = request.GET.get('razorpay_signature')
       
        cart = Cart.objects.filter(razorpay_order_id=razorpay_order_id).first()
        

        if not cart:
            messages.error(request, f"No cart found with order ID: {razorpay_order_id}")
            return redirect('payment_failed')

        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        
        params_dict = {
    'razorpay_order_id': razorpay_order_id,
    'razorpay_payment_id': razorpay_payment_id,
    'razorpay_signature': razorpay_signature
}

        client.utility.verify_payment_signature(params_dict)
        cart.razorpay_payment_id = razorpay_payment_id
        cart.razorpay_signature = razorpay_signature
        cart.is_paid = True
        cart.amount = cart.get_cart_total()
        cart.name_of_products = cart.get_product_names()
        cart.customer_id = request.user.id
        cart.currency = 'INR'
        cart.save()
        messages.success(request, "Payment Successful!")
        return render(request, 'accounts/success.html',{
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
            'cart': cart,
            'name_of_products': cart.name_of_products,
            'amount': cart.amount,
            'currency': cart.currency,
            'created_at': cart.created_at,
            'customer_id': cart.customer_id,
        })

    except Exception as e:
        print(f"Error in success: {e}")
        messages.error(request, "Something went wrong!")
        return redirect('payment_failed')



def failure(request):
    try:
        messages.error(request,"Payment Failed")
    except Exception as e:
        print(f"Error in failure: {e}")
    return render(request,'accounts/failure.html')

