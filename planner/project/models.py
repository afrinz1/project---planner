from django.db import models

import uuid 

from django_ckeditor_5.fields import CKEditor5Field



# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4) # we are doing this in place of id so it must be unqiue4
                                                            # we user onlu uuid and not uuid() because if call uuid() it will get called every single time we run the server

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)  #it will be created during th time of creation

    updated_at = models.DateTimeField(auto_now_add=True) # when we do a updation it will update the current time

    class Meta:

        abstract = True


class Project(BaseClass):

    name = models.CharField(max_length=250)

    description = CKEditor5Field()

    document = models.FileField(upload_to='project-documents')

    class Meta:

        verbose_name = 'Projects'
        verbose_name_plural = 'Project'

    def __str__(self):

        return self.name



class AssignedProjects(BaseClass):
    # Stores information about a project assigned to a team

    # Connects this record to ONE project.
    # PROTECT = Don't allow the project to be deleted
    # while this record is still using it.
    
    project = models.ForeignKey(
        'Project',
        on_delete=models.PROTECT,
        related_name='project'
    )

    # Connects this record to ONE coordinator (boss).
    # CASCADE = If the coordinator's profile is deleted,
    # this assigned-project record will also be deleted.
    coordinator = models.ForeignKey(
        'authentication.Profile',
        on_delete=models.CASCADE,
        related_name='coordinator'
    )

    # Connects this record to MULTIPLE developers.
    # One project can have many developers, and one developer
    # can work on many projects.
    developers = models.ManyToManyField(
        'authentication.Profile'
    )

    # How long the project is expected to take.
    # Example: 30 days.
    project_duration = models.IntegerField()

    project_start_date = models.DateField()

    # The expected date the project will finish.
    # Example: 2026-12-15.
    project_tentative_end_date = models.DateField()

    # Tracks whether the project is finished.
    # False by default = not finished yet.
    # True = finished.
    completed = models.BooleanField(default=False)

    # The actual date the project was completed.
    # null=True = the database can store no date (NULL).
    # blank=True = this field can be left empty in forms.
    # Useful because an unfinished project has no completion date.
    completed_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = 'Assigned Projects'
        verbose_name_plural = 'Assigned Project'

    def __str__(self):

        return f'{self.project.name}-{self.project_start_date}'


class PriorityChoices(models.TextChoices):

    LOW = 'Low','Low'

    MEDIUM = 'Medium','Medium'

    HIGH = 'High','High'


class Task(BaseClass):

    assigned_project = models.ForeignKey('AssignedProjects',on_delete=models.PROTECT,related_name='task_project')

    assigned_to = models.ForeignKey('authentication.Profile',on_delete=models.PROTECT,related_name='task_assigned_to')

    title = models.CharField(max_length=255)

    description = models.TextField()
    
    priority = models.CharField(max_length = 15,choices=PriorityChoices.choices)
    
    duration = models.TimeField(null = True,blank=True)

    start_date = models.DateField(null=True,blank=True)

    end_date = models.DateField(null=True,blank=True)

    completed = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Task'

        verbose_name_plural = 'Tasks'

    def __str__(self):

        return f'{self.assigned_project.project.name}--{self.assigned_to.first_name}--{self.title}'