from rest_framework import serializers
from core.models import *

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VClients
        fields = '__all__'

class FixedPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VFixedPrices
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = VOrders
        fields = '__all__'

class PaymentConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPaymentConditions
        fields = '__all__'

class PoliciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPolicies
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VProducts
        fields = '__all__'

class SellersSerializer(serializers.ModelSerializer):
    class Meta:
        model = VSellers
        fields = [
            'company',
            'code',
            'supervisor'
        ]

class SellerClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VSellerClients
        fields = '__all__'

class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VTitles
        fields = '__all__'

class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    sellers = serializers.CharField()

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = [
            'branch',
            'company',
            'description',
            'discount',
            'fixed_price',
            'lot',
            'original_price',
            'price',
            'product',
            'promotional',
            'quantity',
            'total'
        ]

class OrderHeaderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)

    class Meta:
        model = OrderHeader
        fields = [
            'date',
            'app_id',
            'payment_condition',
            'import_status',
            'unique',
            'pedpalm',
            'items'
        ]