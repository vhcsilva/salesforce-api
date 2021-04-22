from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cgc = models.CharField(max_length=11, blank=True, null=True)

    def get_allowed_companies_branchs(self):
        allowed  = {}
        permissions = self.user.get_all_permissions()

        if 'auth.asa_branca_sergipe' in permissions or 'auth.asa_branca_alagoas' in permissions:
            allowed['01'] = []

            if 'auth.asa_branca_sergipe' in permissions:
                allowed['01'].append('02')
                allowed['01'].append('14')
            
            if 'auth.asa_branca_alagoas' in permissions:
                allowed['01'].append('00')
                allowed['01'].append('06')

        if 'auth.maceio_distribuidora' in permissions:
            allowed['08'] = []
            allowed['08'].append('00')
            allowed['08'].append('02')
        
        return allowed

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class VClients(models.Model):
    recno = models.IntegerField()
    company = models.CharField(max_length=2)
    branch = models.CharField(max_length=2)
    code = models.CharField(max_length=6, blank=True, null=True)
    store = models.CharField(max_length=2)
    name = models.CharField(max_length=40, blank=True, null=True)
    fantasy_name = models.CharField(max_length=40, blank=True, null=True)
    person_type = models.CharField(max_length=1)
    channel = models.CharField(max_length=2)
    client_type = models.CharField(max_length=1)
    cgc = models.CharField(max_length=14, blank=True, null=True)
    client_group = models.CharField(max_length=6)
    risk = models.CharField(max_length=1)
    payment_condition = models.CharField(max_length=3)
    credit_limit = models.FloatField()
    saldup = models.FloatField()
    salpedl = models.FloatField()
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=114, blank=True, null=True)
    last_order = models.CharField(max_length=1)
    able_to_buy = models.CharField(max_length=1)
    xantibi = models.CharField(max_length=1)
    xcorrel = models.CharField(max_length=1)
    xcosmet = models.CharField(max_length=1)
    xhigien = models.CharField(max_length=1)
    xmecoes = models.CharField(max_length=1)
    xmedica = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'V_CLIENTS'


class VFixedPrices(models.Model):
    recno = models.IntegerField()
    company = models.CharField(max_length=2)
    branch = models.CharField(max_length=2)
    client = models.CharField(max_length=6)
    store = models.CharField(max_length=2)
    product = models.CharField(max_length=6)
    price = models.FloatField()
    supervisor = models.CharField(max_length=6)
    seller = models.CharField(max_length=6)
    plpag = models.CharField(max_length=3)
    client_group = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'V_FIXED_PRICES'


class VOrders(models.Model):
    company = models.CharField(max_length=2)
    order = models.CharField(max_length=6)
    client = models.CharField(max_length=14, blank=True, null=True)
    emission = models.CharField(max_length=8)
    seller = models.CharField(max_length=6)
    supervisor = models.CharField(max_length=6)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_ORDERS'


class VPaymentConditions(models.Model):
    company = models.CharField(max_length=2)
    code = models.CharField(max_length=3)
    description = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'V_PAYMENT_CONDITIONS'


class VPolicies(models.Model):
    recno = models.IntegerField()
    company = models.CharField(max_length=2)
    start_date = models.CharField(max_length=8)
    end_date = models.CharField(max_length=8)
    state = models.CharField(max_length=2, blank=True, null=True)
    code = models.CharField(max_length=8)
    description = models.CharField(max_length=50, blank=True, null=True)
    client = models.CharField(max_length=6, blank=True, null=True)
    store = models.CharField(max_length=2, blank=True, null=True)
    product = models.CharField(max_length=6, blank=True, null=True)
    category = models.CharField(max_length=3, blank=True, null=True)
    subcategory = models.CharField(max_length=3, blank=True, null=True)
    provider = models.CharField(max_length=6, blank=True, null=True)
    discount_se = models.FloatField()
    fixed_price_se = models.FloatField()
    seller = models.CharField(max_length=6, blank=True, null=True)
    supervisor = models.CharField(max_length=6, blank=True, null=True)
    minimum_quantity = models.FloatField()
    maximum_quantity = models.FloatField()
    discount = models.FloatField()
    fixed_price = models.FloatField()
    minimum_value = models.FloatField()
    maximum_value = models.FloatField()
    type = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_POLICIES'


class VProducts(models.Model):
    recno = models.IntegerField()
    company = models.CharField(max_length=2)
    branch = models.CharField(max_length=2)
    code = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    active_principle = models.CharField(max_length=100)
    ean = models.CharField(max_length=15, blank=True, null=True)
    group = models.CharField(max_length=4)
    category = models.CharField(max_length=3)
    subcategory = models.CharField(max_length=3)
    price = models.FloatField()
    promotional = models.CharField(max_length=1)
    unity = models.CharField(max_length=5)
    model = models.CharField(max_length=15, blank=True, null=True)
    balance = models.FloatField()
    provider = models.CharField(max_length=8)
    lot = models.CharField(max_length=18)
    due_date = models.CharField(max_length=8)
    multiple = models.FloatField()
    next_due_date = models.CharField(max_length=8, blank=True, null=True)
    taxes = models.FloatField()

    class Meta:
        managed = False
        db_table = 'V_PRODUCTS'


class VSellers(models.Model):
    company = models.CharField(max_length=2)
    branch = models.CharField(max_length=2)
    code = models.CharField(max_length=6)
    supervisor = models.CharField(max_length=6)
    cgc = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'V_SELLERS'


class VSellerClients(models.Model):
    company = models.CharField(max_length=2)
    branch = models.CharField(max_length=2)
    seller = models.CharField(max_length=6, blank=True, null=True)
    supervisor = models.CharField(max_length=6)
    client = models.CharField(max_length=14)
    status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'V_SELLER_CLIENTS'


class VTitles(models.Model):
    company = models.CharField(max_length=2)
    branch = models.CharField(max_length=2)
    cgc = models.CharField(max_length=14)
    client = models.CharField(max_length=6)
    store = models.CharField(max_length=2)
    prefix = models.CharField(max_length=3)
    title = models.CharField(max_length=9)
    parcel = models.CharField(max_length=3)
    type = models.CharField(max_length=3)
    emission = models.CharField(max_length=8)
    due_date = models.CharField(max_length=8)
    real_due_date = models.CharField(max_length=8)
    value = models.FloatField()
    pending = models.FloatField()
    history = models.CharField(max_length=40)
    # Field name made lowercase.
    frv_descri = models.CharField(db_column='FRV_DESCRI', max_length=40)

    class Meta:
        managed = False
        db_table = 'V_TITLES'


class OrderHeader(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    import_date = models.DateField(blank=True, null=True)
    app_id = models.CharField(unique=True, max_length=255)
    pedpalm = models.CharField(max_length=255, null=False, blank=True, default='')
    status = models.CharField(max_length=255)
    import_status = models.CharField(max_length=255, blank=True, null=True)
    client_cgc = models.CharField(max_length=20)
    seller_cgc = models.CharField(max_length=20)
    payment_condition = models.CharField(max_length=255)
    user = models.ForeignKey(User, models.DO_NOTHING)
    obs = models.CharField(max_length=255, blank=True, null=False, default='')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    operation_desc = models.CharField(max_length=4000, blank=True, null=True)
    operation_technical_desc = models.CharField(
        max_length=4000, blank=True, null=True)
    unique = models.CharField(max_length=12)

    class Meta:
        db_table = 'order_header'


class OrderItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.CharField(max_length=2)
    branch = models.CharField(max_length=2)
    description = models.CharField(max_length=255)
    product = models.CharField(max_length=6)
    promotional = models.CharField(max_length=255)
    fixed_price = models.BooleanField()
    quantity = models.FloatField()
    discount = models.FloatField()
    original_price = models.FloatField()
    price = models.FloatField()
    total = models.FloatField()
    order = models.ForeignKey(OrderHeader, models.DO_NOTHING, related_name='items')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    lot = models.CharField(max_length=255)

    class Meta:
        db_table = 'order_items'
