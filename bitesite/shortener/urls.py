from django.urls import path

from .views import about, feedback_thanks, logout_user, \
    RegisterUser, LoginUser, MyLinks, CreateShortLink, FeedbackFormView, EditShortLink, DeleteShortLink

urlpatterns = [
    path('about/', about, name='about'),
    path('create_short_link/', CreateShortLink.as_view(), name='create_short_link'),
    path('edit_short_link/<int:pk>', EditShortLink.as_view(), name='edit_short_link'),
    path('delete_short_link/<int:pk>', DeleteShortLink.as_view(), name='delete_short_link'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('feedback_thanks/', feedback_thanks, name='feedback_thanks'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('my_links/', MyLinks.as_view(), name='my_links'),
]
