from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .utilities import *
from tarantool.error import DatabaseError
import logging


logger = logging.getLogger('debug')

@api_view(['POST'])
def post(request):
    logger.debug('got post request')
    data = request.data
    if not db.valid_post_data(data):
        logger.debug("Data not correct")
        return Response('Data not correct!!!', status=status.HTTP_409_CONFLICT)
    try:
        db.post_db(data)
    except DatabaseError:
        logger.exception("error")
        return Response('This key already exist!!!', status=status.HTTP_409_CONFLICT)
    logger.debug('post finished')
    return Response('OK', status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def get_put_delete(request, obj_id):
    logger.debug(f'func get_put_delete with id:{obj_id} method: {request.method} started')
    obj = db.get_db(obj_id)
    if not obj:
        logger.debug(f'id:{obj_id} not found!')
        return Response('Error', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        response_data = {}
        response_data['key'] = obj[0][1]
        response_data['value'] = obj[0][2]
        return Response(response_data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        db.delete_db(obj_id)
    else:
        data = request.data
        if not db.valid_put_data(data):
            logger.debug("Data not correct")
            return Response('Data not correct!!!', status=status.HTTP_409_CONFLICT)
        db.put_db(obj_id, data)
    return Response('OK', status=status.HTTP_200_OK)
# POST GET PUT DELETE