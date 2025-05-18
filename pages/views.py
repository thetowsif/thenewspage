from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    A class-based view that inherits from the Django 'TemplateView' generic
    view and is responsible for rendering the homepage template of the website.
    """
    template_name = 'home.html'
