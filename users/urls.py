from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserApiViewSet, UserMeView

router = DefaultRouter()
router.register('users', UserApiViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', UserMeView.as_view(), name='user-me'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
