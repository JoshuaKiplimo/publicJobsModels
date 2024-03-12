from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobDetailViewset, ObtainTokenView, company_counts, JobReviewViewSet

router = DefaultRouter()
router.register(r'jobdetails', JobDetailViewset)
router.register(r'reviews', JobReviewViewSet)

urlpatterns = [
    # ...
    path('', include(router.urls)),
    path('obtain_token/', ObtainTokenView.as_view(), name='obtain_token'),
    path('job_count/', company_counts, name='job_count'),
]

urlpatterns += router.urls