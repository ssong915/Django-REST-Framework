from django.db import models
from django.conf import settings

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    hits = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def update_counter(self):
        self.hits = self.hits+1
        self.save()