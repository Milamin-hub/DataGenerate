from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job = models.CharField(max_length=100)
    email = models.EmailField()
    domain = models.URLField()
    phone_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    text = models.TextField()
    integer = models.IntegerField()
    address = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"