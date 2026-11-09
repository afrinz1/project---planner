from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView,ListAPIView

from . models import Project , AssignedProjects

from .serializer import ProjectSerializer

from .serializer import AssignedProjectSerializer

from rest_framework.views import Response

from . models import Task

from .serializer import TaskSerializer

from rest_framework.views import APIView

from planner.utils import generate_tasks

from django.db import transaction
# Create your views here.

class ProjectListCreateView(ListCreateAPIView):

    queryset = Project.objects.filter(active_status=True)

    serializer_class = ProjectSerializer

class ProjectRetrieveDestroyUpdateView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'
    queryset = Project.objects.filter(active_status=True)

    serializer_class = ProjectSerializer

    def perform_destroy(self, instance):
        instance.active_status = False
        instance.save()


class AssignedProjectListCreateView(ListCreateAPIView):

    queryset = AssignedProjects.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developers')
    serializer_class = AssignedProjectSerializer

class AssignedProjectRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = AssignedProjects.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developers')

    serializer_class = AssignedProjectSerializer

    def soft_delete(self,instance):
        instance.active_status = False
        instance.save()

class TaskListCreateView(ListCreateAPIView):

    serializer_class = TaskSerializer

    def get_queryset(self):

        uuid = self.kwargs.get('uuid')

        assigned_project = AssignedProjects.objects.get(uuid = uuid)

        tasks = Task.objects.filter(active_status=True,assigned_project=assigned_project)

        return tasks

    def perform_create(self, serializer):

        uuid = self.kwargs.get('uuid')

        assigned_project = AssignedProjects.objects.get(uuid = uuid)

        serializer.save(assigned_project=assigned_project)

class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Task.objects.filter(active_status=True).select_related('assigned_project','assigned_to')

    serializer_class = TaskSerializer

    def perform_destroy(self, instance):
        instance.active_status = False
        instance.save()

class GenerateTaskWithAIView(APIView):

    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        assigned_project = AssignedProjects.objects.get(uuid=uuid)

        response,developers = generate_tasks(assigned_project)

        tasks=[Task(
            assigned_project=assigned_project,
            assigned_to_id=task.developer_id,
            title = task.title,
            description = task.description,
            priority = task.priority
            )
            for task in response.tasks if task.developer_id in developers]

        with transaction.atomic():
                Task.objects.bulk_create(tasks)

        print(response.tasks)

        return Response(status=200)

    


