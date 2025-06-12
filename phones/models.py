from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Phone(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    specs = models.JSONField()
    image = models.ImageField(upload_to='phones/', null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} {self.model}"
