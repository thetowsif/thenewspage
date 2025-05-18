from django.urls import path

from articles.views import ArticleListView, ArticleDetailView, \
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path(
        route='',
        view=ArticleListView.as_view(),
        name='article_list'
    ),
    path(
        route='details/<int:pk>',
        view=ArticleDetailView.as_view(),
        name='article_detail'
    ),
    path(
        route='new/',
        view=ArticleCreateView.as_view(),
        name='article_new'
    ),
    path(
        route='edit/<int:pk>',
        view=ArticleUpdateView.as_view(),
        name='article_edit'
    ),
    path(
        route='delete/<int:pk>',
        view=ArticleDeleteView.as_view(),
        name='article_delete'
    )
]
