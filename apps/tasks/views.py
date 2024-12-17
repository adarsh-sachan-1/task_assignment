# tasks/views.py
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer
from rest_framework import permissions

class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class TaskPagination(PageNumberPagination):
    page_size = 5

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, AdminOnlyPermission]
    pagination_class = TaskPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['due_date', 'status']
    search_fields = ['task_name', 'status']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_active = False
        task.save()
        return Response({'status': 'Task marked as inactive'})
