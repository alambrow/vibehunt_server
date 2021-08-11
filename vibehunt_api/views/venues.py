from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vibehunt_api.models import Venue

class VenueView(ViewSet):

    def list(self, request):
        neighborhood = self.request.query_params.get('neighborhood', None)

        if neighborhood:
            venues = Venue.objects.filter(neighborhood=neighborhood)
        else:
            venues = Venue.objects.all()

        serializer = VenueSerializer(
            venues, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            venue = Venue.objects.get(pk=pk)
            serializer = VenueSerializer(venue, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ('id', 'venId', 'name', 'address', 'neighborhood', 'lat', 'long')
        depth = 1