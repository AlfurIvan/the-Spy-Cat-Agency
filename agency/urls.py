from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, MissionViewSet

router = DefaultRouter()
router.register(r'spycats', SpyCatViewSet, basename='spycat')
router.register(r'missions', MissionViewSet, basename='mission')

urlpatterns = router.urls
