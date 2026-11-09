from rest_framework import serializers


from .models import Project , Task
from .models import AssignedProjects

from authentication.models import Profile
from authentication.serializer import ProfileSerializer

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Project

        fields = '__all__'
        read_only_fields = ['active_status']

class ProjectField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0])

    def to_representation(self, value):
        return ProjectSerializer(value).data
       #this is to convert that instance (category object) into json format

class ProfileField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0])

    def to_representation(self, value):
        return ProfileSerializer(value).data
       #this is to convert that instance (category object) into json format

class AssignedProjectSerializer(serializers.ModelSerializer):

    project = ProjectField(queryset=Project.objects.all())

    coordinator = ProfileField(queryset=Profile.objects.filter(role = 'project coordinator'))
    
    developers = ProfileField(queryset=Profile.objects.filter(role='developer'), many=True)

    class Meta:

        model = AssignedProjects

        fields = '__all__'
        read_only_fields = ['active_status']



class AssignedProjectField(serializers.PrimaryKeyRelatedField):

    def get_attribute(self, instance):

        return getattr(instance,self.source_attrs[0])

    def to_representation(self, value):
        return AssignedProjectSerializer(value).data
       #this is to convert that instance (category object) into json format


class TaskSerializer(serializers.ModelSerializer):

    assigned_project = AssignedProjectField(read_only=True)
    assigned_to = ProfileField(queryset = Profile.objects.filter(role='developer'))

    class Meta:

        model = Task

        fields = '__all__'
        read_only_fields = ['active_status']


        