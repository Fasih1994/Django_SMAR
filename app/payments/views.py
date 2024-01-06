from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from payments.serializer import SelectPackageSerializer
from django.conf import settings
import stripe

from core.models import Payment, Package
from core.permissions import IsAdminUser


class CreatePayment(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = SelectPackageSerializer

    def post(self, request):
        payment = self.get_serializer(data=request.data)
        if not payment.is_valid():
            return Response(
                {'message': payment.errors},
                status=status.HTTP_400_BAD_REQUEST
                )
        payment = payment.data
        package = Package.objects.get(name=payment["package_name"])
        user = self.request.user
        data = request.data
        stripe.api_key = settings.STRIPE_SECRET_KEY

        payment_method_id = data['payment_method_id']
        customer_data = stripe.Customer.list(email=user.email).data

        # if the array is empty it means the email has not been used yet
        if len(customer_data) == 0:
            # creating customer
            customer = stripe.Customer.create(
                name=user.name,
                email=user.email,
                payment_method=payment_method_id
                )
        else:
            customer = customer_data[0]

        try:
            payment_intent = stripe.PaymentIntent.create(
                customer=customer,
                payment_method=payment_method_id,
                currency='usd',  # you can provide any currency you want
                amount=int(package.price*100),
                confirm=True,
                return_url="http://localhost:9001/",
                receipt_email=user.email
                )
            previous_payments = Payment.objects.filter(
                organization=user.organization
                )
            for p_payment in previous_payments:
                p_payment.is_active = False
                p_payment.save()

            payment = Payment(
                payment_intent_id=payment_intent.id,
                organization=user.organization,
                succeeded=payment_intent.status == 'succeeded',
                is_active=True,
                created_by=user.id,
                last_updated_by=user.id,
                last_update_login=user.id
            )
            payment.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    'message': 'Success',
                    'data': {'customer_id': customer.email},
                    'payment': {
                        'id': payment.id,
                        'organization': user.organization.name
                    }
                }
            )
        except stripe.error.CardError as e:
            print(e)
            return Response(
                {'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )
