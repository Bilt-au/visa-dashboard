from django.db import models

class VisaType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MonthYear(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class VisaData(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED'
        HOLD = 'HOLD'
        INVITED = 'INVITED'
        LODGED = 'LODGED'
        CLOSED = 'CLOSED'


    month_year = models.ForeignKey(MonthYear, on_delete=models.CASCADE)
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=Status.choices)
    points = models.IntegerField()
    count = models.IntegerField()

    def __str__(self):
        return f"{self.month_year} - {self.visa_type} - {self.occupation}"