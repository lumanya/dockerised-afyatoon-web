from PIL import Image
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Therapist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)   
    specilization = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to='profile')
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_photo:
            img = Image.open(self.profile_photo.path)

            # resize the photo

            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.profile_photo.path)



class TimeSlot(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        """
        Custom validation to ensure start_time is before end_time.
        """
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")
        
    def __str__(self):
        return f'{self.therapist} - {self.day_of_week}: {self.start_time} - {self.end_time}'
        

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.therapist.full_name} - {self.date_and_time}'
    




    

