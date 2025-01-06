from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .fields import STAKES_CHOICES
from datetime import timedelta


class Casino(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class PokerSession(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player')
    casino = models.ForeignKey(Casino, default = "Bogata", on_delete=models.CASCADE)
    stakes = models.CharField(max_length=20, default = "13", choices=STAKES_CHOICES)
    date = models.DateField()
    hours = models.IntegerField() 
    buy_in = models.IntegerField() 
    cash_out = models.IntegerField() 
    notes = models.TextField(max_length=5000, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    end_session = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        """Return a string representation of the PokerSession with the created date."""
        return f"PokerSession on {self.created.strftime('%A, %b %d, %Y')}"

    @property
    def win_loss(self):
        return self.cash_out - self.buy_in

    @property
    def win_rate_per_hour(self):
        duration = self.session_duration
        if duration > 0:  # Avoid division by zero
            return self.win_loss / duration
        return 0  # Return 0 if the session duration is zero


    @property
    def total_session_hours(self):
        """Calculate and format the duration between created and end_session with the day of the week."""
        if self.end_session:
            duration = self.end_session - self.created
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            start_day = self.created.strftime('%A')  # Get day of the week (e.g., Monday, Tuesday)
            end_day = self.end_session.strftime('%A')  # Day of the week for the end session
            return (
                f"Started on {start_day}, ended on {end_day}. "
                f"Duration: {int(hours)}h {int(minutes)}m {int(seconds)}s"
            )
        return "Not ended yet"



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Ensure unique tags
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SessionNotes(models.Model):
    pokersession = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name='Session')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="session_notes")
    notes = models.TextField(max_length=5000, blank=True, null=True)
    takeaway = models.TextField(max_length=1000,  blank=True, null=True)
    
    
    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return self.notes[:50] if self.notes else "No notes"