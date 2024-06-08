# Create your models here.
from django.core.mail import send_mail
import enum
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# Create your models here.


class Country(models.Model):
    class Meta:
        db_table = 'Country'
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'

class City(models.Model):
    class Meta:
        db_table = 'City'
    name = models.CharField(max_length=40)
    #country_id
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)   

    def __str__(self) -> str:
        return f'{self.name}'

class Agency(models.Model):
    class Meta:
        db_table = 'Agency'
    fullName = models.CharField(max_length=100, null=True, blank=True)
    arFullName = models.CharField(max_length=100, null=True, blank=True)
    shortName = models.CharField(max_length=50, null=True, blank=True)
    licenseCode = models.CharField(max_length=5, null=True, blank=True)
    # TODO ELISSA 3-19-2024
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=True)
    logo = models.CharField(null=True ,max_length=255, blank=True)
    address = models.CharField(null=True, max_length=255, blank=True)
    # TODO ELISSA 3-19-2024
    image = models.ImageField(upload_to='uploads/agencies/', null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.fullName}'


class UserType(models.Model):
    class Meta:
        db_table = 'UserType'
    userTypeDesc = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f'{self.userTypeDesc}'

class Specialization(models.Model):
    class Meta:
        db_table = 'Specialization'
    specializationDesc = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.specializationDesc}'


class User(AbstractUser):
    class Meta:
        db_table = 'User'

    birthdate = models.DateField(null=True, blank=True)
    middleName = models.CharField(max_length=30, blank=True)
    brokerCode = models.CharField(max_length=5, null=True, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True)
    phoneNumberCode = models.CharField(max_length=100, null=True, blank=True)
    phoneNumber = models.CharField(max_length=30, default= None, null=True, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    profilePicture = models.CharField(max_length=255, null=True, blank=True)
    profileImage = models.ImageField(default='Logo.jpg', upload_to='uploads/users/', null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            old_profile_picture = User.objects.get(pk=self.pk).profileImage
            if old_profile_picture and self.profileImage and old_profile_picture != self.profileImage:
                old_profile_picture.delete(save=False)
        except:
            pass    
        super().save(*args, **kwargs)


class PropertyType(models.Model):
    class Meta:
        db_table = 'PropertyType'
    propertyTypeDesc = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.propertyTypeDesc}'
    
class PropertyStatus(models.Model):
    class Meta:
        db_table = 'PropertyStatus'
    propertyStatusDesc = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.propertyStatusDesc}'


class Property(models.Model):
    class Meta:
        db_table='Property'
    propertyName = models.CharField(max_length=50)
    propertyLandArea = models.DecimalField( max_digits=15, decimal_places=2 ,max_length=20)
    numOfBedrooms = models.IntegerField(default=0)
    numOfBathrooms=models.IntegerField(default=0)
    numOfParkingLots = models.IntegerField(default=0)
    numOfGarages = models.IntegerField(default=0)
    propertyDescription=models.CharField(max_length=200)
    #propertyid
    propertyType = models.ForeignKey(PropertyType,on_delete=models.CASCADE,null=False)
    #propertyStatus
    propertyStatus = models.ForeignKey(PropertyStatus,on_delete=models.CASCADE,null=False)
    #userId
    user  = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    #cityId
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=False)
    # TODO ELISSA
    deleted = models.BooleanField(default=False)

    # Price fields
    salePrice = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    rentPrice = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    saved = models.ManyToManyField(User,blank=True,null=True,related_name="saved")
    # Price Id for Stripe
    price_id = models.CharField(default=0, max_length=100)



    def __str__(self) -> str:
        return f'{self.propertyName}'


# TODO CHARBEL 3-APRIL-2024
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/properties/', null=True, blank=True)
    
class Contract(models.Model):
    class meta:
        db_table='Contract'

    issueDate = models.DateField(null=False)
    startDate = models.DateField(null=False)
    endDate = models.DateField(null=False)
    expiryDate = models.DateField(null=False, default=timezone.now())
    #TODO CHARBEL
    depositAmount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    numOfInvoices = models.IntegerField(default=0)
    #sellerid
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='seller_contracts')
    #buyerid
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='buyer_contracts')
    #propertyid
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=False, related_name='property_contracts')
    #contractParentID
    contractParent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_contracts')

    def is_active(self):
        """
        Check if the contract is currently active based on its start and end dates.
        """
        today = timezone.now().date()
        return self.expiryDate < today

    def send_notification(self, message):
        """
        Send a notification to the parties involved.
        """
        # Placeholder implementation for sending notification
        send_mail(
                subject=self.__str__(),
                message=message,
                recipient_list=[self.buyer.email],
                from_email=settings.EMAIL_HOST_USER)

    def check_expiry_and_notify(self):
        """
        Check if the contract is about to expire and send a notification if needed.
        """
        days_to_expiry = (self.expiryDate - timezone.now().date()).days
        if days_to_expiry <= 7:  # Notify 7 days before expiry
            message = f"Contract {self.id} is expiring in {days_to_expiry} days. Please take necessary actions."
            self.send_notification(message)

    def __str__(self):
        return f"Contract #{self.pk}: Seller - {self.seller.username}, Buyer - {self.buyer.username}, Property - {self.property}"

class TransactionType(models.Model):
    class Meta:
        db_table='TransactionType'
    transactionTypeDesc = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.transactionTypeDesc}'

class TransactionStatus(models.Model):
    class Meta:
        db_table='TransactionStatus'
    transactionStatusDesc = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.transactionStatusDesc}'

class Transaction(models.Model):
    class Meta:
        db_table='Transaction'

    transactionDate=models.DateField(null=False)
    broker = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    #transactionType
    transactionType = models.ForeignKey(TransactionType, on_delete=models.CASCADE, null = False)
    #transactionStatus
    transactionStatus = models.ForeignKey(TransactionStatus, on_delete = models.CASCADE, null = False)
    #contractId
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)


class PaymentType(models.Model):
    class Meta:
        db_table='PaymentType'
    paymentTypeDesc = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.paymentTypeDesc}'

class Payment(models.Model):
    class Meta:
        db_table='Payment'

    paymentAmount=models.DecimalField(max_digits=15, decimal_places=2, null=False) 
    paymentDate=models.DateField(null=False, default=timezone.now())
    #paymentId
    paymentType = models.ForeignKey(PaymentType, on_delete= models.CASCADE, null = False)
    contract = models.ForeignKey(Contract, on_delete= models.CASCADE, null = True)

class RequestStatus(models.Model):
    class Meta:
        db_table = 'RequestStatus'
    reqStts = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.reqStts}'

class RequestType(models.Model):
    class Meta:
        db_table = 'RequestType'
    reqType = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.reqType}'

class Request(models.Model):
    class Meta:
        db_table = 'Request'
    seller = models.ForeignKey(User,on_delete=models.CASCADE,null=False, related_name='seller_req')
    broker = models.ForeignKey(User,on_delete=models.CASCADE,null=False, related_name='broker_req')
    issuedOn = models.DateTimeField(default=timezone.now())
    reqStatus = models.ForeignKey(RequestStatus, on_delete=models.CASCADE, null = False)
    reqType = models.ForeignKey(RequestType, on_delete=models.CASCADE, null = False)


# TODO PATRICK 3-19-2024
class Company(models.Model):
    class Meta:
        db_table = 'Company'
    name = models.CharField(max_length=100, null=True, blank=True)   
    website = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phoneNumber = models.CharField(max_length=10, null=True, blank=True)
    city = models.ForeignKey(City,on_delete=models.SET_NULL, null=True, blank=True)   
    logo = models.CharField(null=True ,max_length=255,blank=True)
    address = models.CharField(null=True, max_length=255, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

class CompanyMessages(models.Model):
    class Meta:
        db_table = 'CompanyMessages'
    senderName = models.CharField(max_length=100, null=True, blank=True)
    senderEmail = models.CharField(max_length=100, null=True, blank=True)   
    messageSubject = models.CharField(max_length=100, null=True, blank=True) 
    message = models.TextField(max_length=1000, null=True, blank=True)
# TODO PATRICK 3-19-2024


#TODO PATRICK 3-20-2024
# class PropertyPhoto(models.Model):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to='property_photos/')


# To generate automatically new token for each user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Property_Status(enum.Enum):
    Active = 1
    Under_Contract = 2
    Pending = 3
    Sold = 4
    Leased_Rented = 5
    Vacant = 6
    Off_Market = 7
    Foreclosure = 8
    Bank_Owned_REO = 9
    Short_Sale = 10
    Probate = 11
    Development = 12
    For_Rent = 13
    For_Sale = 14