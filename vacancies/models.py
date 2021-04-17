import datetime

from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField
from stepik_job_search.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR
# Create your models here.


class Company(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)
    location = models.CharField("Город", max_length=50)
    logo = models.ImageField("Логотип", upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True,)
    description = models.TextField("Описание")
    employee_count = models.IntegerField("Количество сотрудников")
    owner = models.OneToOneField(
        User,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        related_name='mycompnay',
        null=True,
        default=None,
    )

    def __str__(self):
        return f'{self.pk} {self.name}'

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Specialty(models.Model):
    code = models.CharField("Код", max_length=30, unique=True)
    title = models.CharField("Название", max_length=50)
    picture = models.ImageField("Картинка", upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Vacancy(models.Model):
    title = models.CharField("Название вакансии", max_length=60)
    specialty = models.ForeignKey(
        "Specialty",
        verbose_name="Специализация",
        on_delete=models.CASCADE,
        related_name="vacancies"
    )
    company = models.ForeignKey(
        "Company",
        verbose_name=" Компания ",
        on_delete=models.CASCADE,
        related_name="vacancies"
    )
    skills = models.TextField("Навыки")
    description = models.TextField("Текст")
    salary_min = models.IntegerField("Зарплата от")
    salary_max = models.IntegerField("Зарплата до")
    published_at = models.DateField("Опубликовано", default=datetime.date.today())

    def __str__(self):
        return f'{self.pk} {self.title} {self.published_at}'

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"


class Application(models.Model):
    written_username = models.CharField("Имя ", max_length=30)
    written_phone = PhoneNumberField("Телефон")
    written_cover_letter = models.TextField("Сопроводительное письмо")
    vacancy = models.ForeignKey("Vacancy", verbose_name="Вакансия", on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="applications")

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"

    def __str__(self):
        return f'Отклик от {self.written_username}'