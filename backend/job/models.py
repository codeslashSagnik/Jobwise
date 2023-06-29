from django.db import models
from datetime import *
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
import geocoder,os
class Jobtype(models.TextChoices):
    Permanent='Permanent'
    Temporary='Temporary'
    Internship='Internship'
    
class Education(models.TextChoices):
    High_School='High School'
    Bachelors='Bachelors'
    Masters='Masters'
    Phd='PhD'

class Industry(models.TextChoices):
    IT = 'Information Technology'
    Finance = 'Finance'
    Healthcare = 'Healthcare'
    Education = 'Education'
    Manufacturing = 'Manufacturing'
    Other = 'Others'

class Experience(models.TextChoices):
    No_Experience='No Experience',
    One_Year='1 Year'
    Two_Year='2 Years'
    Three_Year='3 Years'
    More_Than_Three_Year='3 Years above'
def return_date_time_added():
    now=datetime.now()
    return now + timedelta(days=10)
class Job(models.Model):
    title=models.CharField(max_length=50,null=False)
    description=models.TextField(max_length=200,null=False)
    company=models.TextField(max_length=100,null=False)
    address=models.CharField(max_length=150,null=False)
    email=models.EmailField(max_length=254,null=False)
    jobtype=models.CharField(
        max_length=60,
        choices=Jobtype.choices,
        default=Jobtype.Permanent
        )
    education=models.CharField(
        max_length=60,
        choices=Education.choices,
        default=Education.Bachelors
        )
    industry=models.CharField(
        max_length=60,
        choices=Industry.choices,
        default=Industry.IT
    )
    experience=models.CharField(
        max_length=60,
        choices=Experience.choices,
        default=Experience.No_Experience
    )
    
    salary=models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(1000000000)])
    point=gismodels.PointField(default=Point(0.0, 0.0))
    last_date=models.DateTimeField(default=return_date_time_added)
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    def save(self,*args, **kwargs):
        g=geocoder.mapquest(self.address, key=os.environ.get('GEOCODER_API'))
        print(g)
        lng=g.lng
        lat=g.lat
        self.point=Point(lng,lat)
        super(Job,self).save(*args, **kwargs)