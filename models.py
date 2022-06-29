from django.db import models

class Blog(models.Model):
    """Blog tworzony przez użytkownika."""
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Reprezentacja modelu w postaci ciągu tekstowego."""
        return self.title

class Post(models.Model):
    """Post zamieszczony na blogu."""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Reprezentacja modelu w postaci ciągu tekstowego."""
        return f"{self.text[:50]}..."



