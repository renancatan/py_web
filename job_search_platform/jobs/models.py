from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    min_salary = models.FloatField(null=True)
    max_salary = models.FloatField(null=True)

    def __str__(self):
        return {"title": self.title, "maxSalary": f"{self.max_salary}"}
