from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from vibehunt_api.models import Comment, Venue
import time

class CommentView(ViewSet):

    def list(self, request):
        venue = self.request.query_params.get('venueId', None)

        if venue:
            comments = Comment.objects.filter(venueId=venue)
        else:
            comments = Comment.objects.all()
        
        time_window = time.time() - 7200
        filteredComments = []
        for comment in comments:
            if comment.timestamp >= time_window:
                filteredComments.append(comment)

        serializer = CommentSerializer(
            filteredComments, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def create(self, request):
        comment = Comment()
        comment.commentId = request.data["commentId"]
        comment.timestamp = request.data["timestamp"]
        comment.venueId = Venue.objects.get(pk=request.data["venueId"])

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('commentId', 'timestamp', 'venueId')
        depth = 1