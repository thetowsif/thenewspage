from django import forms

from articles.models import Comment


class CommentForm(forms.ModelForm):
    """
    It is a form for creating comments on articles.

    This form is 'Comment' model-based and only includes a field for the
    comment text and can be used to create new comments on an article.
    """
    class Meta:
        """
        Metadata for the CommentForm.

        Attributes:
            model (Comment): The model that the form is based.
            fields (tuple): The model fields included in the form.
        """
        model = Comment
        fields = ('comment', )
