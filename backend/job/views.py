from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .models import Job
from.filters import JobsFilter
from .serializers import Jobserializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Min, Max, Count

# Create your views here.
@api_view(['GET'])

def getallJobs(request):
    filterset=JobsFilter(request.GET,queryset=Job.objects.all().order_by('id'))
    count=filterset.qs.count()
    result_per_page=4
    paginator=PageNumberPagination()
    paginator.page_size=result_per_page
    paginated_jobs=paginator.paginate_queryset(filterset.qs,request)
    serializer= Jobserializer(paginated_jobs,many=True)
    return Response({
        "count":count,
        "result_per_page":result_per_page,
        "jobs":serializer.data
        })



@api_view(['GET'])
def getJobById(request,pk):
    job=get_object_or_404(Job,id=pk)
    serializer=Jobserializer(job,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def createjob(request):
    request.data['user']=request.user
    data = request.data

    job = Job.objects.create(**data)

    serializer = Jobserializer(job, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request,pk):
    job=get_object_or_404(Job,id=pk)
    
    if job.user!=request.user:
        return Response({"message":"You cannot update this job"},status=status.HTTP_403_FORBIDDEN)
    
    job.title=request.data['title']
    job.description=request.data['description']
    job.company=request.data['company']
    job.address=request.data['address']
    job.jobtype=request.data['jobtype']
    job.industry=request.data['industry']
    job.experience=request.data['experience']
    job.salary=request.data['salary']
    job.point=request.data['point']
    job.jobtype=request.data['jobtype']
    job.position=request.data['position']
    
    job.save()
    serializer=Jobserializer(job,many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteJob(request,pk):
    job=get_object_or_404(Job,id=pk)
    if job.user!=request.user:
        return Response({"message":"You cannot delete this job"},status=status.HTTP_403_FORBIDDEN)
    job.delete()
    return Response({'message':'Job is deleted succesfully'},status=status.HTTP_200_OK)

@api_view(['GET'])
def getTopicStats(request, topic):

    args = { 'title__icontains': topic }
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response({ 'message': 'Not stats found for {topic}'.format(topic=topic) })

    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        avg_salary = Avg('salary'),
        min_salary = Min('salary'),
        max_salary = Max('salary')
    )

    return Response(stats)