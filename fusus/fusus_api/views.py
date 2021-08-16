from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

class Test(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Initial test.
        """
        return Response("Test good.", status=status.HTTP_200_OK)

