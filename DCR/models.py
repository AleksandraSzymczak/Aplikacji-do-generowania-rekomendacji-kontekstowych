from django.db import models

class UserChoices(models.Model):
    c1_choices = models.JSONField()
    selection_type_c1 = models.CharField(max_length=20)
    c2_choices = models.JSONField()
    selection_type_c2 = models.CharField(max_length=20)
    c3_choices = models.JSONField()
    selection_type_c3 = models.CharField(max_length=20)
    weights = models.JSONField(default=dict) 
