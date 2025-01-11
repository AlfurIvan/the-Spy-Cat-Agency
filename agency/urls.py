from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, MissionViewSet, TargetViewSet

router = DefaultRouter()
router.register(r'spycats', SpyCatViewSet, basename='spycat')
router.register(r'missions', MissionViewSet, basename='mission')
router.register(r'targets', TargetViewSet, basename='target')

urlpatterns = router.urls
