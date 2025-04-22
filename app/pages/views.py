import os
import secrets
import tempfile
import uuid
import zipfile

from celery.result import AsyncResult  # type: ignore
from core.forms import (
    EditUserForm,
    RegistrationUserForm,
)
from core.models import (
    EmailSettings,
    LoginSettings,
)
from django.conf import settings  # type: ignore
from django.contrib import messages  # type: ignore
from django.contrib.auth import (  # type: ignore
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required  # type: ignore
from django.core.mail import (  # type: ignore
    EmailMessage,
    get_connection,
)
from django.core.validators import validate_email  # type: ignore
from django.http import (  # type: ignore
    FileResponse,
    HttpRequest,
)
from django.shortcuts import (  # type: ignore
    HttpResponse,
    redirect,
    render,
)
from django.utils.translation import gettext_lazy as _  # type: ignore
from shop.email_notifications import send_user_verification_code
from wagtail.models import Site  # type: ignore

from pages.forms import ToSVGForm
from pages.models import ContactUsPage
from pages.tasks import convert_to_svg


def email(request: HttpRequest) -> str:
    email_settings = EmailSettings.load(request_or_site=request)
    return email_settings.login


def user_registration(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            request.session['user_id'] = user.id

            return redirect('verify-email')

        return render(request, 'pages/user/registration.html', context={'form': form})

    return render(request, 'pages/user/registration.html', context={'form': RegistrationUserForm()})


def email_verification(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        user_id = request.session.get('user_id', None)
        if user_id is not None and get_user_model().objects.filter(id=user_id).exists():
            user = get_user_model().objects.get(id=user_id)

            if user.verification_code == verification_code:
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('user-profile')

            messages.error(request, _('The verification code does not match. Reload the page to resend the verification code to your email.'))
        else:
            messages.error(request, _('Your account was not found.'))

    send_user_verification_code(request)
    return render(request, 'pages/user/email_verification.html')


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if get_user_model().objects.filter(username=username).exists():
            user = get_user_model().objects.get(username=username)
            if user.check_password(password):
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('user-profile')
            messages.error(request, _('Incorrect password.'))
        else:
            messages.error(request, _('Your account was not found.'))

    return render(request, 'pages/user/login.html', context={'max_simultaneous_logins': LoginSettings.load(request_or_site=request).max_simultaneous_logins})


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')


@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        redirect_to_email_verification = False
        original_email = user.email

        if form.is_valid():

            if original_email != form.cleaned_data['email']:
                redirect_to_email_verification = True

            form.save()
            if redirect_to_email_verification:
                logout(request)

                request.session['user_id'] = user.id
                user.verification_code = ''.join(str(secrets.randbelow(10)) for i in range(6))
                user.save()

                return redirect('verify-email')

    else:
        form = EditUserForm(instance=user, initial={'name': f'{user.first_name} {user.last_name}'})
    return render(request, 'pages/user/profile.html', context={'page_name': 'profile', 'show_search_block': False, 'form': form, 'page': {'email': email(request)}})


@login_required
def user_transactions(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/user/transactions.html', context={'page_name': 'transactions', 'show_search_block': False, 'page': {'email': email(request)}})


@login_required
def user_wishlist(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/user/wishlist.html', context={'page_name': 'wishlist', 'url': request.build_absolute_uri(request.path), 'show_search_block': True, 'page': {'email': email(request)}})


@login_required
def user_purchases(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/user/purchases.html', context={'page_name': 'purchases', 'url': request.build_absolute_uri(request.path), 'show_search_block': True, 'page': {'email': email(request)}})


def resend_contact_us_form(request: HttpRequest) -> HttpResponse:
    try:
        validate_email(request.POST.get('email'))
        email_settings = EmailSettings.load(request_or_site=request)
        site = Site.find_for_request(request)

        message = f'{_("From")}: {request.POST.get("email")}\n{_("Name")}: {request.POST.get("full_name")}\n{_("Message")}:\n{request.POST.get("message")}'

        email_backend = get_connection(
            host=email_settings.host,
            port=int(email_settings.port),
            username=email_settings.login,
            password=email_settings.password,
            use_tls=email_settings.use_tls,
            use_ssl=True,
            fail_silently=False,
        )

        email = EmailMessage(
            subject=_('Direct form'),
            body=message,
            from_email=f'{site.site_name} {_("help")} <{email_settings.login}>',
            to=[email_settings.login],
            connection=email_backend,
        )
        email.send()

    except Exception:
        return redirect('/')

    return redirect(ContactUsPage.objects.filter(live=True).first().get_full_url() + '?success=true')


def to_svg(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        form = ToSVGForm(request.POST, request.FILES)

        if form.is_valid():

            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'to_svg')):
                os.mkdir(os.path.join(settings.MEDIA_ROOT, 'to_svg'))

            if 'file' in request.FILES:
                uploaded_file = form.files['file']
                file_ext = uploaded_file.name.split('.')[-1]
                path_to_image = os.path.join(settings.MEDIA_ROOT, 'to_svg', f'{uuid.uuid4()}.{file_ext}')

                with open(path_to_image, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                new_form_data = {
                    'color_mode': form.data['color_mode'],
                    'filter_speckle': form.data['filter_speckle'],
                    'color_precision': form.data['color_precision'],
                    'layer_difference': form.data['layer_difference'],
                    'mode': form.data['mode'],
                    'corner_threshold': form.data['corner_threshold'],
                    'length_threshold': form.data['length_threshold'],
                    'splice_threshold': form.data['splice_threshold'],
                    'path_precision': form.data['path_precision'],
                    'file_path': path_to_image,
                }

                form = ToSVGForm(data=new_form_data)

            elif form.data['file_path']:
                if os.path.exists(form.data['file_path']):
                    path_to_image = form.data['file_path']
                else:
                    messages.error(request, _('You must update a file.'))
                    return render(request, 'pages/to_svg.html', {'form': form})
            else:
                messages.error(request, _('You must upload a file.'))
                return render(request, 'pages/to_svg.html', {'form': form})

            result = convert_to_svg.delay(path_to_image, form.data)
            return render(request, template_name='pages/to_svg.html', context={'form': form, 'key': result.id})

    else:
        form = ToSVGForm()

    return render(request, template_name='pages/to_svg.html', context={'form': form})


def get_svg_conversion_status(request: HttpRequest, key: str) -> HttpResponse:

    result = AsyncResult(key)
    if result is not None:
        if result.status == 'SUCCESS':
            return HttpResponse('SUCCESS')

        if result.status in {'PENDING', 'STARTED'}:
            return HttpResponse('PENDING')

        return HttpResponse('FAILURE')

    return redirect('to-svg')


def download_svg(request: HttpRequest, key: str) -> FileResponse:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        with zipfile.ZipFile(temp_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(os.path.join(settings.MEDIA_ROOT, 'to_svg', f'{key}.svg'), f'{key}.svg')

    response = FileResponse(open(temp_file.name, 'rb'), as_attachment=True, filename='images.zip')
    os.remove(temp_file.name)

    return response
