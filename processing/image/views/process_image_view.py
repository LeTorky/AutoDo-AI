from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from image.serializers.image_serializer import ImageSerializer
from rest_framework.permissions import IsAuthenticated
from image.utils.extract_text_from_image import extract_text_from_image
from image.utils.convert_text_to_list import convert_text_to_list
import requests


class GetListFromImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Get list from image."""
        # Need to extract domain from request headers. IE need to add it to core server request.
        domain = 'http://localhost:5057'

        serializer = ImageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data['image']

        try:
            extracted_text = extract_text_from_image(image)
            extracted_list = convert_text_to_list(extracted_text)
            json_content = extracted_list['list']
            self._populate_caller_with_list(json_content, domain, request.auth)
            return Response(True)
        except (ValueError, TypeError, KeyError) as e:
            print(e)
            return Response(f'{e}',
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _populate_caller_with_list(self, list_array, domain, token):
        """Populates the caller with the array list generated."""
        url = domain+'/Task/Multiple'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'AccessToken {token}',
        }
        requests.post(url, json=list_array, headers=headers)
