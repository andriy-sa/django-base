from django.conf import settings

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login, authenticate
)
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .forms import FormRegistration
import facebook
from .models import MyUser
from django.core import serializers
from django.contrib import messages

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):

    # users = serializers.serialize('json',MyUser.objects.all())
    # return HttpResponse(users)

    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

@csrf_protect
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = FormRegistration(request.POST)

        if form.is_valid():
            user = MyUser()
            user.email    = request.POST.get('email')
            user.username = request.POST.get('username')
            user.phone    = request.POST.get('phone')
            user.set_password(request.POST.get('password'))
            user.save()
            messages.add_message(request,messages.SUCCESS,'Account Successfully created!')
            return HttpResponseRedirect('/login')
    else:
        form = FormRegistration()


    return TemplateResponse(request,'registration/register.html',{
        'form' : form
    })

def login_fb(request):
    perms = ['email']
    url = facebook.auth_url(settings.FACEBOOK_APP_ID,request.build_absolute_uri('/fb/success/'),perms)
    return HttpResponseRedirect(url)

def login_fb_success(request):
    code = request.GET.get('code')
    fb =  facebook.GraphAPI()
    result = fb.get_access_token_from_code(code,request.build_absolute_uri('/fb/success/'),settings.FACEBOOK_APP_ID,settings.FACEBOOK_APP_SECRET)
    token = result['access_token']
    fb.access_token = token
    user_data = fb.get_object('me',fields='id,name,email')
    user = MyUser.objects.filter(email=user_data['email']).first()
    if user is None:
        user = MyUser(username=user_data['name'],email=user_data['email'])
        user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request,user)
    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
    return HttpResponseRedirect(redirect_to)

