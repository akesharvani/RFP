from django.db import models

# Create your models here.
class RFP(models.Model):
    posted_date = models.CharField(max_length=100, default = "N/A")
    due_date = models.CharField(max_length=100, default = "N/A")
    rfx_bid_number = models.CharField(max_length=100,default = "N/A")
    rfx_type = models.CharField(max_length=100, default = "N/A")
    title = models.CharField(max_length=100,default = "N/A")
    description = models.CharField(max_length=100,default = "N/A")
    buyer_agent_name = models.CharField(max_length=100,default = "N/A")
    buyer_agent_email = models.CharField(max_length=100,default = "N/A")
    buyer_agent_title = models.CharField(max_length=100,default = "N/A")
    sent_to_ms_teams = models.BooleanField(default=False)
