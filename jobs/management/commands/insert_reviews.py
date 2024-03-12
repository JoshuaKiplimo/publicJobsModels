


from django.core.management.base import BaseCommand
from jobs.models import JobReview

class Command(BaseCommand):
    help = 'Add or delete all reviews'


    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='add or delete')
        parser.add_argument('--start-id', type=int, help='Start of the ID range to delete')
        parser.add_argument('--end-id', type=int, help='End of the ID range to delete')

    def handle(self, *args, **kwargs):
        action = kwargs['action']
        if action == 'add':
            self.add_reviews()
        elif action == 'delete':
            start_id = kwargs.get('start_id')
            end_id = kwargs.get('end_id')
            if start_id is not None and end_id is not None:
                self.delete_reviews_range(start_id, end_id)
            else:
                self.delete_reviews()


    def add_reviews(self):
            reviews = [
                {
                    "reviewer_name": "Maria Sanchez",
                    "stars": 5,
                    "review": "VisJobs has been an incredible resource for my job search. Thanks to this platform, I secured a fantastic job in San Francisco that aligns perfectly with my skills and aspirations.",
                    "reviewer_career": "Software Engineer"
                },
                {
                    "reviewer_name": "Hiroki Tanaka",
                    "stars": 4,
                    "review": "I highly recommend VisJobs to any H1B job seeker. The platform made my job search in Silicon Valley much smoother, and I'm now thriving in my new role.",
                    "reviewer_career": "Data Scientist"
                },
                {
                    "reviewer_name": "Sophie Dubois",
                    "stars": 5,
                    "review": "Thanks to VisJobs, I found a job in New York City that offers a perfect balance between work and life. This platform is a game-changer for H1B job seekers!",
                    "reviewer_career": "Project Manager"
                },
                {
                    "reviewer_name": "Yuki Nakamura",
                    "stars": 5,
                    "review": "The platform helped me secure a job in NYC. It's user-friendly and effective. Highly recommended!",
                    "reviewer_career": "Graphic Designer"
                },
                {
                    "reviewer_name": "Pablo Ramirez",
                    "stars": 4,
                    "review": "I found a job in Texas thanks to this platform. It made my job search in the US much smoother.",
                    "reviewer_career": "Marketing Specialist"
                },
                {
                    "reviewer_name": "Anna Petrov",
                    "stars": 5,
                    "review": "Thanks to this platform, I found a job in Silicon Valley that I love. Highly recommend!",
                    "reviewer_career": "Software Developer"
                },
                {
                    "reviewer_name": "Luisa Fernandez",
                    "stars": 4,
                    "review": "The platform made my job search in the US much easier. Found a job in Chicago thanks to it.",
                    "reviewer_career": "Financial Analyst"
                },
                {
                    "reviewer_name": "Mohammed Ali",
                    "stars": 5,
                    "review": "The platform is great for H1B job seekers. Found a job in Florida and couldn't be happier.",
                    "reviewer_career": "IT Consultant"
                },
                {
                    "reviewer_name": "Mei Lin",
                    "stars": 4,
                    "review": "Thanks to this platform, I found a job in California that matched my skills perfectly.",
                    "reviewer_career": "Product Manager"
                },
                {
                    "reviewer_name": "Sofia Garcia",
                    "stars": 5,
                    "review": "The platform helped me find a job in Seattle that I love. It's easy to use and effective.",
                    "reviewer_career": "UX Designer"
                },
                {
                    "reviewer_name": "Jakub Novak",
                    "stars": 4,
                    "review": "Great platform for H1B job seekers. Found a job in Washington D.C. thanks to it!",
                    "reviewer_career": "Business Analyst"
                },
                {
                    "reviewer_name": "Fatemeh Mohammadi",
                    "stars": 5,
                    "review": "The platform is a lifesaver for H1B job seekers. Found a job in California within weeks!",
                    "reviewer_career": "Software Engineer"
                },
                {
                    "reviewer_name": "Carlos Hernandez",
                    "stars": 4,
                    "review": "The platform helped me find a job in Texas that matched my skills perfectly. Highly recommend!",
                    "reviewer_career": "Mechanical Engineer"
                },
                {
                    "reviewer_name": "Ling Wei",
                    "stars": 5,
                    "review": "Thanks to this platform, I found a job in NYC that I love. It's user-friendly and effective.",
                    "reviewer_career": "Data Scientist"
                },
                {
                    "reviewer_name": "Julia Kowalski",
                    "stars": 4,
                    "review": "The platform made my job search as an H1B visa holder much easier. Highly recommend!",
                    "reviewer_career": "Project Manager"
                },
                {
                    "reviewer_name": "David Kim",
                    "stars": 5,
                    "review": "The platform is a fantastic resource for H1B job seekers. Found multiple job opportunities!",
                    "reviewer_career": "Software Engineer"
                },
                {
                    "reviewer_name": "Elena Petrova",
                    "stars": 4,
                    "review": "The platform helped me navigate the job market in the US. Found a job in Chicago thanks to it.",
                    "reviewer_career": "Financial Analyst"
                },
                {
                    "reviewer_name": "Ahmed Khan",
                    "stars": 5,
                    "review": "Thanks to this platform, I landed a job in Silicon Valley. It's user-friendly and effective.",
                    "reviewer_career": "IT Consultant"
                },
                {
                    "reviewer_name": "Katarzyna Nowak",
                    "stars": 4,
                    "review": "The platform is a great resource for H1B job seekers. Found a job in Florida and couldn't be happier.",
                    "reviewer_career": "Marketing Specialist"
                },
                {
                    "reviewer_name": "Javier Fernandez",
                    "stars": 5,
                    "review": "The platform helped me find a job in Seattle that I love. It's easy to use and effective.",
                    "reviewer_career": "Software Developer"
                }
            ]

            for review_data in reviews:
                JobReview.objects.create(**review_data)
            self.stdout.write(self.style.SUCCESS('Reviews added successfully'))

    def delete_reviews(self):
        JobReview.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All reviews deleted'))
    def delete_reviews_range(self, start_id, end_id):
        JobReview.objects.filter(id__gte=start_id, id__lte=end_id).delete()
        self.stdout.write(self.style.SUCCESS(f'Reviews with IDs {start_id}-{end_id} deleted'))