from projectM.models import About
from django.core.management.base import BaseCommand
from typing import Any
import random


class Command(BaseCommand):
    help = 'This commands inserts about data'

    def handle(self, *args: Any, **kwargs: Any):
       About.objects.all().delete()

       title = ['Software Developer']
       description = ['An effective job title wiil typically include a general term, the level of experience and any special requirements. The general term will optimize your job title to show up in a general search for jobs of the same nature. The level of experience will help you attract the most qualified applicants by outlining the amount of responsibility and prior knowledge required. And if your position is specialized, consider including the specialization in the job title as well. But avoid using internal titles, abbreviations or acronyms to make sure people understand what your job posting is before clicking.']
       birthday = ['1996-06-04']
       age = ['28']
       website = ['www.google.com']
       degree = ['Bachelor of Engineering']
       phone = ['8939490154']
       email = ['muralin4696@gmail.com']
       city = ['Chennai']
       country = ['India']
       freelance = ['Available']

       for title, birthday, age, website, degree, phone, email, city, country, freelance in zip(title, birthday, age, website, degree, phone, email, city, country, freelance):
          About.objects.create(title=title, birthday=birthday, age=age, website=website, degree=degree, phone=phone, email=email, city=city, country=country, freelance=freelance, description=description)
       
       self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
        