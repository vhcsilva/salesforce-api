from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.models import *
from core.classes import ProfileClass
from core.serializers import *
from core.utils import *

from datetime import datetime

class ClientsViewSet(viewsets.ModelViewSet):
    serializer_class = ClientsSerializer

    def get_queryset(self):
        user = self.request.user
        allowed_companies = user.profile.get_allowed_companies_branchs()

        branches = arr_to_arr(allowed_companies.values())

        queryset = VClients.objects.filter(company__in=allowed_companies.keys(), branch__in=branches)

        return queryset

class FixedPricesViewSet(viewsets.ModelViewSet):
    serializer_class = FixedPricesSerializer

    def get_queryset(self):
        user = self.request.user
        allowed_companies = user.profile.get_allowed_companies_branchs()

        branches = arr_to_arr(allowed_companies.values())

        queryset = VFixedPrices.objects.filter(company__in=allowed_companies.keys(), branch__in=branches)

        return queryset

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = VOrders.objects.all()

    serializer_class = OrdersSerializer

class PaymentConditionsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentConditionsSerializer

    def get_queryset(self):
        user = self.request.user
        allowed_companies = user.profile.get_allowed_companies_branchs()

        queryset = VPaymentConditions.objects.filter(company__in=allowed_companies.keys())

        return queryset

class PoliciesViewSet(viewsets.ModelViewSet):
    serializer_class = PoliciesSerializer
    
    def get_queryset(self):
        user = self.request.user
        allowed_companies = user.profile.get_allowed_companies_branchs()

        queryset = VPolicies.objects.filter(company__in=allowed_companies.keys())

        return queryset

class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        user = self.request.user
        allowed_companies = user.profile.get_allowed_companies_branchs()

        branches = arr_to_arr(allowed_companies.values())

        queryset = VProducts.objects.filter(company__in=allowed_companies.keys(), branch__in=branches)

        return queryset

class SellersViewSet(viewsets.ModelViewSet):
    #serializer_class = SellersSerializer
    serializer_class = ProfileSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')

        user = User.objects.get(username=username)

        queryset = VSellers.objects.filter(cgc=user.profile.cgc)

        sellers = SellersSerializer(queryset, many=True)
        sellers = [{'code': s['code'], 'company': s['company'], 'supervisor': s['supervisor']} for s in sellers.data]

        return [ProfileClass(user.first_name + ' ' + user.last_name, user.email, sellers)]

class SellerClientsViewSet(viewsets.ModelViewSet):
    serializer_class = SellerClientsSerializer

    def get_queryset(self):
        client = self.request.query_params.get('client')

        queryset = VSellerClients.objects.filter()

        return queryset

class TitlesViewSet(viewsets.ModelViewSet):
    serializer_class = TitlesSerializer

    def get_queryset(self):
        client = self.request.query_params.get('client')

        queryset = VTitles.objects.filter(cgc=client).order_by('real_due_date')

        return queryset

class OrderHeaderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderHeaderSerializer
    
    def get_queryset(self):
        date = self.request.query_params.get('date')
        user = self.request.user

        headers = OrderHeader.objects.filter(user_id=user.id, date=date)

        return headers

    def create(self, request):
        user = request.user
        header = request.data['header']
        items = request.data['items']

        try:
            order_header = OrderHeader()
            order_header.date = datetime.now()
            order_header.app_id = header['app_id']
            order_header.status = 'INI'
            order_header.client_cgc = header['client_cgc']
            order_header.seller_cgc = user.profile.cgc
            order_header.payment_condition = header['payment_condition']
            order_header.unique = header['unique']
            order_header.obs = header['obs']
            order_header.user = user
            order_header.save()
            
            order_header.pedpalm = str(order_header.app_id)[5:12] + str(order_header.id) + str(order_header.user.id) + 'TEL'
            order_header.save()

            for item in items:
                order_item = OrderItems()
                order_item.company = item['company']
                order_item.branch = item['branch']
                order_item.description = item['description']
                order_item.product = item['product']
                order_item.promotional = item['promotional']
                order_item.fixed_price = item['fixed_price']
                order_item.quantity = item['quantity']
                order_item.discount = item['discount']
                order_item.original_price = item['original_price']
                order_item.price = item['price']
                order_item.lot = item['lot']
                order_item.total = item['total']
                order_item.order = order_header
                order_item.save()
            
            return Response(order_header.pedpalm, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('ERROR', status=status.HTTP_400_BAD_REQUEST)



class OrderItemsViewSet(viewsets.ModelViewSet):
    serializer_class = OrderHeaderSerializer
    
    def get_queryset(self):
        user = self.request.user
        order_id = self.request.query_params.get('order_id')

        items = OrderItems.objects.filter(order__user_id=user.id, order_id=order_id)

        return items