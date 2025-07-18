from django.db import models
from base.models import Basemodel
from django.utils.text import slugify

class Category(Basemodel):
    category_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to="Category_images")
    slug=models.SlugField(unique=True,null=True,blank=True)
    # slug field is used to change in the url
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)
        
    def __str__(self):
        return self.category_name
    
class ColorVarient(Basemodel):
    color_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    
    def __str__(self):
        return self.color_name
    
class SizeVarient(Basemodel):
    size_name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    
    def __str__(self):
        return self.size_name
class Product(Basemodel):
    Product_name=models.CharField(max_length=100)
    category=models.ForeignKey(Category, related_name="Category", on_delete=models.CASCADE)
    price=models.IntegerField()
    product_description=models.TextField()
    slug=models.SlugField(unique=True,null=True,blank=True)
    color_varients=models.ManyToManyField(ColorVarient,blank=True)
    size_varients=models.ManyToManyField(SizeVarient,blank=True)    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.Product_name)
        super(Product,self).save(*args,**kwargs)
        
    def __str__(self):
        return self.Product_name
    
    def get_product_price_by_size(self,size):
        return self.price+SizeVarient.objects.get(size_name=size).price
    
class ProductImage(Basemodel):
    product=models.ForeignKey(Product,related_name="Product",on_delete=models.CASCADE)
    product_image=models.ImageField(upload_to="Product_images")
    
class Coupon(Basemodel):
    coupon_code=models.CharField(max_length=100)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=500)
    
    def __str__(self):
        return self.coupon_code
