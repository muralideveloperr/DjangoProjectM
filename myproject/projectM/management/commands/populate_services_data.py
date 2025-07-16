from projectM.models import Services
from django.core.management.base import BaseCommand
from typing import Any
import random


class Command(BaseCommand):
    help = 'This commands inserts services data'

    def handle(self, *args: Any, **kwargs: Any):
       Services.objects.all().delete()

       name = [
          'Resume Builder',
          'Chatbot',
          'Create Resume',
          'Library Management'
               ]
       description = [
          'Resume Builder is a dynamic and user-friendly web application built with Django that allows users to effortlessly create professional resumes. The platform guides users through a structured input process, enabling them to enter personal details, education, work experience, skills, and projects. Once completed, the system generates a polished, print-ready PDF version of the resume based on a pre-designed template.',
          'The Chatbot project is an interactive AI-based web application designed to simulate human-like conversations with users. Built using natural language processing (NLP) techniques and a Django/Flask backend, the chatbot can respond intelligently to queries, assist users, and automate simple tasks. It’s ideal for customer support, information delivery, or educational assistance.',
          "Describe your responsibilities and accomplishments in relationship to the job/organization, not the job/organization itself. Limit your description to the three or four most important points. Check out some of Steinbright's résumé samples to gather ideas on how to market your experiences and talents.",
          "A library management system is software that is designed to manage all the functions of a library. It helps librarian to maintain the database of new books and the books that are borrowed by members along with their due dates. This system completely automates all your library's activities."
          ]
       icon = [
          'bi bi-bounding-box-circles',
          'bi bi-chat-square-text',
          'bi bi-pencil-square',
          'bi bi-chat-square-text'
       ]
       icon_color = [
          'service-item item-red position-relative',
          'service-item item-pink position-relative',
          'service-item item-teal position-relative',
          'service-item item-pink position-relative'
       ]

       for name, description, icon, icon_color in zip(name, description, icon, icon_color):
          Services.objects.create(name=name, description=description, icon=icon, icon_color=icon_color)
       
       self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
        