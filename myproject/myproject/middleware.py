from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
import datetime

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                elapsed = (now - datetime.datetime.fromisoformat(last_activity)).seconds
                if elapsed > 600:  # 10 minutes
                    logout(request)
                    messages.warning(request, "Your session has expired due to inactivity.")
                    return redirect('projectM:login')  # Replace with your login view name

            request.session['last_activity'] = now.isoformat()

        return self.get_response(request)
    

