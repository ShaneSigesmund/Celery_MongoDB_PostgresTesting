import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# Define @api_view decorator
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from redis import Redis

from main.tasks import call_api
from main.tasks import get_database_mongo
from main.tasks import get_database_postgres
from main.tasks import readMongo
from main.tasks import readPostgres

from main.celery import add

@api_view(['POST'])
def count_endpoint(request):
    print("hit count endpoint")

    # Call get_database_mongo function
    collection_name = get_database_mongo()["users"]

    count = request.data.get('count', None)

    if count is None:
        return Response({'error': 'No count provided'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        count = int(count)
    except ValueError:
        return Response({'error': 'Invalid count provided'},
                        status=status.HTTP_400_BAD_REQUEST)

    # If the value of count is 10 then you will be create 10 task and send it to queue for execution.
    if count >= 10:
        # Create empty list
        user_list = []
        user_list2 = []

        # Create at least 10 tasks with celery
        result = call_api.delay(count)

        result = result.ready()
        print(result)
        for i in range(count):
            result = call_api.delay(count)
            result = result.get()

            print(type(result))


            if result.ready() == True:
                result = result.get()

                user_list.append(readMongo())

                user_list2.append(readPostgres())

        return HttpResponse(user_list, status=status.HTTP_200_OK)
    # If count is less than 10
    else:
        # Call the function
        call_api(count)
        response_data = {'message': 'Count endpoint called {} times'.format(count)}

        return Response(response_data, status=status.HTTP_200_OK)


# Make get request
@api_view(['GET'])
def get_all_data_mdb(request):

    user_list = []

    user_list = readMongo()

    # Return user_list
    return HttpResponse(user_list, status=status.HTTP_200_OK)


# Make similar thing but for postgres
@api_view(['GET'])
def get_all_data_psql(request):

    user_list = []

    user_list = readPostgres()
    # Return user_list
    return HttpResponse(user_list, status=status.HTTP_200_OK)