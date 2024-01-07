from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from image.serializers.image_serializer import ImageSerializer
from rest_framework.permissions import IsAuthenticated
from image.utils.extract_text_from_image import extract_text_from_image
from image.utils.convert_text_to_list import convert_text_to_list


class GetListFromImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Get list from image."""

        serializer = ImageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data['image']

        try:
            extracted_text = extract_text_from_image(image)
            extracted_list = convert_text_to_list(extracted_text)
            return Response(extracted_list)
        except (ValueError, TypeError) as e:
            return Response(f'{e}',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
