from django.db import models


class NewsletterRequest(models.Model):
    order = models.OneToOneField("pretixbase.Order", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
