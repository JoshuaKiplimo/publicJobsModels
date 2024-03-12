from django.db import models
import json

class JobReview(models.Model):
    # Name of the user leaving the review
    reviewer_name = models.CharField(max_length=255, null=True)

    # The main content of the review
    review = models.TextField(null=True)

    # Rating out of 5 stars
    STARS_CHOICES = [(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
    stars = models.IntegerField(choices=STARS_CHOICES, default=0)

    # Career or job title of the reviewer
    reviewer_career = models.CharField(max_length=255, null=True,  default="Unknown Career")

# Create your models here.
class JobDetail(models.Model):
    # Unique identifier for the job
    job_id = models.CharField(max_length=255, unique=True)
    #Job salary
    job_salary = models.CharField(verbose_name="Minimum Salary",max_length=255, null=True, blank=True)
    min_salary = models.IntegerField(verbose_name="Minimum Salary", null=True, blank=True)
    max_salary = models.IntegerField(verbose_name="Maximum Salary", null=True, blank=True)
    #If job will be a featured job
    job_isFeatured = models.BooleanField(default=False)
    #If job will be a featured job
    job_isFlagged = models.BooleanField(default=False)
    # Name of the job
    job_name = models.CharField(max_length=255, null=True, blank=True)
    # List of job locations
    job_location_list = models.TextField(null=True, blank=True)
    # City where the job is located
    job_city = models.CharField(max_length=255, null=True, blank=True)
    # State where the job is located
    job_state = models.CharField(max_length=255, null=True, blank=True)
    # Country where the job is located
    job_country = models.CharField(max_length=255, null=True, blank=True)
    # General category of the job
    job_general_category = models.CharField(max_length=255, null=True, blank=True)
    # Years of experience required for the job
    job_yoe = models.CharField(max_length=255, null=True, blank=True)
    # Experience level of the job
    job_experience_level = models.CharField(max_length=255, null=True, blank=True)
    # Estimated salary for the jobj
    # Whether the job allows remote work (True/False)
    job_remote = models.BooleanField(default=False)
    # Whether the job allows hybrid work (True/False)
    job_hybrid = models.BooleanField(default=False)
    # Skills required for the job
    job_skills = models.TextField(null=True, blank=True)
    # Description of the job
    job_description = models.TextField(null=True, blank=True)
    # Name of the company offering the job
    company_name = models.CharField(max_length=255)
    # Date when the job was posted
    date_posted = models.DateTimeField(null=True, blank=True)
    # Link to apply for the job
    job_apply_link = models.CharField(max_length=255, blank=True)
    # Company information from the job API
    job_api_company = models.CharField(max_length=255, null=True, blank=True)
    # Commitment level for the job
    job_commitment = models.CharField(max_length=255, null=True, blank=True)
    # Team associated with the job
    team = models.CharField(max_length=255, null=True, blank=True)
    # Department associated with the job
    department = models.CharField(max_length=255, null=True, blank=True)
    # Type of workplace for the job
    work_place_type = models.CharField(max_length=255, null=True, blank=True)
    # Whether the job offers sponsorship (True/False)
    job_sponsorship = models.BooleanField(default=False)
    # Whether the job is sponsorship-friendly (True/False)
    sponsorship_friendly = models.BooleanField(default=False)
    # Version of the scrap file used to collect the job information
    # Version starts from '1.0' and updates with every new scrap version being pushed to remote db
    # This keeps track of the scrap version 
    job_scrap_version = models.CharField(max_length=255, null=True, blank=True)
  

    def set_job_location(self, location_data):
        self.job_location_list = json.dumps(location_data)

    def get_job_location(self):
        try:
            return json.loads(self.job_location_list) if self.job_location_list else None
        except json.JSONDecodeError:
            return None


    def __str__(self) -> str:
        return self.job_name

    class Meta:
        ordering = ['date_posted']
