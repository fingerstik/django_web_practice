# from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.views import generic

# @method_decorator(logout_message_required, name='dispatch')
from jrweb.board.forms import LoginForm


class LoginView(generic.FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/board/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)

        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)

        return super().form_valid(form)
