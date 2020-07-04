# https://www.societyhive.com/Housing-society-accounting-software-and-apartment-mobile-App-Features
# https://www.youtube.com/watch?v=lyqha_20OH8

# http://dhakadailybazar.com/apartment-management-system/setting/member_type_setup.php
# https://docs.oracle.com/cd/E59116_01/doc.94/e58792/toc.htm
# https://my.vertabelo.com/model/94XnxU79GMGhAWwyEOMdazJDwgCXmGtH
# https://www.youtube.com/watch?v=LEXbgq9AUfQ - video
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Main roles in system
class UserType(models.Model):
    ADMIN = 'adm'
    OWNER = 'own'
    TENANT = 'ten'
    EMPLOYEE = 'emp'
    USERTYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (OWNER, 'Owner'),
        (TENANT, 'Tenant'),
        (EMPLOYEE, 'Employee')
    )
    status = models.CharField(max_length=3, choices=USERTYPE_CHOICES, default=OWNER)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True)
    TITLE_CHOICES = (
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('ms', 'Ms'),
    )
    title = models.CharField(max_length=3, choices=TITLE_CHOICES, blank=True)
    educationtitle = models.CharField(max_length=50, blank=True)
    organization = models.CharField(max_length=50, blank=True)
    permanentaddress = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=12, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        db_table = 'profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class MemberGroup(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Profile, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(MemberGroup, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'state'
        verbose_name_plural = 'states'
        db_table = 'state'

    def __str__(self):
        return self.name


class City(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    # owner = models.ForeignKey('auth.User', related_name='prelimcity', on_delete=models.CASCADE)3
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_city', on_delete=models.CASCADE)
    # models.CharField(max_length=100,null=True)
    updatedby = models.ForeignKey('auth.User', related_name='u_city', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        db_table = 'city'

    def __str__(self):
        return self.name + ", " + self.state.name


class Address(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    addr1 = models.CharField(max_length=100)
    addr2 = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_address', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_address', on_delete=models.CASCADE)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return self.addr1 + " " + self.addr2


class Society(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    # uniqId = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    shortname = models.CharField(max_length=10)
    registrationnumber = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    establishedon = models.DateTimeField(null=True)
    developer = models.CharField(max_length=100)
    imagepath = models.CharField(max_length=100)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_society', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_society', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'society'
        verbose_name_plural = 'societies'
        db_table = 'society'

    def __str__(self):
        return self.name


# enum - to create group of any
class Group(models.Model):
    name = models.CharField(max_length=128)  # floorplan, etc
    description = models.TextField(null=True)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)

    # group = models.ForeignKey(Group, on_delete=models.CASCADE) - self join TBD
    class Meta:
        db_table = 'group'

    def __str__(self):
        return self.name


# all documents with details
# vehicle docs, meeting docs, events docs, festival docs, society docs {society master plan, floor plan, parking plan, garden plan}, billing docs, account docs, 
class Doc(models.Model):
    name = models.CharField(max_length=128)
    extension = models.CharField(max_length=10)  # jpg, doc, etc
    description = models.TextField(null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'doc'
        verbose_name_plural = 'docs'
        db_table = 'doc'

    def __str__(self):
        return self.name


# enum - First 1, Second 2 - global for all societies
class FloorEnum(models.Model):
    name = models.CharField(max_length=25)
    floornumber = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'floordetail'
        verbose_name_plural = 'floordetails'
        db_table = 'floordetail'

# define floor plan under society e.g. Odd, Even, Refuse floor
class FloorPlan(models.Model):
    name = models.CharField(max_length=25)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    imagepath = models.ForeignKey(Doc, on_delete=models.CASCADE)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_floorplan', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_floorplan', on_delete=models.CASCADE)

    class Meta:
        db_table = 'floorplan'

    def __str__(self):
        return self.name


# define unit plan under society e.g. every unique type of flat in society plan
class UnitPlan(models.Model):
    name = models.CharField(max_length=25)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    imagepath = models.ForeignKey(Doc, on_delete=models.CASCADE)
    floorplan = models.ForeignKey(FloorPlan, on_delete=models.CASCADE)
    description = models.TextField(null=True)  # flat facing, etc. any oral description related to flat goes here
    maintenancearea = models.IntegerField()
    carpetarea = models.IntegerField()

    ONERK = '01r'
    ONEBHK = '01b'
    ONEHALFBHK = '15b'
    TWOBHK = '02b'
    TWOHALFBHK = '25b'
    THREEBHK = '03b'
    FOURBHK = '04b'
    PENT = 'pen'
    UNIT_CHOICES = (
        (ONERK, '1 Room Kitchen'),
        (ONEBHK, '1 BHK'),
        (ONEHALFBHK, '1.5 BHK'),
        (TWOBHK, '2 BHK'),
        (TWOHALFBHK, '2.5 BHK'),
        (THREEBHK, '3 BHK'),
        (FOURBHK, '4 BHK'),
        (PENT, 'Penthouse'),
    )
    unittype = models.CharField(max_length=3, choices=UNIT_CHOICES, default=ONEBHK)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_unitplan', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_unitplan', on_delete=models.CASCADE)

    class Meta:
        db_table = 'unitplan'

    def __str__(self):
        return self.name


class CCTV(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)  # make, model, etc
    status = models.CharField(max_length=30, null=False, default='running')
    building = models.ForeignKey('Building', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cctv'

    def __str__(self):
        return self.name


class Elevator(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)  # make, model, etc
    status = models.CharField(max_length=30, null=False, default='running')
    building = models.ForeignKey('Building', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'elevator'

    def __str__(self):
        return self.name

class Building(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    '''
    RESIDENT = 'RES'
    CLUBHOUSE = 'CLU'
    ROWHOUSE = 'ROW'
    BUILDING_CHOICES = (
        (RESIDENT, 'Residential'),
        (CLUBHOUSE, 'Club house'),
        (ROWHOUSE, 'Row house'),
    )
    buildingtype = models.CharField(max_length=3, choices=BUILDING_CHOICES, default=RESIDENT)
    '''
    # elevators =  models.ForeignKey(Elevator, on_delete=models.CASCADE)
    # floors = models.ManyToManyField('Floor')
    description = models.TextField(null=True)
    PROPOSED = 'PRO'
    COMPLETE = 'COM'
    UNDERCONSTRUCTION = 'UCO'
    DESTROYED = 'DES'
    CONSTRUCTIONSTATUS_CHOICES = (
        (PROPOSED, 'Proposed'),
        (COMPLETE, 'Complete'),
        (UNDERCONSTRUCTION, 'Under Construction'),
        (DESTROYED, 'Destroyed'),
    )
    constructionstatus = models.CharField(max_length=3, choices=CONSTRUCTIONSTATUS_CHOICES, default=COMPLETE)
    constructionstatusyear = models.IntegerField()
    # imagepath = models.ImageField(upload_to="gallery")
    imagepath = models.CharField(max_length=100)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_building', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_building', on_delete=models.CASCADE)

    class Meta:
        db_table = 'building'

    def __str__(self):
        return self.name


# building object is ready then assign floors
class Floor(models.Model):
    floordetail = models.ForeignKey(FloorEnum, on_delete=models.CASCADE)
    floorplan = models.ForeignKey(FloorPlan, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_floor', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_floor', on_delete=models.CASCADE)

    class Meta:
        db_table = 'floor'

    def __str__(self):
        return self.floordetail.name + " (" + self.building.society.shortname + ")"


class Flat(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=25)
    flatnumber = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    unitplan = models.ForeignKey(UnitPlan, on_delete=models.CASCADE)
    extensionnumber = models.CharField(max_length=10)
    description = models.TextField(null=True)
    possesion = models.DateField(null=True)
    ISEMPTY = 'empt'
    ISOWNER = 'iso'
    ISTENANT = 'ist'
    LIVINGSTATUS_CHOICES = (
        (ISEMPTY, 'Empty'),  # nobody living
        (ISOWNER, 'Is Owner'),  # owner living
        (ISTENANT, 'Is Tenant'),  # tenant living
    )
    status = models.CharField(max_length=3, choices=LIVINGSTATUS_CHOICES, default=ISOWNER)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_flat', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_flat', on_delete=models.CASCADE)

    class Meta:
        db_table = 'flat'


    def __str__(self):
        return self.name


class FlatOwner(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    ACTIVE = 'act'
    INACTIVE = 'ina'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),  # current owner of flat
        (INACTIVE, 'Inactive'),  # no longer owner of flat
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=ACTIVE)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_flatowner', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_flatowner', on_delete=models.CASCADE)

    class Meta:
        db_table = 'flatowner'

    def __str__(self):
        return self.name


class Lease(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    months = models.IntegerField()  # agreement in months
    rentpermonth = models.IntegerField()
    deposit = models.IntegerField()
    frommonth = models.IntegerField()
    fromyear = models.IntegerField()
    ACTIVE = 'act'
    INACTIVE = 'ina'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=ACTIVE)  # only one active record per flat

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_lease', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_lease', on_delete=models.CASCADE)

    class Meta:
        db_table = 'lease'

    def __str__(self):
        return self.name


class Parking(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    lotnumber = models.CharField(max_length=10)
    description = models.TextField(null=True)
    assignedto = models.ForeignKey(Flat, on_delete=models.CASCADE)  # parking assigned to flat number

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_parking', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_parking', on_delete=models.CASCADE)

    class Meta:
        db_table = 'parking'

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    number = models.CharField(max_length=15)
    parkedat = models.ForeignKey(Parking, on_delete=models.CASCADE)

    TWO = 'TWO'
    THREE = 'THR'
    FOUR = 'FOU'
    VEHICLE_CHOICES = (
        (TWO, 'Two Wheeler'),
        (THREE, 'Three Wheeler'),
        (FOUR, 'Four Wheeler'),
    )
    vehicletype = models.CharField(max_length=3, choices=VEHICLE_CHOICES, default=FOUR)
    description = models.TextField(null=True)

    NEW = 'NEW'
    APPROVED = 'APR'
    ISSUED = 'ISD'
    REJECTED = 'REJ'
    STICKER_CHOICES = (
        (NEW, 'New'),  # by user for new entry.
        (APPROVED, 'Approved'),  # by approver once docs are correct.
        (ISSUED, 'Issued'),  # by approver once sticker issued. End
        (REJECTED, 'Rejected')  # approver will enter the reason also.
    )
    status = models.CharField(max_length=3, choices=STICKER_CHOICES, default=NEW)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_vehicle', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_vehicle', on_delete=models.CASCADE)

    class Meta:
        db_table = 'vehicle'

    def __str__(self):
        return self.name


# +++++++++++++++++++++++++++++++++++++++++++++

class Complain(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=25)
    description = models.TextField(null=True)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_complain', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_complain', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=25)
    description = models.TextField(null=True)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_meeting', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_meeting', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Notice(models.Model):
    uniqId = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=25)
    description = models.TextField(null=True)
    noticedate = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, null=False, default='active')  # active, inactive

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_notice', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_notice', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BillSetup(models.Model):
    name = models.CharField(max_length=25)  # eg. 1. menenance per sqft 1.7/month 2. ganesh vargani / headcount
    amount = models.IntegerField()

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_billsetup', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_billsetup', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Maintenance(models.Model):
    amount = models.IntegerField()  # readonly #user flat carpet area * billsetup(mentain row)
    durationinmonths = models.IntegerField()
    frommonth = models.DateTimeField(null=True)

    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey('auth.User', related_name='c_maintenance', on_delete=models.CASCADE)
    updatedby = models.ForeignKey('auth.User', related_name='u_maintenance', on_delete=models.CASCADE)

    def __str__(self):
        return self.name