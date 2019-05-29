from django.urls import path

from order.views import OrderListView, OrderCreateView, OrderRetrieveAPIView, OrderProcessView, TestPayView

urlpatterns = [
    path('', OrderListView.as_view(), name="order_list"),
    path('create/', OrderCreateView.as_view(), name="order_create"),
    path('<int:pk>/', OrderRetrieveAPIView.as_view(), name="order_info"),
    path('<int:order>/process/', OrderProcessView.as_view(), name="order_process"),
    path('pay/', TestPayView.as_view(), name="alipay_notify")
]
