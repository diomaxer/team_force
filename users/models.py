from django.db import models


class Skills(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40, null=True, blank=True)
    languages = models.ManyToManyField(Language)
    skills = models.ManyToManyField(Skills)
    hobie = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
