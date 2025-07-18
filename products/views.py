from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.http import HttpResponse


def get_products(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        context = {'product': product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request, 'product/products.html', context=context)

    except Exception as e:
        print(f"Exception in get_products: {e}")
        return HttpResponse("<h3>Error loading product details</h3>")
    
def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Product_name__icontains=query)
    else:
        products = Product.objects.all()
    
    context = {'products': products}
    return render(request, 'home/index.html', context)


