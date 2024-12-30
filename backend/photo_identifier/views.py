from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FoodPrediction, FoodCategory
from photo_handler.models import Photo
from .ml import run_food_model

class PredictFoodView(APIView):
    def post(self, request, photo_id):
        try:
            # Retrieve the photo
            photo = Photo.objects.get(id=photo_id)

            # Run the ML model on the photo
            result = run_food_model(photo.filename)

            # Get or create the food category
            category, _ = FoodCategory.objects.get_or_create(name=result['category'])

            # Save the prediction
            prediction = FoodPrediction.objects.create(
                photo=photo,
                category=category,
                confidence=result['confidence']
            )

            # Return the prediction data
            return Response({
                'photo_id': photo.id,
                'category': prediction.category.name,
                'confidence': prediction.confidence
            }, status=status.HTTP_201_CREATED)
        except Photo.DoesNotExist:
            return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)
