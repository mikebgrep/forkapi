from datetime import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from forkapi.authentication.HeaderAuthentication import HeaderAuthentication
from forkapi.generics import ListCreateDestroyViewSet
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleView(ListCreateDestroyViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def get_authenticators(self):
        """
        Instantiates and returns the list of authentication_classes that this view requires.
        """
        if self.request.method == 'GET':
            authentication_classes = [HeaderAuthentication]
        else:
            authentication_classes = [TokenAuthentication]

        return [auth() for auth in authentication_classes]

    def list(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        try:
            valid_date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = Schedule.objects.filter(date=valid_date)
            serializer = ScheduleSerializer(queryset, many=True, context={"request": request})
            return Response(serializer.data)

        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=HTTP_400_BAD_REQUEST)
