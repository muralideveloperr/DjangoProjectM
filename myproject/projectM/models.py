from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class About(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    birthday = models.DateField()
    age = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    freelance = models.CharField(max_length=100)
    #profile_img = models.ImageField(null=True)

    def __str__(self):
        return self.title
    
class Services(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True)
    icon = models.CharField(max_length=100, null=True)
    icon_color = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Resume(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profile_photo = models.ImageField(null=True, upload_to='resume/profile_photos')
    address = models.CharField(max_length=255)
    birthday = models.DateField()
    education = models.TextField()
    language = models.CharField(max_length=100)
    objective = models.TextField()
    work_experience = models.TextField()
    skills = models.TextField()
    certifications = models.TextField()
    projects = models.TextField()
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ChatbotRules(models.Model):
    keyword = models.CharField(max_length=100)
    response = models.TextField()

    def __str__(self):
        return self.keyword

class ManageLibraryCard(models.Model):
    card_id = models.CharField(max_length=100,  unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    issued_date = models.DateField()

    def __str__(self):
        return self.card_id
    
class AddBook(models.Model):
    book_title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    category = models.CharField(max_length=100)
    borrowed = models.BooleanField(default=False)
    borrowed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    borrowed_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.book_title
    
class ExpenseCategory(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class ExpensesTracker(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.description
    
class ToDoList(models.Model):
    task_name = models.CharField(max_length=100)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name
    
class ContactManager(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class JobType(models.Model):
    job_type = models.CharField(max_length=100)

    def __str__(self):
        return self.job_type
    
class JobBoard(models.Model):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    job_description = models.TextField()
    requirements = models.TextField()
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.job_title
    
class JobApplications(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    resume=models.FileField(upload_to='job_board/job_applications/resumes/')
    cover_letter=models.TextField()

    def __str__(self):
        return self.name
    
class OnlinePollingSystem(models.Model):
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_votes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question
    
class PollOptions(models.Model):
    poll = models.ForeignKey(OnlinePollingSystem, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.option_text
    
class QuizDetails(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    number_of_questions = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title
    
class QuizQuestions(models.Model):
    quiz = models.ForeignKey(QuizDetails, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    total_marks = models.PositiveIntegerField(default=0)
    correct_option = models.ForeignKey('QuizOptions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question_text

class QuizOptions(models.Model):
    question = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizDetails, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOptions, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(default=timezone.now)
    is_correct = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"

class QuizLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    quiz_taken = models.ForeignKey(QuizDetails, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score'] # Order by score in descending order

    def __str__(self):
        return f"{self.user.username} - {self.score}"
    
class QuizParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"



    
