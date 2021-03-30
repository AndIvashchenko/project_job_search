import datetime

from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()

    def __str__(self):
        return f'{self.pk} {self.name}'


class Specialty(models.Model):
    code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=50)
    picture = models.URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return self.code


class Vacancy(models.Model):
    title = models.CharField(max_length=60)
    specialty = models.ForeignKey("Specialty", on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(default=datetime.date.today())

    def __str__(self):
        return f'{self.pk} {self.title} {self.published_at}'
