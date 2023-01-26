from django.urls import path

from . import views
from snippets.views import  SnippetListView, IndexView, LoginFormView, LogoutView, Snippet_Add, UserListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('snippets/list/', SnippetListView.as_view(), name='list_snippets'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('snippets/user/', UserListView.as_view(), name='user_snippets'),
    path('snippets/add/', Snippet_Add.as_view(), name='snippet_add'),    
    path('snippets/<str:slug_url>/<int:id>', views.language, name='language'),
    path('snippets/<int:id>/edit/', views.snippet_edit, name='snippet_edit'),
    path('snippets/<int:id>/delete/', views.snippet_delete, name='snippet_delete'),
]