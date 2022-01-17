from django.core.exceptions import ValidationError as retryExceeded
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from customer.otp_backend import OTPBackend
from customer.models import Customer
from customer.serializers import CustomerSerializer

user = get_user_model()


class CustomerViewSet(ViewSet):
    serializer_class = CustomerSerializer

    @action(methods=['post'], detail=False)
    def get_otp(self, request):
        phone = request.data.get('phone')
        test = request.data.get('test')
        if not phone:
            raise ValidationError(detail={'message': 'phone required'})
        otp_obj = OTPBackend(phone)
        try:
            otp_obj.send_otp(test)
        except retryExceeded as e:
            return Response({'message': e}, status=HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'success'})

    @action(methods=['post'], detail=False)
    def login(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        if not phone or not otp:
            raise ValidationError(detail={'message': 'phone and otp required'})
        otp_obj = OTPBackend(phone)
        try:
            valiation_status = otp_obj.validate_otp(otp)
        except retryExceeded as e:
            return Response({'message': e}, status=HTTP_406_NOT_ACCEPTABLE)
        if valiation_status:
            # login success get authentication token for the customer
            user_obj, status = user.objects.get_or_create(username=phone)
            customer, status = Customer.objects.get_or_create(user=user_obj)
            tokens = get_tokens_for_user(user_obj)
            return Response(tokens)
        raise ValidationError(detail={'message': 'mismatch'})

    @action(methods=['post'], detail=False)
    def update_info(self, request):
        if not request.user.is_authenticated:
            raise ValidationError(detail={'message': 'customer not found'})
        customer = Customer.objects.filter(user=request.user)
        if not customer:
            raise ValidationError(detail={'message': 'customer not found'})
        customer.update(**request.data)
        return Response(data=self.serializer_class(customer[0]).data)

    @action(methods=['post'], detail=False)
    def get_token(self, request):
        unique_id = request.data.get('customer_id')
        if not unique_id:
            raise ValidationError(detail={'message': 'id required'})
        user_obj, status = user.objects.get_or_create(username=unique_id)
        customer, status = Customer.objects.get_or_create(user=user_obj)
        tokens = get_tokens_for_user(user_obj)
        return Response(tokens)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
