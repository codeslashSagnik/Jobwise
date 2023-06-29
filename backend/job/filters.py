from django_filters import rest_framework as filters
from .models import Job

class JobsFilter(filters.FilterSet):
    createdAt = filters.DateFromToRangeFilter()
    experience = filters.CharFilter(field_name='experience', lookup_expr='exact')
    industry = filters.CharFilter(field_name='industry', lookup_expr='exact')
    education = filters.CharFilter(field_name='education', lookup_expr='exact')
    keyword=filters.CharFilter(field_name="title",lookup_expr='icontains')
    location=filters.CharFilter(field_name='address',lookup_expr='icontains')
    min_salary = filters.NumberFilter(field_name='salary' or  0, lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name='salary' or 10000000 , lookup_expr='lte')

    class Meta:
        model = Job
        fields = ('location','keyword','education', 'jobtype', 'experience', 'industry', 'createdAt','min_salary','max_salary')
