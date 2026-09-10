from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Lead(BaseModel):

    class Status(models.TextChoices):
        NEW = "New", "New"
        CONTACTED = "Contacted", "Contacted"
        QUALIFIED = "Qualified", "Qualified"
        LOST = "Lost", "Lost"

    name = models.CharField(max_length=150)
    email = models.EmailField()
    company = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)

    status = models.CharField(max_length=20,choices=Status.choices,default=Status.NEW)
    lost_reason = models.TextField(blank=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="leads")
    class Meta:
        constraints = [ models.UniqueConstraint( fields=["owner", "email"],name="unique_email_per_owner") ]

    def __str__(self):
        return self.name


class LeadNote(BaseModel):

    lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name="notes")

    content = models.TextField()

    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="lead_notes")



    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Note - {self.lead.name}"
