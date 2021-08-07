from django.db import models
from datetime import datetime
# Create your models here.
# 员工信息账号模型
class User(models.Model):
    #类变量
    # id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50) #员工账号
    nickname=models.CharField(max_length=50) #昵称
    password_hash=models.CharField(max_length=100) #密码
    password_salt=models.CharField(max_length=50) #密码干扰值
    status=models.IntegerField(default=1) #状态：1正常/2禁用/6/管理员/9删除
    create_at=models.DateTimeField(default=datetime.now) #创建时间
    update_at=models.DateTimeField(default=datetime.now) #修改时间

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,
                'password_salt':self.password_salt,'status':self.status,'creat_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    class Meta:
        #实例变量
        db_table = "user" #更改表名


class Shop(models.Model):
    # id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255) #店铺名称
    cover_pic=models.CharField(max_length=255) #封面图片
    banner_pic=models.CharField(max_length=255) #图标logo
    address = models.CharField(max_length=255)    #店铺地址
    phone = models.CharField(max_length=255)    #联系电话
    status = models.IntegerField(default=1)        #状态:1正常/2暂停/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        shopname = self.name.split("-")
        return {'id':self.id,'name':shopname[0],'shop':shopname[1],'cover_pic':self.cover_pic,'banner_pic':self.banner_pic,'address':self.address,'phone':self.phone,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "shop"  # 更改表名

class category(models.Model):
    # id = models.AutoField(primary_key=True)
    shop_id = models.IntegerField() #店铺id
    name = models.CharField(max_length=50) #分类名称
    status = models.IntegerField(default=1) #状态:1正常/9缺货
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id, 'shop_id': self.shop_id,
                'name': self.name, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "category"  # 更改表名

class Product(models.Model):
    shop_id = models.IntegerField() #店铺id
    category_id = models.IntegerField() #菜品分类id
    cover_pic = models.CharField(max_length=50) #菜品图片
    name = models.CharField(max_length=50) #菜品名称
    price = models.FloatField() #菜品单价
    status = models.IntegerField(default=1) #状态:1正常/2暂停/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id': self.id, 'shop_id': self.shop_id, 'category_id': self.category_id, 'cover_pic': self.cover_pic,
                'name': self.name, 'price': self.price, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "product"  # 更改表名

class Member(models.Model):
    nickname= models.CharField(max_length=50) #昵称
    avatar = models.CharField(max_length=255) #头像
    mobile = models.CharField(max_length=50) #电话
    status = models.IntegerField(default=1) #状态:1正常/2暂停/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id': self.id, 'nickname': self.nickname, 'avatar': self.avatar, 'mobile': self.mobile,
                'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "member"  # 更改表名

class Order(models.Model):
    shop_id = models.IntegerField()  # 店铺id号
    member_id = models.IntegerField()  # 会员id
    user_id = models.IntegerField()  # 操作员id
    money = models.FloatField()  # 金额
    status = models.IntegerField(default=1)  # 订单状态:1过行中/2无效/3已完成
    payment_status = models.IntegerField(default=1)  # 支付状态:1未支付/2已支付/3已退款
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间


    def toDict(self):
        return {'id': self.id, 'shop_id': self.shop_id, 'member_id': self.member_id, 'user_id': self.user_id,'money':self.money,
                'status': self.status, 'payment_status':self.payment_status,'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "orders"  # 更改表名


# 订单详情模型
class OrderDetail(models.Model):
    order_id = models.IntegerField()  # 订单id
    #product_id = models.IntegerField()  # 菜品id
    product = models.ForeignKey('Product',on_delete=models.CASCADE) #多对一
    product_name = models.CharField(max_length=50)  # 菜品名称
    price = models.FloatField()  # 单价
    quantity = models.IntegerField()  # 数量
    status = models.IntegerField(default=1)  # 状态:1正常/9删除

    def toDict(self):
        return {'id': self.id, 'order_id': self.order_id, 'product_id': self.product_id, 'product_name': self.product_name,'price':self.price,
                'status': self.status, 'quantity':self.quantity}

    class Meta:
        db_table = "order_detail"  # 更改表名


# 支付信息模型
class Payment(models.Model):
    order_id = models.IntegerField()  # 订单id号
    member_id = models.IntegerField()  # 会员id
    money = models.FloatField()  # 支付金额
    type = models.IntegerField()  # 付款方式：1会员付款/2收银收款
    bank = models.IntegerField(default=1)  # 收款银行渠道:1微信/2余额/3现金/4支付宝
    status = models.IntegerField(default=1)  # 支付状态:1未支付/2已支付/3已退款
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    class Meta:
        db_table = "payment"  # 更改表名