from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .forms import AddProductForm
from .cart import Cart
# Create your views here.

@require_POST
def add(request, product_id):
    # 상세페이지와 장바구니에서 더하기
    #빈 카트든 채워진 카트이든 아래와 같이 표현됨.
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # 제품 상세페이지 혹은 장바구니페이지에서 전달된 request.POST
    # AddproductForm을 통해 전달된 데이터
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # form. cleaned_data returns a dictionary of validated form input fields and their values, where string primary keys are returned as objects. form. data returns a dictionary of un-validated form input fields and their values in string format (i.e. not objects).
    cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')

def remove(request, product_id):
    # 카트에서 제품 삭제하기
    # 이하 카트 불러오기 
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

def detail(request):
    # 카트 상세 페이지
    cart = Cart(request)

    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    return render(request, 'cart/detail.html', {'cart':cart})