import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_job_search.settings'
django.setup()

from data import jobs, companies, specialties  # noqa: E402.
from vacancies.models import Vacancy, Company, Specialty  # noqa: E402.


if __name__ == '__main__':
    Vacancy.objects.all().delete()
    Specialty.objects.all().delete()
    Company.objects.all().delete()

    for specialty in specialties:
        spec = Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
        )

    for company in companies:
        comp = Company.objects.create(
            name=company['title'],
            logo=company['logo'],
            employee_count=company['employee_count'],
            location=company['location'],
            description=company['description'],
        )

    for job in jobs:
        vacancy = Vacancy.objects.create(
            title=job['title'],
            company=Company.objects.get(id=job['company']),
            specialty=Specialty.objects.get(code=job['specialty']),
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )
