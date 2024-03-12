# job_api/serializers.py
from rest_framework import serializers
from .models import JobDetail, JobReview
import json
class JobReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobReview
        fields = '__all__'

class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        exclude = ['job_api_company', 'job_scrap_version', 'job_location_list']

    def to_representation(self, instance):
         data = super().to_representation(instance)
         request = self.context.get('request')

         if request and not request.user.is_staff:
            # For non-staff users, remove specific fields
            excluded_fields = ['job_api_company', 'job_scrap_version', 'job_location_list']
            for field in excluded_fields:
                data.pop(field, None)  # Use pop to remove the fields, None is default if field does not exist

         return data

    def to_internal_value(self, data):
        # Convert the string representation to a Python list
        if isinstance(data.get('job_location_list'), list):
            data['job_location_list'] = json.dumps(data['job_location_list'])
        elif isinstance(data.get('job_location_list'), str):
            data['job_location_list'] = json.loads(data['job_location_list'])
        return super().to_internal_value(data)

    def create(self, validated_data):
        job_locationlist = validated_data.pop('job_location_list', None)
        instance = super().create(validated_data)
        if job_locationlist:
            instance.set_job_location(job_locationlist)
        instance.save()
        return instance


    
class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
