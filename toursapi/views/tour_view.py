from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from toursapi.models import Tour, User, Category, TourCategory, State
from toursapi.views.user_view import UserSerializer
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
        try:
            user_id = request.query_params.get('userId', None)

            if user_id is not None:
                user = User.objects.get(id = user_id)
                tours = Tour.objects.filter(user_id=user)
            else:
                tours = Tour.objects.all()

            serializer = TourSerializer(tours, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #     """Handle GET requests to get all tours.
    #     Returns: Response -- JSON serialized list of tours"""
    #     try:
    #         tours = Tour.objects.all()
    #         serializer = TourSerializer(tours, many=True)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def list(self, request):
    #     tours =Tour.objects.all()

    #     user = request.query_parms.get('userId', None)
    #     tour = request.query_parms.get('tourId', None)

    #     if request.query_parms.get('completed', None) is not None and user is not None:
    #         tours = Tour.objects.filter(complete = 'True', user_id = user)
        
    #     serializer = TourSerializer(tours, many=True)
    #     return Response(serializer.data, status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized tour instance"""
        try:
            user = User.objects.get(id=request.data["user"])

            state = State.objects.get(id=request.data["state"])

            tour = Tour.objects.create(
                user=user,
                name=request.data["name"],
                description=request.data["description"],
                price=request.data["price"],
                address=request.data["address"],
                image=request.data["image"],
                state=state,
            )
            
            if request.data['tourCategories']:
                for category_id in request.data['tourCategories']:
                    new_category = Category.objects.get(id=category_id)
                    TourCategory.objects.create(tour=tour, category=new_category)
                
            serializer = TourSerializer(tour)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for an tour
        Returns: Response -- Empty body with 204 status code"""

        state = State.objects.get(id=request.data["state"])

        try:
            tour = Tour.objects.get(pk=pk)
            tour.name = request.data["name"]
            tour.description = request.data["description"]
            tour.price = request.data["price"]
            tour.address = request.data["address"]
            tour.image = request.data["image"]
            tour.state = state
            
            if request.data['tourCategories']:
                existing_tour_categories = TourCategory.objects.all().filter(tour=tour)
                for tour_category in existing_tour_categories:
                    tour_category.delete()
                for category_id in request.data['tourCategories']:
                    new_category = Category.objects.get(id=category_id)
                    TourCategory.objects.create(tour=tour, category=new_category)

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
            tour = Tour.objects.get(pk=pk)
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
            category = Category.objects.get(pk=category_id)
            tour = Tour.objects.get(pk=pk)
            existing_tour_categories = TourCategory.objects.all().filter(category=category, tour=tour)
            if len(existing_tour_categories) > 0:
                return Response({'message': 'Category already added to tour'}, status=status.HTTP_200_OK)
            else:
                TourCategory.objects.create(category=category, tour=tour)
                return Response({'message': 'Category added to tour'}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({'error': 'Tour not found.'}, status=status.HTTP_404_NOT_FOUND)
        except tour.DoesNotExist:
            return Response({'error': 'tour not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=True)
    def remove_tour_category(self, request, pk):
        """Delete request for a user to remove an item from an tour"""
        try:
            # tourcategory = tourItem.objects.get(pk=request.data.get("tour_item"), tour__pk=pk)
            tour = Tour.objects.get(pk=pk)
            
            category_id = request.query_params.get('categoryId', None)
            
            if category_id is not None:
                category = Category.objects.get(id=category_id)
                tour_category = TourCategory.objects.get(category=category, tour=tour)
                tour_category.delete()
                serializer = TourSerializer(tour)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        except TourCategory.DoesNotExist:
            return Response({'error': 'tour category not found.'}, status=status.HTTP_404_NOT_FOUND)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Category
        fields = ('id', 'name')
        depth = 1
class TourSerializer(serializers.ModelSerializer):
    """JSON serializer for tours"""
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Tour
        fields = ('id', 'categories', 'user', 'name', 'description', 'price', 'address', 'image', 'state')
        depth = 1
    
    def get_categories(self, obj):
        tour_categories = TourCategory.objects.all().filter(tour=obj)
        category_list = [tour_categories.category for tour_categories in tour_categories]
        serializer = CategorySerializer(category_list, many=True)
    
        if len(category_list) > 0:
            return serializer.data
        else:
            return []
        
