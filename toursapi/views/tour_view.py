from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from toursapi.models import Tour, User, Category, TourCategory
# from tourspapi.views.tour_category_view import TourCategorySerializer


class TourView(ViewSet):
    """tour view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tour.
        Returns: Response -- JSON serialized tour"""

        try:
            tour = Tour.objects.get(pk=pk)
            serializer = TourSerializer(tour)
            return Response(serializer.data)
        except Tour.DoesNotExist:
            return Response({'message': 'tour not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all tours.
        Returns: Response -- JSON serialized list of tours"""
        try:
            tours = Tour.objects.all()
            serializer = TourSerializer(tours, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized tour instance"""
        try:
            user = User.objects.get(id=request.data["user"])

            tour = Tour.objects.create(
                user=user,
                name=request.data["name"],
                description=request.data["description"],
                price=request.data["price"],
                address=request.data["address"],
                image=request.data["image"],
                state=request.data["state"],
            )
            serializer = TourSerializer(tour)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for an tour
        Returns: Response -- Empty body with 204 status code"""

        try:
            tour = Tour.objects.get(pk=pk)
            tour.name = request.data["name"]
            tour.description = request.data["description"]
            tour.price = request.data["price"]
            tour.address = request.data["address"]
            tour.image = request.data["image"]
            tour.state = request.data["state"]

            tour.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except tour.DoesNotExist:
            return Response({'message': 'tour not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for an tour
        Returns: Response -- Empty body with 204 status code"""

        try:
            tour = tour.objects.get(pk=pk)
            tour.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except tour.DoesNotExist:
            return Response({'message': 'tour not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # Add & Remove tour category

    @action(methods=['post'], detail=True)
    def add_tour_category(self, request, pk, category_id=None):
        """Post request for a user to add an item to an tour"""
        try:
            # item = Item.objects.get(pk=request.data["item"])
            tourcategory = TourCategory.objects.get(pk=category_id)
            tour = Tour.objects.get(pk=pk)

            tourcategory = TourCategory.objects.create(category=tourcategory, tour=tour)
            return Response({'message': 'Category added to tour'}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
        except tour.DoesNotExist:
            return Response({'error': 'tour not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['delete'], detail=True)
    def remove_tour_category(self, request, pk, tour_category=None):
        """Delete request for a user to remove an item from an tour"""
        try:
            # tourcategory = tourItem.objects.get(pk=request.data.get("tour_item"), tour__pk=pk)
            tour_category_id = self.kwargs.get('tour_category')
            tourcategory = TourCategory.objects.get(pk=tour_category_id)

            tourcategory.delete()
            return Response("tour item removed", status=status.HTTP_204_NO_CONTENT)
        except TourCategory.DoesNotExist:
            return Response({'error': 'tour category not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # @action(methods=['delete'], detail=True)
    # def remove_tour_item(self, request, pk):
    #     """Delete request for a user to remove an item from an tour"""

    #     touritem = request.data.get("tour_item")
    #     tourItem.objects.filter(pk=touritem, tour__pk=pk).delete()

    #     return Response("tour item removed", status=status.HTTP_204_NO_CONTENT)


class TourCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TourCategory
        fields = ('id', 'name')
        depth = 1
class TourSerializer(serializers.ModelSerializer):
    """JSON serializer for tours"""
    categories = TourCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Tour
        fields = ('id', 'categories', 'user', 'name', 'description', 'price', 'address', 'image', 'state')
        depth = 1
