from datetime import datetime

from rest_framework import serializers

from book.models import Book
from order.models import OrderDetail, Transaction, OrderStatus, Order


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    订单详情的序列化，从前端获得的只有book_id
    """

    def validate_book_id(self, data):
        if Book.objects.filter(id=data):
            return data
        else:
            raise serializers.ValidationError("书籍不存在")

    class Meta:
        model = OrderDetail
        exclude = ('id', 'order', 'created_at')
        extra_kwargs = {
            "book_name": {"read_only": True},
            "book_author": {"read_only": True},
            "book_ISBN": {"read_only": True},
            "book_year": {"read_only": True},
            "book_pages": {"read_only": True},
            "book_language": {"read_only": True},
            "book_category": {"read_only": True},
            "book_picture": {"read_only": True},
            "book_description": {"read_only": True},
            "book_download_link_pdf": {"read_only": True},
            "book_download_link_epub": {"read_only": True},
            "book_price": {"read_only": True},
        }


class TransactionSerializer(serializers.ModelSerializer):
    """
    交易信息的序列化
    """

    class Meta:
        model = Transaction
        exclude = ('id', 'order')


class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'order',
            'order_status'
        )

    def update(self, instance, validated_data):
        if instance:
            order_status = validated_data['order_status']
            # 下单->取消
            if instance.order_status == OrderStatus.Ordered and order_status == OrderStatus.Canceled:
                instance.order_status = order_status
            # 支付->取消
            # TODO:退款逻辑
            if instance.order_status == OrderStatus.Payed and order_status == OrderStatus.Canceled:
                instance.order_status = order_status
            # # 下单->支付
            # if instance.order_status == OrderStatus.Ordered and order_status == OrderStatus.Payed:
            #     instance.order_status = order_status
            #     instance.order_pay_time = datetime.now()
            if instance.order_status == OrderStatus.Payed and order_status == OrderStatus.Confirmed:
                instance.order_status = order_status
                instance.order_confirm_time = datetime.now()
            instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    """
    订单的序列化
    """
    order_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    order_detail = OrderDetailSerializer(many=True)
    order_price = serializers.FloatField(required=True, write_only=True)
    pay_method = serializers.IntegerField(write_only=True)
    order_status = serializers.IntegerField(required=True, write_only=True)
    # 交易信息时自动创建的，故只能读取
    transaction = TransactionSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'order_user',
            'order_price',
            'order_status',
            'order_detail',
            'pay_method',
            'transaction'
        )

    def validate_order_status(self, data):
        if data != OrderStatus.Ordered:
            return serializers.ValidationError("支付异常")
        return data

    def validate_pay_method(self, data):
        if data == 0 or data == 1:
            return data
        else:
            raise serializers.ValidationError("支付方式异常")

    def validate(self, attrs):
        order_details = attrs["order_detail"]
        price = 0
        # 验证价格计算正确
        for detail in order_details:
            book = Book.objects.filter(id=detail['book_id'])
            if not book:
                raise serializers.ValidationError("菜品信息错误")
            else:
                price += book[0].price
        if price != attrs['order_price']:
            raise serializers.ValidationError("价格异常")
        return attrs

    def create(self, validated_data):
        order_details = validated_data.pop("order_detail")
        order_price = validated_data.pop('order_price')
        order_status = validated_data.pop('order_status')
        pay_method = validated_data.pop('pay_method')
        order = Order.objects.create(
            **validated_data
        )
        for detail in order_details:
            book = Book.objects.get(id=detail['book_id'])
            OrderDetail.objects.create(
                **detail,
                order=order,
                book_name=book.name,
                book_author=book.author,
                book_ISBN=book.ISBN,
                book_year=book.year,
                book_pages=book.pages,
                book_language=book.language,
                book_category=book.category,
                book_picture=book.picture,
                book_description=book.description,
                book_download_link_pdf=book.download_link_pdf,
                book_download_link_epub=book.download_link_epub,
                book_price=book.price,
            )
            Transaction.objects.create(
                order=order,
                order_price=order_price,
                order_status=order_status,
                pay_method=pay_method,
            )
            return order
