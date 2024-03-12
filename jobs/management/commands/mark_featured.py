from django.core.management.base import BaseCommand
from jobs.models import JobDetail
from random import shuffle

class Command(BaseCommand):
    help = 'Marks all JOB_ISFEATURED to False and selects random jobs with values in city, state, country, min_salary, max_salary, and remote, then marks job_isfeatured as True'

    def handle(self, *args, **kwargs):
        # Mark all JOB_ISFEATURED to False
        JobDetail.objects.update(job_isFeatured=False)

        # Select all jobs with values in city, state, country, min_salary, max_salary, and remote
        jobs_to_feature = JobDetail.objects.exclude(job_city__isnull=True).exclude(job_state__isnull=True).exclude(job_country__isnull=True).exclude(min_salary__isnull=True).exclude(max_salary__isnull=True).filter(job_remote=True)

        # Shuffle the queryset
        jobs_to_feature = list(jobs_to_feature)
        shuffle(jobs_to_feature)

        # Select the first 200 jobs
        jobs_to_feature = jobs_to_feature[:200]

        # Mark job_isFeatured as True for selected jobs
        for job in jobs_to_feature:
            job.job_isFeatured = True
            job.save()

        self.stdout.write(self.style.SUCCESS('Successfully marked featured jobs'))
