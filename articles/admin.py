from django.contrib import admin

from articles.models import Comment, Article


class CommentInline(admin.TabularInline):
    """
    An inline admin class for the Comment model.

    This class allows you to interact with 'Comment' objects on the same page
    as the parent Article object in the Django admin interface. These comments
    are displayed in a tabular way.

    Attributes:
        model: The inline class base model.
    """
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    """
    An admin class for the Article model.

    It allows you to manage Article objects in the Django admin interface.
    It includes the 'CommentInline' class as an inline so that 'Comment'
    objects can be displayed and manipulated on the same page as the parent
    Article object.

    Attributes:
        inlines: A list of inline classes to use with the Article model.
    """
    inlines = [CommentInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
