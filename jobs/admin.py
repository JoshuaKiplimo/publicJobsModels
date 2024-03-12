from django.contrib import admin
from .models import JobDetail, JobReview
from unfold.admin import ModelAdmin
from django.db.models import Case, When, Value, IntegerField

class JobDetailAdmin(ModelAdmin):
    list_display = ('job_isFlagged', 'job_isFeatured', 'job_name', 'company_name', 'date_posted', 'job_id', 'job_salary', 'min_salary', 'max_salary')
    search_fields = ('job_id', 'job_name', 'company_name', 'job_isFlagged', 'job_isFeatured')
    list_filter = ('job_isFeatured', 'job_isFlagged', 'job_city', 'job_state', 'job_country')


class JobReviewAdmin(ModelAdmin):
    list_display = ('reviewer_name', 'review', 'stars', 'reviewer_career')

admin.site.register(JobDetail, JobDetailAdmin)
admin.site.register(JobReview, JobReviewAdmin)
