from django.urls import path
from user.views import CreateTestUsersAPIView, PopulateAddressDataAPIView, AddressListAPIView

urlpatterns = [
    path('create-test-users/', CreateTestUsersAPIView.as_view(), name='create-test-users'),
    path('populate-address-data/', PopulateAddressDataAPIView.as_view(), name='populate-address-data'),
    path('addresses/', AddressListAPIView.as_view(), name='address-list'),
]

