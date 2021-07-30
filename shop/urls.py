from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', product_in_category, name='product_all'),
    path('<slug:category_slug>/', product_in_category, name='product_in_category'),
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'),
]
# slug 컨버터를 사용하지 않아도 작동하지만, 오류에 주의하기