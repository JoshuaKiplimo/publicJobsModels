from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token  # Add this import
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import JobDetail
from .serializers import JobDetailSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.db import IntegrityError
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import django_filters
from .models import JobDetail
from rest_framework import filters
from rest_framework import viewsets
from .models import JobReview
from .serializers import JobReviewSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import render
from .models import JobDetail
from django.contrib.admin.views.decorators import staff_member_required
from random import shuffle

@api_view(['GET'])
def company_counts(request):
    # Count entries for each company
    green_house_count = JobDetail.objects.filter(job_api_company='gree_house').count()
    lever_count = JobDetail.objects.filter(job_api_company='lever').count()
    workable_count = JobDetail.objects.filter(job_api_company='workable').count()

    return Response({
        'green_house_count': green_house_count,
        'lever_count': lever_count,
        'workable_count': workable_count,
    })

class CustomPagination(PageNumberPagination):
    
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        
        next_page = int(next_url.split('page=')[1]) if next_url and 'page=' in next_url else None
        previous_page = int(previous_url.split('page=')[1]) if previous_url and 'page=' in previous_url else None

        return Response({
            'next': next_page,
            'previous': previous_page,
            'results': data
        })

class JobReviewViewSet(viewsets.ModelViewSet):
    queryset = JobReview.objects.all()
    serializer_class = JobReviewSerializer

class JobDetailFilter(django_filters.FilterSet):
    job_name = django_filters.CharFilter(lookup_expr='icontains')
    job_city = django_filters.CharFilter(lookup_expr='icontains')
    job_state = django_filters.CharFilter(lookup_expr='icontains')
    job_country = django_filters.CharFilter(lookup_expr='icontains')
    job_general_category = django_filters.CharFilter(lookup_expr='icontains')
    job_experience_level = django_filters.CharFilter(lookup_expr='icontains')
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    job_commitment = django_filters.CharFilter(lookup_expr='icontains')
    team = django_filters.CharFilter(lookup_expr='icontains')
    department = django_filters.CharFilter(lookup_expr='icontains')
    work_place_type = django_filters.CharFilter(lookup_expr='icontains')
    job_scrap_version = django_filters.CharFilter(lookup_expr='icontains')

    # Boolean fields
    job_remote = django_filters.BooleanFilter()
    job_isFeatured= django_filters.BooleanFilter()
    job_isFlagged = django_filters.BooleanFilter()
    job_hybrid = django_filters.BooleanFilter()
    job_sponsorship = django_filters.BooleanFilter()
    sponsorship_friendly = django_filters.BooleanFilter()

    # filtering by text content
    job_skills = django_filters.CharFilter(lookup_expr='icontains')
    job_description = django_filters.CharFilter(lookup_expr='icontains')
    min_salary = django_filters.NumberFilter(lookup_expr='gte')
    max_salary = django_filters.NumberFilter(lookup_expr='lte')
    
    class Meta:
        model = JobDetail
        fields = {
            'job_api_company': ['exact', 'icontains'],
            'min_salary': ['exact', 'gte', 'lte'],  # New filters for min_salary
            'max_salary': ['exact', 'gte', 'lte'],  # New filters for max_salary
            'job_yoe': ['exact', 'icontains'],
            'job_id': ['exact', 'icontains'],
            'job_location_list': ['exact', 'icontains'],
            'job_city': ['exact', 'icontains'],
            'job_state': ['exact', 'icontains'],
            'job_country': ['exact', 'icontains'],
            'job_general_category': ['exact', 'icontains'],
            'job_experience_level': ['exact', 'icontains'],
            'job_remote': ['exact'],
            'job_hybrid': ['exact'],
            'job_skills': ['exact', 'icontains'],
            'job_description': ['exact', 'icontains'],
            'company_name': ['exact', 'icontains'],
            'date_posted': ['exact', 'gte', 'lte'],  # Range filtering
            'job_apply_link': ['exact', 'icontains'],
            'job_commitment': ['exact', 'icontains'],
            'team': ['exact', 'icontains'],
            'department': ['exact', 'icontains'],
            'work_place_type': ['exact', 'icontains'],
            'job_sponsorship': ['exact'],
            'sponsorship_friendly': ['exact'],
        }

    def qs_random_order(self):
        queryset = self.qs
        queryset = list(queryset)
        shuffle(queryset)
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if getattr(self.Meta, 'random_order', False):
            queryset = self.qs_random_order()
        return queryset

class JobDetailViewset(viewsets.ModelViewSet):
    
    queryset = JobDetail.objects.all()
    
    serializer_class = JobDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]  # Add this line
    filterset_class = JobDetailFilter
    pagination_class = CustomPagination 

    @action(detail=True, methods=['patch'], url_path='flag')
    def flag_job(self, request, pk=None):
        try:
            job = JobDetail.objects.get(job_id=pk)  # Assuming job_id is the field you're using to look up the job
        except JobDetail.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        job.job_isFlagged = True
        job.save()
        return Response({'message': 'Job flagged successfully'})

    @action(detail=False, methods=['get'])
    def get_job(self, request):
        job_id = request.query_params.get('job_id')
        job = get_object_or_404(JobDetail, job_id=job_id)
        serializer = JobDetailSerializer(job)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Paginate the queryset if pagination is configured
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If pagination is not configured, serialize and return the whole queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response({'error': 'Job with the same job_id already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            import traceback
            # print(traceback.print_exc())
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data['url'])}
        except (TypeError, KeyError):
            return {}
        
class ObtainTokenView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
@staff_member_required
def metrics(request):
    count = JobDetail.objects.filter(job_isFlagged=True).count()
    return render(request, "admin/flagged.html", {"count": count})
