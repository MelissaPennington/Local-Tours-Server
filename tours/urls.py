"""tours URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from toursapi.views import check_user, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'items', ItemView, 'item')
router.register(r'orderitems', OrderItemView, 'orderitem')
router.register(r'orders', OrderView, 'order')
router.register(r'revenues', RevenueView, 'revenue')
router.register(r'users', UserView, 'user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkuser', check_user),
    path('register', register_user),
    path('tours/<int:pk>/add_tour_category/<int:category_id>',
         OrderView.as_view({'post': 'add_order_item'}), name='order-add-order-item'),
    path('orders/<int:pk>/remove_order_item/<int:order_item>/',
         OrderView.as_view({'delete': 'remove_order_item'}), name='order-remove-order-item')
]
