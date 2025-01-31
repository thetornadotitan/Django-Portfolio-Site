from django.db import models
from django.contrib.auth.models import User
from shared.utils import replace_font_quotes, clean_iframes

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    summary = models.TextField()
    body = models.TextField()

    def __str__(self):
        return "ID: " + str(self.pk) + " - " + self.title

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        
    def save(self, *args, **kwargs):
        # Clean iframes and replace escaped quotes before saving the body and summary
        self.body = replace_font_quotes(clean_iframes(self.body))
        self.summary = replace_font_quotes(clean_iframes(self.summary))

        super().save(*args, **kwargs)