from django.db import models

from user.models import User


class OrderStatus:
    Canceled = 0
    Ordered = 1
    Payed = 2
    Confirmed = 3

    OrderStatusChoices = (
        (0, "已取消"),
        (1, "已下单"),
        (2, "已支付"),
        (3, "已确认"),
    )

    @staticmethod
    def status(status_code):
        return (
            '已取消',
            '已下单',
            '已支付',
            '已确认',
        )[status_code]


class Order(models.Model):
    order_id = models.AutoField(verbose_name="订单编号", primary_key=True)

    order_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="订单用户")

    def __str__(self):
        description = "编号:{}".format(self.order_id)
        return description

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name="订单编号", on_delete=models.CASCADE, related_name='order_detail')
    book_id = models.IntegerField(verbose_name="书籍编号")
    book_name = models.CharField(max_length=128, verbose_name="书名")
    book_author = models.CharField(max_length=128, verbose_name="作者", null=True, blank=True)
    book_ISBN = models.CharField(max_length=128, verbose_name='ISBN', null=True, blank=True)
    book_year = models.CharField(max_length=8, verbose_name='年份', blank=True, null=True)
    book_pages = models.IntegerField(verbose_name='页数', blank=True, null=True)
    book_language = models.CharField(max_length=64, verbose_name='语言', blank=True, null=True)
    book_category = models.CharField(verbose_name="分类", max_length=64, blank=True, null=True)
    book_picture = models.TextField(verbose_name="图片", null=True, blank=True)
    book_description = models.TextField(verbose_name="描述", null=True, blank=True)
    book_download_link_pdf = models.TextField(verbose_name='PDF下载链接', null=True, blank=True)
    book_download_link_epub = models.TextField(verbose_name='EPUB下载链接', null=True, blank=True)
    book_price = models.FloatField(verbose_name="价格")
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return "订单{}详情".format(self.order_id)

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name


class Transaction(models.Model):
    order = models.OneToOneField(Order, related_name="transaction", verbose_name="订单编号", on_delete=models.CASCADE)
    order_time = models.DateTimeField(verbose_name="下单时间", auto_now_add=True)
    order_price = models.FloatField(verbose_name="订单金额")
    PAY_CHOICES = (
        (0, "支付宝"),
        (1, '微信支付')
    )
    pay_method = models.IntegerField(choices=PAY_CHOICES, verbose_name="支付方式")
    order_pay_time = models.DateTimeField(verbose_name="付款时间", null=True, blank=True)
    order_confirm_time = models.DateTimeField(verbose_name="确认时间", null=True, blank=True)
    order_status = models.IntegerField(verbose_name="订单状态",
                                       choices=OrderStatus.OrderStatusChoices,
                                       default=OrderStatus.Ordered)
    check_info = models.TextField(null=True, blank=True, verbose_name="发票信息")
    trade_info = models.TextField(null=True, blank=True, verbose_name='交易信息')

    def __str__(self):
        return "订单{}交易信息".format(self.order)

    class Meta:
        verbose_name = '交易信息'
        verbose_name_plural = verbose_name
