"""Demo API"""
import json
from django.core import serializers
from django.http import HttpResponseNotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.restapis.models.demo import Demo


def _model_to_json(rec):
    data = serializers.serialize('json', rec)
    struct = json.loads(data)
    items = []
    index = 0
    for item in rec:
        struct[index]['fields']['id'] = struct[index]['pk']
        items.append(struct[index]['fields'])
        index += 1

    return Response(items)


def _req_to_json(request: Request):
    return json.loads(request.body.decode('utf-8'))


class DemoAPI(APIView):

    def post(self, request: Request, *args, **kwargs):
        try:
            data = _req_to_json(request)
            rec = Demo(message=data['message'])
            rec.save()

            return Response({ 'status': 'Record had been created successfully!' })
        except:
            return Response({ 'status': 'Failed to create a record!' })    

    def get(self, request: Request, *args, **kwargs):
        try:
            records = Demo.objects.all()

            if records is None or len(records) == 0:
                return HttpResponseNotFound('Records not found!')

            return _model_to_json(records)
        except:
            return HttpResponseNotFound('Failed to fetch records!')

    def delete(self, request: Request, *args, **kwargs):
        return Response('DELETE api called!')

    def put(self, request: Request, *args, **kwargs):
        return Response('PUT api called!')
