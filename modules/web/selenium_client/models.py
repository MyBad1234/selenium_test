from django.db import models


class Search(models.Model):
    """model for test my selenium script inj docker"""

    company = models.CharField(max_length=200)
    word = models.CharField(max_length=200)
    result = models.CharField(max_length=50, null=True, blank=True)
