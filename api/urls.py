from rest_framework.routers import DefaultRouter

from api.views import MaterialViewSet

router = DefaultRouter()
router.register(r"material", MaterialViewSet)

urlpatterns = router.urls
