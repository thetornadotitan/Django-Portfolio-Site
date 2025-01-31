from django.db import models
from django.contrib.auth.models import User
from shared.utils import replace_font_quotes, clean_iframes

class ProjectLinks(models.Model):
    text = models.CharField(max_length=255)
    url = models.TextField()
    
    def __str__(self):
        return f"{self.text} ({self.url})"
    
    class Meta:
        ordering = ["text"]
        verbose_name = "Link"
        verbose_name_plural = "Links"
    
class ProjectTags(models.Model):
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.text}"
    
    class Meta:
        ordering = ["text"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Project(models.Model):
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)  # Updated field
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    tags = models.ManyToManyField(ProjectTags, related_name="projects", blank=True)
    links = models.ManyToManyField(ProjectLinks, related_name="projects", blank=True) 
    order = models.IntegerField()

    def __str__(self):
        return "ID: " + str(self.pk) + " - " + self.title

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        
    def save(self, *args, **kwargs):
        # Clean iframes and replace escaped quotes before saving the body and summary
        self.body = replace_font_quotes(clean_iframes(self.body))

        super().save(*args, **kwargs)