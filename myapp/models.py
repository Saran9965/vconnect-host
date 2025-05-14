from django.db import models
from django.contrib.auth.models import User
from django.db import models

class empdata(models.Model):
    name = models.CharField(max_length=50, default='')
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128,default='')
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.BigIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    SERVICE_CHOICES = [
        ('PLUMBER', 'Plumber'),
        ('ELECTRICIAN', 'Electrician'),
        ('CARPENTER', 'Carpenter'),
        ('TV TECH', 'TV Technician'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"


class Rating(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.service.name} {self.stars} stars"


class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews') 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reviewed {self.service.name} - '{self.review[:30]}...'"
