from django.urls import path, include
from .views import CustomLoginView, TaskCreate, TaskDetail, TaskList, TaskUpdate, TaskDelete, UserRegistrationPage
from django.contrib.auth.views import LogoutView
from . import views as base_view

urlpatterns = [
    path('', base_view.home, name='home'),
    path('profile/', TaskList.as_view(), name="task-list"),
    path('task-detail/<int:pk>/', TaskDetail.as_view(), name="task-detail"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name="task-delete"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
    path('register/', UserRegistrationPage.as_view(), name="register")
]