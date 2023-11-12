# models.py
from django.db import models

class NewsArticle(models.Model):
    end_year = models.CharField(max_length=10, blank=True)
    intensity = models.CharField(max_length=10)
    sector = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    insight = models.TextField()
    url = models.URLField()
    region = models.CharField(max_length=255)
    start_year = models.CharField(max_length=10, blank=True)
    impact = models.CharField(max_length=255, blank=True)
    added = models.DateTimeField()
    published = models.DateTimeField(null=True, default=None)
    country = models.CharField(max_length=255)
    relevance = models.CharField(max_length=10)
    pestle = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    likelihood = models.CharField(max_length=10)
    

    def __str__(self):
        return self.title
