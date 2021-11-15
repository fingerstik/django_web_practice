from django.db import models
from datetime import datetime, timedelta

from django.utils import timezone
# Create your models here.


class Posting(models.Model):
    posting_title = models.CharField(max_length=128)
    posting_body = models.TextField()
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.posting_title

    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.posting_date
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.posting_date.date()
            return str(int(time.days)) + '일 전'
        else:
            return False
