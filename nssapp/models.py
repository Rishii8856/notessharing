from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'nsuser'),
        
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic')


class UserReg(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"User not associated - {self.mobilenumber}"


class Notes(models.Model):
    nsuser = models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    notestitle = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    notesdesc = models.TextField()
    file1 = models.FileField(upload_to='notes_files', null=True, blank=True)
    file2 = models.FileField(upload_to='notes_files', null=True, blank=True)
    file3 = models.FileField(upload_to='notes_files', null=True, blank=True)
    file4 = models.FileField(upload_to='notes_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.notestitle


##  Download 
User = get_user_model()

class DownloadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey('Notes', on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} downloaded {self.note}"
    
## Visitor Tack karnya sathi

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField()
    visit_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)  # seconds

    def __str__(self):
        return self.ip_address