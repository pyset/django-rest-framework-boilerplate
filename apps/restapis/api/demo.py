"""Demo API"""
import json
from django.core import serializers
from django.http import HttpResponseNotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from apps.restapis.models.demo import Demo
from rest_framework.decorators import action
from django.utils import timezone


class DemoAPI(viewsets.GenericViewSet):
    def _req_to_json(self, request: Request):
        """
        Get the request content as json.

        :param request: The request object.
        :return: The json body.
        """
        return json.loads(request.body.decode('utf-8'))


    def _model_to_json(self, rec):
        """
        Convert model object to json.

        :param rec: The model object.
        :return: The json body.
        """
        data = serializers.serialize('json', rec)
        struct = json.loads(data)
        items = []
        index = 0
        for item in rec:
            struct[index]['fields']['id'] = struct[index]['pk']
            items.append(struct[index]['fields'])
            index += 1

        return Response(items)


    @action(methods=["post"], detail=False, url_path=r"create")
    def post(self, request: Request, *args, **kwargs):
        """
        Create new record.

        :param request:  The request object.
        :param args:
        :param kwargs: Url params,
        :return: status message.
        """
        try:
            data = self._req_to_json(request)
            rec = Demo(message=data['message'])
            rec.save()

            return Response({ 'status': 'Record had been created successfully!' })
        except:
            return Response({ 'status': 'Failed to create a record!' })    
    

    @action(methods=["get"], detail=False, url_path=r"fetch")
    def get(self, request: Request, *args, **kwargs):
        """
        Fetch all records.

        :param request:  The request object.
        :param args:
        :param kwargs: Url params,
        :return: First record object.
        """
        try:
            records = Demo.objects.all()

            if records is None or len(records) == 0:
                return HttpResponseNotFound('Record not found!')

            return self._model_to_json(records)
        except:
            return HttpResponseNotFound('Failed to fetch first record!') 
