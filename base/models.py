import secrets
from django.db import models
from .stacks import Paystack


# Create your models here.
class Payments(models.Model):

    amount = models.PositiveIntegerField()

    #reference will be attached to payments so can be verified
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ('-date_created',)

    def __str__(self):
        return f'Payment: {self.amount}'
    
    #overriding the database save method
    def save(self, *args, **kwargs) -> None:
        #if payment has no reference
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            #confirm if they exist a similar referenc in the payment database
            object_with_similar_reference = Payments.objects.filter(ref = ref)
            #if query set does not exist
            if not object_with_similar_reference:
                self.ref = ref

        super().save(*args, *kwargs)

    def amount_value(self) -> int:
        return self.amount * 100
    

    def verify_pay(self):

        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:

            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()

        if self.verified:
            return True
        
        return False




