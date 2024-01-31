from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from toursapi.models import State


class StateView(ViewSet):
    """state view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single state.
        Returns: Response -- JSON serialized state"""

        try:
            item = State.objects.get(pk=pk)
            serializer = StateSerializer(item)
            return Response(serializer.data)
        except State.DoesNotExist:
            return Response({'message': 'State not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all items.
        Returns: Response -- JSON serialized list of items"""

        try:
            states = State.objects.all()
            serializer = StateSerializer(states, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StateSerializer(serializers.ModelSerializer):
    """JSON serializer for states"""
    class Meta:
        model = State
        fields = ('id', 'name')
        depth = 1
