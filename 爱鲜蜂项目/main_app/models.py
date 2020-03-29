from django.db import models

# Create your models here.

'''
商品表：
商品id(productid)        118826  
图片(productimg)      http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164119_550363.jpg@200w_200h_90Q
名字(productname)    爱鲜蜂·海南千禧果
长名字(productlongname)   爱鲜蜂·海南千禧果400-450g/盒
是否精选(isxf)    1
是否买一增一(pmdesc)   1
规格(specifics) 
价格(price)         13.80
原价(marketprice)     13.8
商品组id(categoryid)       103532
商品子组id(childcid)      103533
商品子组名名称(childcidname)   国产水果
详情页id(dealerid)       4858
库存(storenums)     7
销量(productnum) 
'''
class axf_goods(models.Model):
    productid = models.IntegerField()
    productimg = models.CharField(max_length=256)
    productname = models.CharField(max_length=256)
    productlongname = models.CharField(max_length=256)
    isxf = models.BooleanField(default=True)
    pmdesc = models.BooleanField(default=True)
    specifics = models.CharField(max_length=128)
    price = models.FloatField(default=1.0)
    marketprice = models.FloatField(default=1.0)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField(default=0)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)
    class Meta:
        db_table="axf_goods"



class axf_foodtypes(models.Model):
    typeid = models.IntegerField(default=0)
    typename = models.CharField(max_length=256)
    childtypenames = models.CharField(max_length=256)
    typesort = models.IntegerField(default=0)
    class Meta:
        db_table="axf_foodtypes"

class axf_user(models.Model):
    u_username = models.CharField(max_length=128)
    u_email = models.CharField(max_length=48,unique=True)
    u_password = models.CharField(max_length=128)
    u_icon = models.ImageField(upload_to=r"icon/%Y/%m/%d")
    u_isactivate = models.BooleanField(default=False)
    u_isdelete = models.BooleanField(default=False)
    class Meta:
        db_table="axf_user"

class axf_shopping_cart(models.Model):
    s_good = models.ForeignKey(axf_goods)
    s_user = models.ForeignKey(axf_user)
    s_num = models.IntegerField(default=0)
    s_isChoice = models.BooleanField(default=True)
    s_isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "axf_shopping_cart"


class axf_order(models.Model):
    o_user = models.ForeignKey(axf_user,null=True,on_delete=models.SET_NULL)
    o_time = models.DateTimeField(auto_now=True)
    o_price = models.FloatField(default=0.0)
    o_order_statu = models.IntegerField(default=0)
    class Meta:
        db_table="axf_order"

class axf_ordergoods(models.Model):
    og_goods = models.ForeignKey(axf_goods)
    og_order = models.ForeignKey(axf_order)
    og_num = models.IntegerField(default=1)
    class Meta:
        db_table="axf_ordergoods"