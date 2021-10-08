from rest_framework import routers
from core.views import *

router = routers.DefaultRouter()
router.register(r'clients', ClientsViewSet, basename='VClients')
router.register(r'fixed_prices', FixedPricesViewSet, basename='VFixedPrices')
router.register(r'orders', OrdersViewSet)
router.register(r'payment_conditions', PaymentConditionsViewSet, basename='VPaymentConditions')
router.register(r'policies', PoliciesViewSet, basename='PoliciesViewSet')
router.register(r'products', ProductsViewSet, basename='ProductsViewSet')
router.register(r'sellers', SellersViewSet, basename='VSellers')
router.register(r'seller_clients', SellerClientsViewSet, basename='VSellerClients')
router.register(r'titles', TitlesViewSet, basename='VTitles')
router.register(r'order', OrderHeaderViewSet, basename='OrderHeader')