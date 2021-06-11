from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Student(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.firstname


class Diary(models.Model):
    student = models.OneToOneField(Student, null=True, on_delete=models.CASCADE, related_name='diary')
    avg_score = models.FloatField(max_length=20)

    def __str__(self):
        return f'{self.student} - {self.avg_score}'


class Book(models.Model):
    name = models.CharField(max_length=50)
    pages = models.IntegerField()
    students = models.ManyToManyField(Student, related_name='books')

    def __str__(self):
        return self.name
