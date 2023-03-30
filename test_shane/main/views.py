from django.http import HttpResponse

# Create your views here.

# Define @api_view decorator
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from main.tasks import call_api, readMongo, readPostgres, getParallel




@api_view(['POST'])
def count_endpoint(request):
    print("Entered in first endpoint!")

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

        print("Running 10+ Tasks............")
        user_list = []

        # Create at least 10 tasks with celery
        for i in range(count):

            user_list.append(call_api(count, getParallel.delay().get()))


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