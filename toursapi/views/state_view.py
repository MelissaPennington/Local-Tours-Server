from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from toursapi.models import State


class StateView(ViewSet):
    """item view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single item.
        Returns: Response -- JSON serialized item"""

        try:
            item = State.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except State.DoesNotExist:
            return Response({'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all items.
        Returns: Response -- JSON serialized list of items"""

        try:
            state = State.objects.all()
            serializer = StateSerializer(states, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemSerializer(serializers.ModelSerializer):
    """JSON serializer for items"""
    class Meta:
        model = State
        fields = ('id', 'name')
        depth = 1
