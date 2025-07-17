from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
import requests
from projectM.models import About, Services, ChatbotRules
from projectM.forms import AddBookForm, AddExpenseForm, ContactManagerForm, JobApplicationForm, JobBoardForm, LoginForm, ManageLibraryCardForm, OnlinePollingSystemForm, PollOptionsForm, QuizDetailsForm, QuizQuestionsForm, ResumeGeneratorForm, RegisterForm, ToDoListForm, UserAnswerForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import AddBook, ContactManager, ExpenseCategory, ExpensesTracker, JobBoard, JobType, ManageLibraryCard, OnlinePollingSystem, PollOptions, QuizDetails, QuizLeaderboard, QuizOptions, QuizParticipants, QuizQuestions, Resume, ToDoList, UserAnswer
from django.template.loader import get_template
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date
from django.core.paginator import Paginator

#from decouple import config
#from openai import OpenAI

#client = OpenAI(api_key=config('OPENAI_API_KEY'))

# Create your views here.

title = 'PROJECT-M'

def index(request):
    #page_title = 'Home PROJECT-M'
    content = 'Crack the Code, Change the World.'
    return render(request, 'index.html', {'title': title, 'content': content})

def solar_system_explorer(request):
    return render(request, 'solar_system_explorer.html', {'title': title})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            user.set_password(password) #Password Hashing(Encryption)
            user.save()
            # Add user to "Readers" group defaultly
            readers_group, created = Group.objects.get_or_create(name='Readers')
            user.groups.add(readers_group)

            messages.success(request, 'Registetered successfully!')
            return redirect('projectM:login')
    else:
        form = RegisterForm()

    return render(request, 'login & register/register.html', {'title': title, 'form': form})

def login(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Email: {email}, Username: {username}, Password: {password}")

            user = authenticate(username=username, password=password, email=email)
            print(f"Result:{user}")


            if user is not None:
                auth_login(request, user) # Session Starts
                messages.success(request, 'Logged in successfully!')
                return redirect('projectM:index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login & register/login.html', {'title': title, 'form': form})

def logout(request):
    auth_logout(request) # Session Ends
    messages.success(request, 'Logged out successfully!')
    return redirect('projectM:login')

def about(request):
    about_details = About.objects.all()
    return render(request, 'about.html', {'title': title, 'about_details': about_details})

@login_required
@permission_required('projectM.view_services', raise_exception=True)
def services(request):
    if request.user and not request.user.has_perm('projectM.view_services'):
        messages.error(request, 'You do not have permission to view the services page.')
        return redirect('projectM:index')
    all_services = Services.objects.all()
    paginator = Paginator(all_services, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'services.html', {'title': title, 'all_services': all_services, 'page_obj': page_obj})

@login_required
@permission_required('projectM.view_services', raise_exception=True)
def resume(request):
    return render(request, 'resume.html', {'title': title})

@login_required
def portfolio(request):
    
    return render(request, 'portfolio.html', {'title': title})

@login_required
def contact(request):
    return render(request, 'contact.html', {'title': title})

@login_required
def test(request):
    return render(request, 'test.html', {'title': title})

# ----- Resume Start -----
@login_required
def resume_builder(request, slug):
    service = get_object_or_404(Services, slug=slug)
    return render(request, 'resume_builder.html', {'title': title, 'service': service})

@login_required
def create_resume(request, slug):
    service = get_object_or_404(Services, slug=slug)
       
    name=request.POST.get('name')
    job_title=request.POST.get('job_title')
    phone=request.POST.get('phone')
    email=request.POST.get('email')
    birthday=request.POST.get('birthday')
    address=request.POST.get('address')
    education_list=request.POST.getlist('education')
    language_list=request.POST.getlist('language')
    objective=request.POST.get('objective')
    work_experience_list=request.POST.getlist('work_experience')
    skills_list=request.POST.getlist('skills')
    certifications_list=request.POST.getlist('certifications')
    projects=request.POST.get('projects')
    print(work_experience_list)

    form = ResumeGeneratorForm()
    if request.method == 'POST':
        form = ResumeGeneratorForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.education = ', '.join(education_list) # Save as comma-separated string
            resume.language = ', '.join(language_list) # Save as comma-separated string
            resume.work_experience = ', '.join(work_experience_list) # Save as comma-separated string
            resume.skills = ', '.join(skills_list) # Save as comma-separated string
            resume.certifications = ', '.join(certifications_list) # Save as comma-separated string
            # print(resume.language)
            resume.save()
            resume.education_list = education_list
            resume.language_list = language_list
            # messages.success(request, 'Resume generated successfully!')
            print("Saved Resume Slug:", resume.slug)
            return redirect('projectM:view_resume',  slug=resume.slug)
        else:
            print("Invalid Form", form.errors)
    return render(request, 'resume4.html', {'title': title,
                                            'service': service,
                                            'form': form,
                                            'name': name,
                                            'job_title': job_title,
                                            'phone': phone,
                                            'email': email,
                                            'birthday': birthday,
                                            'address': address,
                                            'education': education_list,
                                            'language': language_list,
                                            'objective': objective,
                                            'work_experience': work_experience_list,
                                            'skills': skills_list,
                                            'certifications': certifications_list,
                                            'projects': projects
                                            })

@login_required
def view_resume(request, slug):
    resumes = Resume.objects.filter(slug=slug)
    if not resumes.exists():
        print("Resume not found")
        # Optionally handle missing resume
        return HttpResponse("Resume not found", status=404)

    resume = resumes.first()

    # Split and clean (strip spaces) each list
    education_list = [item.strip() for item in resume.education.split(',')] if resume.education else []
    language_list = [item.strip() for item in resume.language.split(',')] if resume.language else []
    work_experience_list = [item.strip() for item in resume.work_experience.split(',')] if resume.work_experience else []
    skills_list = [item.strip() for item in resume.skills.split(',')] if resume.skills else []
    certifications_list = [item.strip() for item in resume.certifications.split(',')] if resume.certifications else []

    return render(request, 'view_resume.html', {
        'title': 'View Resume',  # make sure 'title' is defined
        'resume': resume,
        'education_list': education_list,
        'language_list': language_list,
        'work_experience_list': work_experience_list,
        'skills_list': skills_list,
        'certifications_list': certifications_list
    })

# ----- Resume Start -----

# ----- Chatbot Start -----

# OpenAI code

# def get_bot_response(message):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful resume assistant."},
#             {"role": "user", "content": message}
#         ]
#     )
#     return response.choices[0].message.content.strip()

# Rules Based Chatbot code
def get_response_from_db(message):
    message = message.lower()
    rules = ChatbotRules.objects.all()

    for rule in rules:
        if rule.keyword.lower() in message:
            return rule.response
        
    return "I'm sorry, I didn't understand that. Can you please rephrase?"

@login_required
def chatbot(request, slug):
    service = get_object_or_404(Services, slug=slug)
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip().lower()
        # Logic to generate response goes here
        #bot_response = f"AI: {user_message}"  # Replace with real AI logic
        
        # Open AI Code --Start--
        # bot_response = get_bot_response(user_message)
        # ---End---

        #Rules Based Chatbot Code Start

        bot_response = get_response_from_db(user_message)

        return JsonResponse({'message': bot_response})
    
    return render(request, 'chatbot/chatbot.html', {'title': title,  'service': service, 'slug': slug})
# ----- Chatbot End -----
# ----- Library Management System Start -----
@login_required
def library_management(request, slug):
        service = get_object_or_404(Services, slug=slug)
        return render(request, 'library_management_system/admin.html', {'title': 'Library Management', 'service': service, 'slug': slug})

@login_required
def manage_library_card(request):
    service = get_object_or_404(Services, name='Library Management')
    form = ManageLibraryCardForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'add_card':
            form = ManageLibraryCardForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Card added successfully!')
                # return redirect('projectM:manage_library_card')  # Optional: redirect to clear form
            else:
                messages.error(request, 'Please correct the above errors.')
        elif form_type == 'remove_card':
            card_id = request.POST.get('card_id')
            try:
                card = ManageLibraryCard.objects.get(card_id=card_id)
                card.delete()
                messages.success(request, 'Card removed successfully.')
            except ManageLibraryCard.DoesNotExist:
                messages.error(request, 'Card not found.')
            

            
    return render(request, 'library_management_system/manage_card.html', {
        'title': 'Manage Library Card',
        'slug': service.slug,
        'form': form
    })

@login_required
def add_book(request):
    service = Services.objects.get(name='Library Management')
    if request.method == "POST":
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('projectM:view_books')
        else:
            print(form.errors)
    else:
        form = AddBookForm()

    return render(request, 'library_management_system/add_book.html', {'title': 'Add Book',
                                                                        'slug': service.slug,
                                                                          'form': form
                                                                          })

@login_required
def view_books(request):
    service = Services.objects.get(name='Library Management')
    query = request.GET.get('q')
    books = AddBook.objects.all().order_by('id')  # Ascending by ID

    if not books.exists():
        messages.error(request, 'No books found.')

    if query:
        books = books.filter(
            Q(book_title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'library_management_system/view_books.html', {'title': 'View Books',
                                                                         'slug': service.slug,
                                                                           'books': books
                                                                           })

@login_required
def edit_book(request, book_id):
    service = Services.objects.get(name = 'Library Management')
    book = get_object_or_404(AddBook, id=book_id)

    if request.method == "POST":
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('projectM:view_books')
    return render(request, 'library_management_system/edit_book.html', {'title': 'Edit Book',
                                                                         'slug': service.slug,
                                                                           'book':book
                                                                           })

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(AddBook, id=book_id)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('projectM:view_books')

@login_required
def borrow_book(request):
    service = Services.objects.get(name = 'Library Management')
    books = AddBook.objects.all()


    if request.method == "POST":
        book_id = request.POST.get('book_id')
        return_date = request.POST.get('return_date')

        print(book_id, return_date)

        if book_id and return_date:
            book = get_object_or_404(AddBook, id=book_id)

            if book.borrowed:
                messages.error(request, "This book is already borrowed.")
            else:
                book.borrowed = True
                book.borrowed_by = request.user
                book.borrowed_date = timezone.now().date()
                book.return_date = return_date
                book.save()
                messages.success(request, "Book borrowed successfully!")
                return redirect('projectM:view_books')

    return render(request, 'library_management_system/borrow_book.html', {'title': 'Borrow Book',
                                                                          'slug': service.slug,
                                                                           'books': books,
                                                                           })

@login_required
def return_book(request):
    service = Services.objects.get(name = 'Library Management')
    books = AddBook.objects.all()
    print("Res: ", books)


    if request.method == "POST":
        book_id = request.POST.get('book_id')
        print(f"Received book_id: {book_id}")

        if book_id:
            book = get_object_or_404(AddBook, id=book_id)
            print("Book: ", book)
            if book.borrowed:
                book.borrowed = False
                book.borrowed_by = None
                book.borrowed_date = None
                book.return_date = None
                book.save()
                messages.success(request, "Book returned successfully!")
            else:
                messages.error(request, "This book is not borrowed.")

            return redirect('projectM:view_books')
        else:
            messages.error(request, "Invalid book ID.")


    return render(request, 'library_management_system/return_book.html', {'title': 'Return Book',
                                                                          'slug': service.slug,
                                                                           'books': books,
                                                                           })

@login_required
def add_admin(request):
    service = Services.objects.get(name = 'Library Management')
    return render(request, 'library_management_system/add_admin.html', {'title': 'Add Admin',
                                                                          'slug': service.slug})

# ----- Library Management System End -----

# ----- Weather App Start -----
@login_required
# @permission_required('projectM.view_weather_app', raise_exception=True)
def weather_app(request, slug):
    if request.user and not request.user.has_perm('projectM.view_weather_app'):
        messages.error(request, 'You do not have permission to view the Weather App page.')
        return redirect('projectM:services')
    service = get_object_or_404(Services, slug=slug)
    weather_data = {}

    if request.method == "POST":
        city = request.POST.get('city')
        api_key = '76993e1346a85fc08bea5b3eafa364b1'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        else:
            weather_data = {'error': 'City not found'}
            
    
    return render(request, 'weather_app/weather_app.html', {'title': title,
                                                        'service': service,
                                                        'weather_data': weather_data,
                                                        })
# ----- Weather App End -----

# ----- Expense Tracker Start -----
@login_required
def expense_tracker(request, slug):
    service = get_object_or_404(Services, slug=slug)
    categories = ExpenseCategory.objects.all().order_by('id')
    #expenses = ExpensesTracker.objects.all().order_by('id')
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(f"Category ID: {category}, Start Date: {start_date}, End Date: {end_date}")

    if category:
        expenses = ExpensesTracker.objects.filter(category__id=category)
    elif start_date and end_date:
        expenses = ExpensesTracker.objects.filter(date__range=[start_date, end_date])
    else:
        expenses = ExpensesTracker.objects.all().order_by('id')


    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0  # returns 0 if no data


    return render(request, 'expense_tracker/et_index.html', {'title': title,
                                                             'service': service,
                                                             'categories': categories,
                                                             'expenses': expenses,
                                                             'total_amount': total_amount
                                                             })

@login_required
def add_expense(request):
    service = Services.objects.get(name = 'Expense Tracker')
    categories = ExpenseCategory.objects.all().order_by('id')

    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('projectM:expense_tracker', slug=service.slug)
    else:
        form = AddExpenseForm()

    return render(request, 'expense_tracker/et_add_expenses.html', {'title': 'Add Expense',
                                                                    'slug': service.slug,
                                                                    'categories': categories,
                                                                    'form': form
                                                       })
# ----- Expense Tracker End -----

# ----- To Do List Start -----
@login_required
def to_do_list(request, slug):
    service = get_object_or_404(Services, slug=slug)

    if request.method == "POST":
        form = ToDoListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully!')
            return redirect('projectM:to_do_list', slug=service.slug)
    else:
        form = ToDoListForm()

    tasks = ToDoList.objects.all().order_by('id')
    today = date.today()
    
    return render(request, 'to_do_list/to_do_index.html', {'title': title,
                                                           'service': service,
                                                           'form': form,
                                                           'tasks': tasks,
                                                           'today': today
                                                           })

@login_required
def complete_task(request, task_id, slug):
    service = get_object_or_404(Services, slug=slug)
    task = get_object_or_404(ToDoList, id=task_id)
    if not task.is_completed:
        task.is_completed = True
        task.save()
        messages.success(request, 'Task marked as completed!')
        return redirect('projectM:to_do_list', slug=service.slug)
@login_required

def delete_task(request, task_id, slug):
    service = get_object_or_404(Services, slug=slug)
    task = get_object_or_404(ToDoList, id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('projectM:to_do_list', slug=service.slug)
# ----- To Do List End -----

# ----- Contact Manager Start -----
@login_required
def contact_manager(request, slug):
    service = get_object_or_404(Services, slug=slug)
    contacts = ContactManager.objects.all().order_by('id')

    return render(request, 'contact_manager/cm_index.html', {'title': title, 'service': service, 'contacts': contacts})

@login_required
def add_contact(request):
    service = Services.objects.get(name = 'Contact Manager')

    if request.method == "POST":
        form = ContactManagerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact added successfully!')
            return redirect('projectM:contact_manager', slug=service.slug)
    else:
        form = ContactManagerForm()

    return render(request, 'contact_manager/add_contact.html', {'title': 'Add Contact', 'slug': service.slug, 'form': form})

@login_required
def edit_contact(request, contact_id):
    service = Services.objects.get(name='Contact Manager')
    contact = get_object_or_404(ContactManager, id=contact_id)

    if request.method == "POST":
        form = ContactManagerForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact Updated Successfully!')
            return redirect('projectM:contact_manager', slug=service.slug)
    else:
        form = ContactManagerForm(instance=contact)

    return render(request, 'contact_manager/edit_contact.html', {'title': 'Edit Contact', 'slug': service.slug, 'form': form, 'contact': contact})

@login_required
def delete_contact(request, contact_id):
    service = Services.objects.get(name='Contact Manager')
    contact = get_object_or_404(ContactManager, id=contact_id)
    contact.delete()
    messages.success(request, 'Contact Deleted Successfully!')
    return redirect('projectM:contact_manager', slug=service.slug)
# ----- Contact Manager End -----

# ----- Job Board Start -----
@login_required
def job_board(request, slug):
    service = get_object_or_404(Services, slug=slug)
    job_board = JobBoard.objects.all().order_by('id')

    return render(request, 'job_board/jb_index.html', {'title': title, 'service': service, 'job_board': job_board})

@login_required
def post_job(request):
    service = Services.objects.get(name = 'Job Board')
    job_types = JobType.objects.all().order_by('id')
    print(job_types)

    if request.method == "POST":
        print("Success!")
        form = JobBoardForm(request.POST)
        if form.is_valid():
            print("Success12!")
            form.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('projectM:job_board', slug=service.slug)
        else:
            print("Invalid Form", form.errors)
    else:
        form = JobBoardForm()

    return render(request, 'job_board/post_job.html', {'title': title, 'slug': service.slug, 'job_types': job_types, 'form': form})

@login_required
def apply_job(request):
    service = Services.objects.get(name='Job Board')

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            print("Resume file saved at:", instance.resume.path)
            messages.success(request, 'Job applied successfully!')
            return redirect('projectM:job_board', slug=service.slug)
        else:
            print("Invalid Form", form.errors)
    else:
        form = JobApplicationForm()

    return render(request, 'job_board/apply_job.html', {'title': title, 'slug': service.slug, 'form': form})
# ----- Job Board End -----

# -----Online Polling System Start -----

def online_polling_system(request, slug):
    service = get_object_or_404(Services, slug=slug)
    polls = OnlinePollingSystem.objects.all().order_by('id')
    
    return render(request, 'online_polling_system/online_polling_index.html', {'title': title, 'service': service, 'polls': polls})

def create_poll(request):
    service = Services.objects.get(name='Online Polling System')

    if request.method == "POST":
       question = request.POST.get('question')
       option_texts = request.POST.getlist('option_text') # collect all options with same name

       if not question or not any(option_texts):
           messages.error(request, 'Please enter a question and at least one option.')
           return redirect('projectM:create_poll')
       
       # Save poll
       poll = OnlinePollingSystem(question=question, created_by=request.user, is_active=False)
       poll.save()

       # Save each options
       for option_text in option_texts:
           option = PollOptions(poll=poll, option_text=option_text)
           option.save()

       messages.success(request, 'Poll created successfully!')
       return redirect('projectM:online_polling_system', slug=service.slug)
    else:
        return render(request, 'online_polling_system/create_poll.html', {'title': title, 'service': service})

def vote_poll(request, poll_id):
    service = Services.objects.get(name='Online Polling System')

    poll = get_object_or_404(OnlinePollingSystem, id=poll_id)

    if request.method == "POST":
        option_id = request.POST.get('option')
        if option_id:
            selected_option = get_object_or_404(PollOptions, id=option_id, poll=poll)
            selected_option.votes +=1
            selected_option.save()

            poll.total_votes += 1
            poll.save()

            messages.success(request, 'Vote submitted successfully!')
            return redirect('projectM:online_polling_system', slug=service.slug)
    
    options = PollOptions.objects.filter(poll=poll) 

    return render(request, 'online_polling_system/vote_poll.html', {'title': title, 'service': service, 'options': options, 'poll': poll})

def polls_result(request, poll_id):
    service = Services.objects.get(name='Online Polling System')
    poll = get_object_or_404(OnlinePollingSystem, id=poll_id)
    options = PollOptions.objects.filter(poll=poll)
    total_value = poll.total_votes
    # Add percentage for each option
    options_with_percentage = []
    
    for option in options:
        if total_value > 0:
            percentage = (option.votes / total_value) * 100
        else:
            percentage = 0
        options_with_percentage.append({
            'option': option,
            'percentage': round(percentage, 2)
        })

    return render(request, 'online_polling_system/polls_result.html', {'title': title,
                                                                       'service': service,
                                                                       'poll': poll,
                                                                       'percentage': percentage,
                                                                       'options_with_percentage': options_with_percentage
                                                                       })

def activate_poll(request, poll_id):
    service = Services.objects.get(name='Online Polling System')
    poll = get_object_or_404(OnlinePollingSystem, id=poll_id)

    poll.is_active = True
    poll.save()

    messages.success(request, 'Poll activated successfully!')
    return redirect('projectM:online_polling_system', slug=service.slug)

def deactivate_poll(request, poll_id):
    service = Services.objects.get(name='Online Polling System')
    poll = get_object_or_404(OnlinePollingSystem, id=poll_id)

    poll.is_active = False
    poll.save()

    messages.success(request, 'Poll deactivated successfully!')
    return redirect('projectM:online_polling_system', slug=service.slug)

# -----Online Polling System End -----

# -----Quiz App Start -----

def quiz_app(request, slug):
    service = get_object_or_404(Services, slug=slug)

    quizzes = QuizDetails.objects.all()
    quiz_count = quizzes.count()

    return render(request, 'quiz_app/quiz_dashboard.html', {'title': title,
                                                            'service': service,
                                                            'quiz_count': quiz_count
                                                            })

def quiz_list(request):
    service = Services.objects.get(name='Quiz App')
    quizzes = QuizDetails.objects.all().order_by('-id')

    quiz_data = []
    for quiz in quizzes:
        first_question = quiz.questions.first()  # uses related_name='questions'
        quiz_data.append({
            'quiz': quiz,
            'first_question': first_question
        })

    return render(request, 'quiz_app/quiz_list.html', {
        'title': title,
        'slug': service.slug,
        'quiz_data': quiz_data
    })


def add_quiz_details(request):
    service = Services.objects.get(name='Quiz App')

    if request.method == "POST":
        form = QuizDetailsForm(request.POST)
        if form.is_valid():
            quiz_details = form.save(commit=False)
            quiz_details.created_by = request.user
            quiz_details.save()
            messages.success(request, 'Quiz added successfully!')
            return redirect('projectM:quiz_list')
    else:
        form = QuizDetailsForm()

    return render(request, 'quiz_app/add_quiz_details.html', {'title': title,
                                                              'slug': service.slug,
                                                              'form': form
                                                              })


def add_quiz(request):
    service = Services.objects.get(name='Quiz App')
    quiz_titles = QuizDetails.objects.all().order_by('id')

    if request.method == "POST":
        question_text = request.POST.get('question_text')
        option_texts = request.POST.getlist('option_text')
        quiz_id = request.POST.get('quiz_id')
        correct_option_index = request.POST.get('correct_option')  # index: '1', '2', etc.

        if not question_text or not any(option_texts):
            messages.error(request, 'Please enter a question and at least one option.')
            return redirect('projectM:add_quiz')

        if not quiz_id:
            messages.error(request, 'Please select a quiz.')
            return redirect('projectM:add_quiz')

        try:
            quiz_instance = QuizDetails.objects.get(id=quiz_id)
        except QuizDetails.DoesNotExist:
            messages.error(request, 'Selected quiz does not exist.')
            return redirect('projectM:add_quiz')

        # Create question (without correct_option for now)
        question_obj = QuizQuestions.objects.create(
            quiz=quiz_instance,
            question_text=question_text,
            total_marks=0  # or as needed
        )

        # Save options and track the correct one
        correct_option_obj = None
        for idx, text in enumerate(option_texts, start=1):
            if text.strip():
                option = QuizOptions.objects.create(
                    question=question_obj,
                    option_text=text.strip()
                )
                if str(idx) == correct_option_index:
                    correct_option_obj = option

        # Update question with correct option
        if correct_option_obj:
            question_obj.correct_option = correct_option_obj
            question_obj.save()

        quiz_instance.number_of_questions += 1
        quiz_instance.save()

        

        messages.success(request, 'Question added successfully!')
        return redirect('projectM:add_quiz')

    return render(request, 'quiz_app/add_quiz.html', {
        'title': title,
        'quiz_titles': quiz_titles,
        'slug': service.slug
    })


def manage_quiz(request):
    service = Services.objects.get(name='Quiz App')
    questions = QuizQuestions.objects.all().order_by('id')

    quetsion_options = {}
    for question in questions:
        options = QuizOptions.objects.filter(question=question)
        quetsion_options[question.id] = options



    return render(request, 'quiz_app/manage_quiz_questions.html', {'title': title,
                                                        'slug': service.slug,
                                                        'questions': questions,
                                                        'quetsion_options': quetsion_options
                                                        })

def view_participants(request):
    service = Services.objects.get(name='Quiz App')

    participants = QuizParticipants.objects.all().order_by('id')

    return render(request, 'quiz_app/view_participants.html', {'title': title,
                                                        'slug': service.slug,
                                                        'participants': participants
                                                        })


def quiz(request, quiz_id, question_id):
    service = Services.objects.get(name='Quiz App')
    quiz_instance = get_object_or_404(QuizDetails, id=quiz_id)
    question = get_object_or_404(QuizQuestions, quiz=quiz_instance, id=question_id)
    options = QuizOptions.objects.filter(question=question)
    print(options)
    questions = QuizQuestions.objects.filter(quiz=quiz_instance).order_by('id')
    question_ids = list(questions.values_list('id', flat=True))
    current_number = question_ids.index(question.id) + 1 if question.id in question_ids else 1

    if request.method == 'POST':
        selected_option_id = request.POST.get('selected_option')
        print(f"Selected Option ID: {selected_option_id}")

        if selected_option_id:
            selected_option = get_object_or_404(QuizOptions, id=selected_option_id)

            if selected_option == question.correct_option:
                correct_answer = True
            else:
                correct_answer = False

            
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                selected_option=selected_option,
                is_correct=correct_answer,
                quiz=quiz_instance,
                active=True
            )

        # next_question = get_object_or_404(QuizQuestions, quiz=quiz_instance, id__gt=question_id).order_by('id').first()

        # id__gt -> Finds questions with an ID greater than the current one (i.e., the next question in sequence).
        next_question = QuizQuestions.objects.filter(
            quiz=quiz_instance,
            id__gt=question_id
        ).order_by('id').first()

        # print(f"Next Question ID: {next_question.id}")

        if next_question:
            return redirect('projectM:quiz', quiz_id=quiz_id, question_id=next_question.id)
        else:
            add_data_in_leaderboard = QuizLeaderboard.objects.create(
                user=request.user,
                quiz_taken=quiz_instance
            )
            get_score = UserAnswer.objects.filter(
                user=request.user,
                quiz=quiz_instance,
                is_correct=True
            )
            user_answer_count = get_score.count()
            add_data_in_leaderboard.score = user_answer_count
            add_data_in_leaderboard.save()


            return redirect('projectM:quiz_results', quiz_id=quiz_id)
            # return redirect('projectM:quiz_results')

            

    return render(request, 'quiz_app/quiz.html', {'title': title,
                                                  'slug': service.slug,
                                                  'quiz_instance': quiz_instance,
                                                  'question': question,
                                                  'options': options,
                                                  'current_number': current_number,
                                                  
                                                  })

def quiz_results(request, quiz_id):
    service = Services.objects.get(name='Quiz App')
    quiz_instance = get_object_or_404(QuizDetails, id=quiz_id)
    print(f"quiz_instance: {quiz_instance.id}")
    print(f"quiz_instance: {quiz_instance.number_of_questions}")
    
    user_answer = UserAnswer.objects.filter(
        user=request.user,
        quiz=quiz_instance,
        is_correct=True
    )
    user_answer_count = user_answer.count()
    print(f"User Answer Count: {user_answer_count}")



    return render(request, 'quiz_app/quiz_results.html', {'title': title,
                                                        'slug': service.slug,
                                                        'quiz_instance': quiz_instance,
                                                        'user_answer_count': user_answer_count,
                                                        })

def leaderboard(request):
    service = Services.objects.get(name='Quiz App')


    return render(request, 'quiz_app/leaderboard.html', {'title': title,
                                                        'slug': service.slug})

# -----Quiz App End -----

#https://www.sourcecodester.com/javascript/17357/resume-maker-using-html-css-javascript.html
# https://github.com/YuwenXiong/Library-Management-System/blob/master/templates/addbook.html