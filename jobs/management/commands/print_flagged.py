from django.core.management.base import BaseCommand
from jobs.models import JobDetail

class Command(BaseCommand):
    help = 'Prints all flagged job entries'

    def handle(self, *args, **options):
        # Filter jobs that are flagged
        flagged_jobs = JobDetail.objects.filter(job_isFlagged=True)

        if not flagged_jobs.exists():
            self.stdout.write(self.style.WARNING('No flagged jobs found.'))
            return

        # Print details for each flagged job
        for job in flagged_jobs:
            self.stdout.write(f"Job ID: {job.job_id}, Job Name: {job.job_name}, Company Name: {job.company_name}, Salary: {job.job_salary}, Flagged: {job.job_isFlagged}")

        self.stdout.write(self.style.SUCCESS(f'Total flagged jobs: {flagged_jobs.count()}'))
