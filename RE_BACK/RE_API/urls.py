from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('login', LoginAPIView.as_view()),
    path('signup', RegisterAPIView.as_view()),
    path('agencies/', AgencyView.as_view(), name='agency-list-create'),  # For GET (list) and POST (create)
    path('agencies/agency-details', AgencyDetailsView.as_view(), name='agency-detail'),  # For GET (retrieve), PUT (update), DELETE (delete)
    path('agencies/agency-update', AgencyUpdateView.as_view(), name='agency-update'),  # For GET (retrieve), PUT (update), DELETE (delete)
    path('cities/', CityListView.as_view()),
    path('agencies/agency-delete', AgencyDeleteView.as_view(), name='agency-delete'),
    path('agencies/agency-create', AgencyCreateView.as_view()),

    path('user-info/update', UpdateUserAPIView.as_view()),
    path('contracts/GetAll', ContractGetAllView.as_view()),    
    path('contracts/GetPaymentsByContractId', GetContractPaymentsView.as_view()),
    path('properties/', PropertyListView.as_view()),
    path('properties/property-delete', PropertyDeleteView.as_view()),   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
