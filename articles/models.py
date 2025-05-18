from django.conf import settings
from django.db import models
from django.urls import reverse


class Article(models.Model):
    """
    A model that represents a newspaper article.

    Attributes:
        title: The title of the article.
        body: The body or content of the article.
        date: The article creation date and time.
        author: The user who is the author of the article.
    """
    title = models.CharField(
        max_length=255
    )
    body = models.TextField()
    date = models.DateTimeField(
        auto_now_add=True
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        It returns the string representation of an 'Article' object.
        :return: The title of the article.
        """
        return self.title

    def get_absolute_url(self):
        """
        It returns the absolute URL of the detail page for an Article object.
        :return: The absolute URL of the detail page for the article.
        """
        article_detail_url = reverse(
            viewname='article_detail',
            kwargs={
                'pk': self.pk
            }
        )
        return article_detail_url


class Comment(models.Model):
    """
    A model that represents a comment made on a newspaper article.
    """
    comment = models.CharField(
        max_length=150
    )
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        It returns the string representation of a 'Comment' object.
        :return: The comment content.
        """
        return self.comment

    def get_absolute_url(self):
        """
        It returns the absolute URL of the Article list.
        :return: The absolute URL for the article list.
        """
        return reverse(viewname='article_list')
