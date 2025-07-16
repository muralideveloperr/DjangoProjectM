from datetime import date
from django.utils import timezone
from django import forms
from .models import AddBook, ContactManager, ExpensesTracker, JobApplications, JobBoard, OnlinePollingSystem, PollOptions, QuizDetails, QuizQuestions, Resume,  ManageLibraryCard, ToDoList, UserAnswer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ResumeGeneratorForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, required=True)
    job_title = forms.CharField(label='Job Title', max_length=100, required=True)
    phone = forms.CharField(label='Phone', max_length=20, required=True)
    email = forms.EmailField(label='Email', required=True)
    profile_photo = forms.ImageField(label='Profile Photo', required=False)
    birthday = forms.DateField(label='Birthday', required=True)
    address = forms.CharField(label='Address', max_length=255)

    class Meta:
        model = Resume
        fields = ['name',
                  'job_title',
                  'phone',
                  'email',
                  'profile_photo',
                  'birthday',
                  'address',
                  'objective',
                  'projects'
                  ]
        
class ManageLibraryCardForm(forms.ModelForm):
    card_id = forms.CharField(label='Card ID', max_length=100, required=True)
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Phone', max_length=20, required=True)
    issued_date = forms.DateField(label='Issue Date', required=True)

    class Meta:
        model = ManageLibraryCard
        fields = [
            'card_id',
            'name',
            'email',
            'phone',
            'issued_date'
        ]

class AddBookForm(forms.ModelForm):
    class Meta:
        model = AddBook
        fields = [
            'book_title',
            'author',
            'published_date',
            'category'
        ]


class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpensesTracker
        fields = '__all__'

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label = 'First Name', max_length=100, required=True)
    last_name = forms.CharField(label = 'Last Name', max_length=100, required=True)
    email = forms.EmailField(label = 'Email', max_length=100, required=True)
    username = forms.CharField(label = 'Username', max_length=100, required=True)
    password = forms.CharField(label = 'Password', max_length=100, required=True)
    confirm_password = forms.CharField(label = 'Confirm Password', max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        
        if password and len(password) < 8 :
            raise forms.ValidationError("Password should contain at least 8 characters.")
        
class LoginForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length=100, required=True)
    password = forms.CharField(label = 'Password', max_length=100, required=True)

    def clean(self):
         cleaned_data = super().clean()

         username = cleaned_data.get('username')
         password = cleaned_data.get('password')

         if username and password:
             user = authenticate(username=username, password=password)

             if user is None:
                 raise forms.ValidationError("Invalid username or password")

class ToDoListForm(forms.ModelForm):
    task_name = forms.CharField(label='Task Name', max_length=100, required=True)
    deadline = forms.DateField(label='Deadline', required=True)

    class Meta:
        model = ToDoList
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data.get('deadline')
        #today = timezone.now().date()
        today = date.today()

        if deadline and deadline < today:
            raise forms.ValidationError("Deadline cannot be in the past.")
        
class ContactManagerForm(forms.ModelForm):
    class Meta:
        model = ContactManager
        fields = '__all__'

class JobBoardForm(forms.ModelForm):
    class Meta:
        model = JobBoard
        fields = '__all__'
        
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplications
        fields = '__all__'

class OnlinePollingSystemForm(forms.ModelForm):
    class Meta:
        model = OnlinePollingSystem
        fields = '__all__'
        exclude = ['total_votes', 'created_by']

class PollOptionsForm(forms.ModelForm):
    class Meta:
        model = PollOptions
        fields = ['option_text']

class QuizDetailsForm(forms.ModelForm):
    class Meta:
        model = QuizDetails
        fields = ['title', 'duration', 'description']

class QuizQuestionsForm(forms.ModelForm):
    class Meta:
        model = QuizQuestions
        fields = ['question_text', 'correct_option']

class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['selected_option']

    
    