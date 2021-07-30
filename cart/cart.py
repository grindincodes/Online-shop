from decimal import Decimal
from django.conf import settings
from shop.models import Product

#세션에 값을 저장하려면 세션 키 값을 설정해야 함. 예를 들어, 'cart_in_session' 처럼 이름지어 저장.
#settings.py 에 CART_ID = 'cart_in_session' 이런 식으로 되어 있음.
class Cart(object):
    def __init__(self, request):
        # 컨테이너, 즉 객체 생성 시 실행되는 부분
        # 객체가 생성될 때 initialize 하는 것
        # self.어쩌구 해서 객체의 변수 생성 self는 객체 자신을 가리킴.
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        # 세션에 아무것도 없으면 빈 카트 생성 
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        # 기본으로 실행되는 iteration
        # 키들(id들)이 담긴 리스트에서 id__in = 하면 그 id를 가진 제품들이 나오게 됨.
        # fliter(~Q(id__in=product_ids)) 하면 그 id를 제외한 제품들이 나오게 됨.
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, is_update=False):
        # 기본 수량 1, 업데이트 기본 False
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}
        # 없던 것이면 생성

        # 업데이트가 활성화 되어있으면 수량 바꿔주기 업데이트가 아니면 수량 더해주기
        # 즉, 장바구니에서 바꾸면 is_update=True 가 전달되고, 제품상세페이지에서는 =False
        if is_update:
            self.cart[product_id]['quantity'] = quantity
        
        else:
            self.cart[product_id]['quantity'] += quantity
        # 직접 작성한 save() 함수 이용하여 저장해주기
        self.save()
    
    def save(self):
        # DB에 저장하는 방식이 아니고 session에 저장하기
        # 세션 중 카트 세션에 카트 저장. 큰 딕셔너리 self.cart가 settings.CART_ID을 key값으로 하여 저장되는 것
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True
        # Django only saves to the session database when the session has been modified
        # we can tell the session object explicitly that it has been modified by setting the modified attribute on the session object:
        # https://docs.djangoproject.com/en/3.2/topics/http/sessions/ 참고

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()
            #지우고 카트 저장.

    def clear(self):
        # 카트세션 비우기
        self.session[settings.CART_ID] = {}
        self.session.modified = True
    
    def get_product_total(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())