from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import (
    Shop, Category, Product, ProductInfo, Parameter, ProductParameter,
    Order, OrderItem, Contact
)
from .serializers import (
    ShopSerializer, CategorySerializer, ProductSerializer, ProductInfoSerializer,
    ParameterSerializer, ProductParameterSerializer, OrderSerializer, OrderItemSerializer,
    ContactSerializer, UserSerializer
)
from django.core.mail import send_mail
from django.conf import settings


class UserCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=request.data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name']
            )
            send_mail(
                'Confirm your registration',
                'Thank you for registering. Please confirm your email address.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user).exclude(status='cart')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        order = Order.objects.get(user=request.user, status='cart')
        order.status = 'confirmed'
        order.save()
        send_mail(
            'Order Confirmation',
            f'Your order {order.id} has been confirmed.',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            order_item = OrderItem.objects.get(pk=pk, order__user=request.user)
            order_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ContactView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        contacts = Contact.objects.filter(user=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
