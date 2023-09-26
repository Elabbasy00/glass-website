

# project/users/adapter.py:
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if(request.user.is_verified):
            path = "/accounts/{username}/"
            return path.format(username=request.user.username)
        else:
            path = "/accounts/inactive/"
            return path
    
    def get_signup_redirect_url(self, request):
        if(request.user.is_verified):
            path = "/accounts/{username}/"
            return path.format(username=request.user.username)
        else:
            path = "/accounts/inactive/"
            return path
    