from django.shortcuts import render
from .serializers import UserSerializer, TaskSerializer, TeamSerializer
from .models import Task, Team
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token


# Create your views here.


# User Authentication Views>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Signup view
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)  # directly create
        return Response(
            {
                'message': 'User created successfully',
                'token': token.key,
                'data': serializer.data,
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
# Login view  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                serializer = UserSerializer(user)
                return Response(
    {
        'message': 'Login successful',
        'data': serializer.data
    },
    status=status.HTTP_200_OK
)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        
# Logout view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Frontend will handle session/token removal
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


# Task Related Views>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Task Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):
    # Get
    if request.method == 'GET':
            tasks = Task.objects.filter(assigned_to=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response({
                'message': 'Tasks fetched successfully',
                'data' :serializer.data
            }, status=status.HTTP_200_OK)
        
        # Post
    else:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(assigned_to=request.user)
            return Response({
                'message': 'Task added successfully',
                'data' :serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Task Update, Delete
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk, assigned_to=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    # Put 
    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Task updated successfully',
                'data' :serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Delete
    elif request.method == 'DELETE':
        if pk is None:
            return Response({'error': 'Task ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            task.delete()
        
        return Response({
                'message': 'Task deleted successfully'
            },status=status.HTTP_204_NO_CONTENT)

# Mark as completed
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_task_completed(request, pk):
    try:
        task = Task.objects.get(pk=pk, assigned_to=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    task.status = 'completed'
    task.save()
    serializer = TaskSerializer(task)
    return Response({
                'message': 'Task marked as completed',
                'data' :serializer.data
            }, status=status.HTTP_200_OK)
    
    
#Team Related Views>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    
# Team Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def team_list(request):
    if request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Team added successfully',
                'data' :serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
   
# Add member to team 
@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def add_member_to_team(request, team_id):
    # check team exists or not
    try:
        team = Team.objects.get(pk=team_id)
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # check user exists or not
    username = request.data.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # add user to team
    team.members.add(user)
    team.save()
    serializer = TeamSerializer(team)
    return Response({
                'message': 'Member added to team successfully',
                'username': user.username,
                'data' :serializer.data
            }, status=status.HTTP_200_OK)
    
# get team tasks
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_tasks(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
    
    tasks = team.tasks.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response({
                'message': 'Team tasks fetched successfully',
                'data' :serializer.data
            }, status=status.HTTP_200_OK)

    
#Report Related Views>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Reports
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_report(request):
    
    # Task stats per user
    completed_tasks = Task.objects.filter(assigned_to = request.user,status='completed').count()
    if completed_tasks is None:
        return Response({'error': 'No completed tasks found for the user'}, status=status.HTTP_404_NOT_FOUND)
    
    pending_tasks = Task.objects.filter(assigned_to = request.user,status='pending').count()
    if pending_tasks is None:
        return Response({'error': 'No pending tasks found for the user'}, status=status.HTTP_404_NOT_FOUND)
    
    in_progress_tasks = Task.objects.filter(assigned_to = request.user,status='in_progress').count()
    if in_progress_tasks is None:
        return Response({'error': 'No in-progress tasks found for the user'}, status=status.HTTP_404_NOT_FOUND)
    
    
    return Response({
        'message': 'User report fetched successfully',
        'username': request.user.username,
        'completed_tasks': completed_tasks, 
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        }, status=status.HTTP_200_OK)
    
        