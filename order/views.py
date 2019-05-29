from datetime import datetime

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from BookShopBackend.settings import DOMAIN
from order.models import Order, Transaction, OrderStatus
from order.serializers import OrderSerializer, TransactionUpdateSerializer


class OrderListView(ListAPIView):
    """
    当前用户订单列表
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(order_user=user)


class OrderRetrieveAPIView(RetrieveAPIView):
    """
    取回订单
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(order_user=user)


class OrderCreateView(CreateAPIView):
    """
    创建订单并生成支付链接
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        price = serializer.validated_data['order_price']

        order_id = serializer.data['order_id']
        pay_url = DOMAIN + "orders/pay?id=" + str(order_id)

        ret_data = {
            "pay_url": pay_url
        }

        ret_data.update(serializer.data)

        return Response(ret_data, status=status.HTTP_201_CREATED, headers=headers)


class OrderProcessView(UpdateAPIView):
    """
    订单处理
    """
    lookup_field = 'order'
    queryset = Transaction.objects.all()
    serializer_class = TransactionUpdateSerializer
    permission_classes = (IsAuthenticated,)


class TestPayView(APIView):
    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get("id")
        trans = Transaction.objects.get(order_id=order_id)
        trans.order_status = OrderStatus.Payed
        trans.order_pay_time = datetime.now()
        trans.save()
        return Response(
            {
                "status": "支付成功"
            },
            status=status.HTTP_200_OK
        )
