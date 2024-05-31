from django.urls import path
from views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('orders/', OrderView.as_view(), name='order-list'),
    path('order-items/', OrderItemView.as_view(), name='order-item-create'),
    path('order-items/<int:pk>/', OrderItemView.as_view(), name='order-item-delete'),
    path('contacts/', ContactView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactView.as_view(), name='contact-delete'),
]
