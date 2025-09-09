from django.urls import path
from .views import signup, login, logout,task_list, task_detail, team_list, mark_task_completed, add_member_to_team, team_tasks, user_report

urlpatterns = [
    
    # Authentication endpoints
    path('auth/signup/', signup, name='signup'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    
    # Task endpoints
    path('tasks/', task_list, name='task-list'),# get and post tasks
    path('tasks/<int:pk>/', task_detail, name='task-detail'),# get put delete tasks
    path('tasks/<int:pk>/completed/', mark_task_completed, name='mark-task-complete'),# put complete task
    
    # Team endpoints
    path('teams/', team_list, name='team-list'),#post teams
    path('teams/<int:team_id>/add-member/', add_member_to_team, name='add-member-to-team'),# post add member to team
    path('teams/<int:team_id>/tasks/', team_tasks, name='team-taks'),# get team tasks
    
    # Reports endpoints
    path('reports/summary/', user_report, name='user-report'),# get user report
]