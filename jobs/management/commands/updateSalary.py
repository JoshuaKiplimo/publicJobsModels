from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import serialize
from django.db.models import F
from jobs.models import JobDetail
import json

class Command(BaseCommand):
    help = 'Update min and max salary fields for jobs with a salary value'

    def handle(self, *args, **options):
        # Filter jobs by non-empty job_salary
        jobs_with_salary = JobDetail.objects.exclude(job_salary__isnull=True).exclude(job_salary='')

        # Process each job
        for job in jobs_with_salary:
            job_salary_str = job.job_salary

            # Skip if salary string is effectively null
            if job_salary_str.lower() == "null":
                continue

            if len(job_salary_str) <= 2:
                # Assume hourly wage and calculate annual salary
                hourly_wage = int(job_salary_str)
                annual_salary = hourly_wage * 2080
                job.min_salary = job.max_salary = annual_salary

            elif len(job_salary_str) == 4:
                # Assume monthly wage and calculate annual salary
                monthly_wage = int(job_salary_str)
                annual_salary = monthly_wage * 12
                job.min_salary = job.max_salary = annual_salary

            elif len(job_salary_str) > 15:
                # Mark as flagged if salary string is too long
                job.job_isFlagged = True

            else:
                salaries = job_salary_str.replace(',', '').split('-')
                if len(salaries) == 1:
                    # Singular salary
                    min_salary = max_salary = int(salaries[0])
                else:
                    # Salary range
                    min_salary, max_salary = map(int, salaries)

                    if max_salary < min_salary:
                        # Flag if max salary is less than min salary
                        job.job_isFlagged = True
                        continue

                job.min_salary = min_salary
                job.max_salary = max_salary

            # Save updates to job
            try:
                job.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated job: {job.job_id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to update job: {job.job_id}, Error: {str(e)}'))
