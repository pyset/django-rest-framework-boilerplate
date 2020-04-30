"""Demo API."""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from apps.restapis.models.demo import Demo
from rest_framework.decorators import action


class DemoAPI(viewsets.GenericViewSet):
    @action(methods=["post"], detail=False)
    def post(self, request: Request, *args, **kwargs):
        """
        Create new record.

        :param request:  The request object.
        :param args:
        :param kwargs: Url params,
        :return: status message.
        """
        try:
            data = request
            rec = Demo(message=data['message'])
            rec.save()

            return Response({ 'status': 'Record had been created successfully!' })
        except:
            return Response({ 'status': 'Failed to create a record!' })    
