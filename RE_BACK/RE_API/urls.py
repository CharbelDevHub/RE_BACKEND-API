from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('login', LoginAPIView.as_view()),
    path('agencies/', AgencyView.as_view(), name='agency-list-create'),  # For GET (list) and POST (create)
    path('agencies/<int:pk>/', AgencyView.as_view(), name='agency-detail'),  # For GET (retrieve), PUT (update), DELETE (delete)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
