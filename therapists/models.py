from PIL import Image
from django.db import models
from django.conf import settings


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


class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField()
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.therapist.full_name} - {self.date_and_time}'
    



    

