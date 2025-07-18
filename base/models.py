from django.db import models
import uuid

class Basemodel(models.Model):
    uid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False);
    created_at=models.DateTimeField(auto_now=True);
    updated_at=models.DateTimeField(auto_now_add=True);
    
    class Meta:
        # for treating django this as class not model
        abstract=True