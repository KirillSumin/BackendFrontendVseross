import json
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.core.exceptions import BadRequest
from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from pytz import timezone
from django.views import View
from django.views.generic import FormView, TemplateView

from application import settings
from core.forms import LoginForm
from core.models import User, EntranceHistory


class LoginView(FormView):
    template_name = 'login_bootstrap.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard:history_of_passes')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        context = super().get_context_data(form=form)

        context['email_init'] = form.data.get('email')

        return self.render_to_response(context)

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        user = authenticate(email=cleaned_data['email'], password=cleaned_data['password'])
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error('email', 'Email или пароль не верны')
            return self.form_invalid(form)


class TestView(TemplateView):
    template_name = 'adminlte/base.html'


class FaceRecognizeView(View):
    def post(self, request):
        res = json.loads(request.body)
        if res['secret_key'] != '12524':
            return JsonResponse({}, status=403)

        try:
            user = User.objects.get(email=res['email'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'user with this email doesnt exist'}, status=500)

        try:
            entrance_history = EntranceHistory.objects.get(user=user, exit_date=None)
            # небезапасно если как то пользователь вышел без учёта
            # тк нет двух камер делам таймаут по выходу
            settings_time_zone = timezone(settings.TIME_ZONE)
            delta = timedelta(seconds=2)
            in_date = entrance_history.entry_date
            now_date = datetime.now(settings_time_zone)
            if now_date - in_date < delta:
                return JsonResponse({'error': 'too faster exit, wait'}, status=200)
            entrance_history.exit_date = datetime.now(settings_time_zone)
            entrance_history.save()
        except (EntranceHistory.DoesNotExist, EntranceHistory.MultipleObjectsReturned):
            entrance_history = EntranceHistory.objects.create(user=user, auth_type='face')
        print(user, entrance_history)
        return JsonResponse({}, status=200)
