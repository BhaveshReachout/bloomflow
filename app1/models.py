from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, RegexValidator
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    Fname = models.CharField(max_length=100, null=True, blank=True)
    Lname = models.CharField(max_length=100, null=True, blank=True)
    Cname = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    City = models.CharField(max_length=50, null=True, blank=True)
    State = models.CharField(max_length=50, null=True, blank=True)
    Country = models.CharField(max_length=50, null=True, blank=True)
    Zip = models.CharField(max_length=10, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)
    Email = models.EmailField(null=True, blank=True)
    Mobile = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return "%s" % self.user

    class Meta:
        db_table = 'profile'

    def set_data(self, n, form_pic, a='default'):
        self.name = n
        temp = self.picture
        self.picture = form_pic
        if self.picture == None:
            self.picture = temp
        self.address = a
        self.save()
        return 'done'

    def set_order_data(self, a='default'):
        self.address = a
        self.save()
        return 'done'


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    f_name = models.CharField(max_length=25)
    l_name = models.CharField(max_length=25)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=10)
    msg = models.TextField(max_length=500)

    def __str__(self):
        return "%s" % self.user

    class Meta:
        db_table = 'contact'

    def set_data(self, f_name1, l_name1, email1, mobile1, msg1):
        self.f_name = f_name1
        self.l_name = l_name1
        self.email = email1
        self.mobile = mobile1
        self.msg = msg1
        self.save()
        return 'done'


class Category(models.Model):
    C_name = models.CharField(max_length=35)
    C_disc = models.CharField(max_length=200)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return "%s" % self.C_name


class Subcategory(models.Model):
    Scname = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=CASCADE, related_name='subcat', default=None)

    def __str__(self):
        return self.Scname

    class Meta:
        db_table = 'subcategory'


class Product(models.Model):
    Pname = models.CharField(max_length=100)
    Image = models.ImageField(null=True, blank=True)
    Pcolour = models.CharField(max_length=50, null=True, blank=True)
    PCImage = models.ImageField(null=True, blank=True)
    Pprice = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    Pquantity = models.IntegerField(default=0)
    Ptotal = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    Pdesc = models.CharField(max_length=255)
    Psize = models.CharField(max_length=255, null=True, blank=True)
    Plight = models.CharField(max_length=255, null=True, blank=True)
    Pdifficulty = models.CharField(max_length=255, null=True, blank=True)
    PAirCleaner = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=CASCADE)
    subcategory = models.ForeignKey(
        Subcategory, null=True, blank=True, on_delete=CASCADE)
    Psku = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Pname

    def set_prod_total(self, temp):
        self.Ptotal = temp
        self.save()

    def set_prod_qty(self, qty):
        self.Pquantity = qty
        self.save()

    class Meta:
        db_table = 'Product'


class Product_Gallary(models.Model):
    Image1 = models.ImageField(null=True, blank=True)
    Image2 = models.ImageField(null=True, blank=True)
    Image3 = models.ImageField(null=True, blank=True)
    Productid = models.ForeignKey(
        Product, null=True, blank=True, on_delete=CASCADE)

    class Meta:
        db_table = 'Product_Gallary'


class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
            return self.model.objects.create(user=user_obj)


class CartAdd(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=CASCADE)
    product = models.ManyToManyField(Product, blank=True)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    update_stamp = models.DateTimeField(auto_now=True)
    is_order = models.BooleanField(default=False)
    objects = CartManager()

    def __str__(self):
        temp = str(self.id)
        return temp

    def get_id(self):
        return self.id

    def get_product(self):
        return self.product.all()

    def set_qty(self, qty):
        self.quantity = qty
        self.save()

    def set_total(self, t):
        self.total = t
        self.save()

    def get_total(self):
        return self.total

    def id_or_not(self):
        if (self.id is CartAdd.user):
            return True
        else:
            return False

    class Meta:
        db_table = 'Cart'


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('shipped', 'Shipped'),
    ('paid', 'Paid')
)
PAYMENT_MODE_CHOICE = (
    ('cod', 'cod'),
    ('paytm', 'paytm'),
)


class Order(models.Model):
    p_mode = models.CharField(
        max_length=255, default='cod', choices=PAYMENT_MODE_CHOICE)
    ostatus = models.CharField(
        max_length=255, default='created', choices=ORDER_STATUS_CHOICES)
    ocontactno = models.CharField(max_length=10, default='1')
    oaddress = models.CharField(max_length=255, blank=True)
    amount = models.IntegerField(default=1)
    odate = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(CartAdd, on_delete=CASCADE, default='None')
    made_by = models.ForeignKey(User, on_delete=CASCADE, default='None')
    order_id = models.CharField(
        unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.odate and self.id:
            self.order_id = self.odate.strftime(
                'PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'order'


class OrderDetails(models.Model):
    oquant = models.IntegerField(default=1)
    product = models.ManyToManyField(Product)
    order = models.OneToOneField(Order, on_delete=CASCADE)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_product(self):
        return self.product.all()

    class Meta:
        db_table = 'orderdetails'


class ItemRating(models.Model):
    Rnumber = models.IntegerField()
    title = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modefied = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def get_star(self):
        return self.Rnumber

    def set_data(self, rnumber, comment, product, title):
        self.Rnumber = rnumber
        self.comment = comment
        self.product = product
        self.title = title
        return 'done'

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'itemrating'
