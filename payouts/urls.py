from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayoutViewSet

router = DefaultRouter()
router.register(r'payouts', PayoutViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
