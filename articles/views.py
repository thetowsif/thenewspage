from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, \
    UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from articles.forms import CommentForm
from articles.models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    """
    A class-based view in Django that displays a list of "Article" objects.

    This view requires the user to be logged in (via the "LoginRequiredMixin"
    mixin) and uses the template "article_list.html" to render the list of
    articles.

    Attributes:
        model: The model that the view is using.
        template_name: The template name used to render the view.
    """
    model = Article
    template_name = 'articles/article_list.html'


class ArticleDetailGet(DetailView):
    """
    A class-based view in Django that displays the details of a
    single "Article" object.

    This view renders the details of the article and includes a form for
    adding comments to it.

    Attributes:
        model: The model that the view is using.
        template_name: The template name used to render the view.

    """
    model = Article
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        """
        This method adds a 'CommentForm' form object (for adding comments
        in articles) to the context data passed to the template when rendering
        the view.

        :param kwargs: Additional keywords arguments.
        :return: This method returns a dictionary with the context data used
            in the template rendering.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class ArticleDetailPost(SingleObjectMixin, FormView):
    """
    A class-based view in Django that handles form submission for adding
    comments to a single "Article" object.

    This view uses the 'SingleObjectMixin' to retrieve the commented
    'Article' object and the 'CommentForm' form to handle comment submissions.

    Attributes:
        model: The model that the view is using.
        form_class: The form class to use for handling the comment submission.
        template_name: The template name used to render the view.
    """
    model = Article
    form_class = CommentForm
    template_name = 'articles/article_detail.html'

    def post(self, request, *args, **kwargs):
        """
        This method handles POST requests for the view, retrieving the
        'Article' object being commented on and calling its parent's
        implementation.

        :param request: The incoming request.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The HTTP response.
        """
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        A method called when the form submission is valid.

        It attaches the article and the comment author (authenticated user)
        to the comment and saves it to the database. It then calls the parent's
        implementation of the method.

        :param form: The form being submitted.
        :return: The HTTP response.
        """
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        This method returns the URL for the detail page of the commented
        article after successful comment form submission.

        :return: It returns the URL for the detail page of the
            commented article.
        """
        article = self.get_object()
        success_url = reverse(
            viewname='article_detail',
            kwargs={
                'pk': article.pk
            }
        )
        return success_url


class ArticleDetailView(LoginRequiredMixin, View):
    """
    A class-based view in Django that handles both GET and POST requests for the detail page of an 'Article' object.

    This view requires the user to be logged in (via the 'LoginRequiredMixin'
    mixin) and uses the 'ArticleDetailGet' and 'ArticleDetailPost' views
    to handle the GET and POST requests, respectively.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the view.

        This method calls the 'ArticleDetailGet' view to handle the request.

        :param request: The incoming GET request.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The HTTP response.n:
        """
        view = ArticleDetailGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for the view.

        This method calls the 'ArticleDetailPost' view to handle the request.

        :param request: The incoming POST request.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The HTTP response.
        """
        view = ArticleDetailPost.as_view()
        return view(request, *args, **kwargs)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    A class-based view for creating a new article.

    This view extends the Django 'LoginRequiredMixin' mixin to ensure that
    only authenticated users can access it. It also uses the built-in Django
    generic view 'CreateView' to handle the creation of a new article instance.

    Attributes:
        model: The model to use for the view.
        fields: The model fields to display in the form for creating a new
            article instance.
        template_name: The name of the template to use for the view.
    """
    model = Article
    fields = ('title', 'body')
    template_name = 'articles/article_new.html'

    def form_valid(self, form):
        """
        A method called when the form submission is valid.

        This method adds the authenticated user as the article's author
        before saving the form to the database.

        It then calls the parent's implementation of the method.

        :param form: The form being submitted.
        :return: The HTTP response.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A class-based view for updating an article.

    This view extends the Django's 'LoginRequiredMixin' mixin to ensure
    that only authenticated users can access it and the
    'UserPassesTestMixin' mixin to ensure that only the author of an
    article can edit its info. It also uses the built-in Django generic
    view 'UpdateView' to handle the update of an existing article.

    Attributes:
        model: The model to use for the view.
        fields: The model fields to display in the form for updating an article.
        template_name: The name of the template to use for the view.
    """
    model = Article
    fields = ('title', 'body')
    template_name = 'articles/article_edit.html'

    def test_func(self):
        """
        A test method to check if the current user is the article author.

        The method checks if the current authenticated user is the article
        author by comparing it with the 'obj.author' (obj is the instance of
        the article to be updated).

        :return: True, if the current authenticated user is the article author,
            False otherwise.
        """
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A class-based view for deleting an article.

    This view extends the Django's 'LoginRequiredMixin' mixin to ensure that
    only authenticated users can access it and the 'UserPassesTestMixin'
    mixin to ensure that only the author of an article can delete it.
    It also uses the built-in Django generic view 'DeleteView' to handle
    the article deletion process.

    Attributes:
        - model: The model to use for the view.
        - template_name: The name of the template to use for the view.
        - success_url: The success URL of an article deletion.
    """
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        """
        A test method to check if the current user is the article author.

        The method checks if the current authenticated user is the article
        author by comparing it with the 'obj.author' (obj is the instance of
        the article to be updated).

        :return: True, if the current authenticated user is the article author,
            False otherwise.
        """
        obj = self.get_object()
        return obj.author == self.request.user
