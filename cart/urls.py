from django.urls import path
from .views import *

app_name= 'cart'

# detail이 카트의 홈, product_add, product_remove는 기능
urlpatterns= [
    path('', detail, name='detail'),
    path('add/<int:product_id>/', add, name='product_add'),
    path('remove/<product_id>/', remove, name='product_remove'),
]