from django.db import models
import django
import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at
            else "not leaved"
        )

    def get_duration(self):
        if self.leaved_at:
            duration = self.leaved_at - self.entered_at
            return duration
        else:
            duration = django.utils.timezone.now() - self.entered_at
            return datetime.timedelta(seconds=round(duration.total_seconds()))

    def format_duration(self, duration):
        if duration.total_seconds() < 3600:
            return str(duration)[-5:]
        elif duration.total_seconds() < 36000:
            return '0' + str(duration)
        else:
            return str(duration)

    def is_visit_long(self, minutes=60):
        return self.get_duration().total_seconds() > minutes * 60
