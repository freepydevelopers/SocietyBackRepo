from django.contrib import admin
from .models import Profile, MemberGroup, Membership, State, City, Address, Society, Group, Doc, FloorEnum, FloorPlan, UnitPlan, Elevator, Building, Floor, Flat, FlatOwner, Lease, Parking, Vehicle, Complain, Meeting,  Notice, BillSetup, Maintenance

# class Meta:
#   abstract = True


# use search_fields = ['question_text']
# Change list pagination, search boxes, filters, date-hierarchies, and column-header-ordering

class CityModelInline(admin.TabularInline):
    model = City
    extra = 1
    readonly_fields = ('uniqId',)

class StateModelAdmin(admin.ModelAdmin):
    field = ['name']
    inlines = [CityModelInline]

admin.site.register(State, StateModelAdmin)

admin.site.register(Profile)

admin.site.register(MemberGroup)

admin.site.register(Membership)

class AddressModelAdmin(admin.ModelAdmin):
    model = Address
    readonly_fields = ('uniqId',)

admin.site.register(Address, AddressModelAdmin)

class SocietyModelAdmin(admin.ModelAdmin):
    model = Society
    readonly_fields = ('uniqId',)

admin.site.register(Society, SocietyModelAdmin)

admin.site.register(Group)

admin.site.register(Doc)

admin.site.register(FloorEnum)

admin.site.register(FloorPlan)

admin.site.register(UnitPlan)

class ElevatorModelAdmin(admin.ModelAdmin):
    model = Elevator
    readonly_fields = ('uniqId',)

admin.site.register(Elevator, ElevatorModelAdmin)

class BuildingModelAdmin(admin.ModelAdmin):
    model = Building
    readonly_fields = ('uniqId',)

admin.site.register(Building, BuildingModelAdmin)

admin.site.register(Floor)

class FlatModelAdmin(admin.ModelAdmin):
    model = Flat
    readonly_fields = ('uniqId',)

admin.site.register(Flat, FlatModelAdmin)

admin.site.register(FlatOwner)

admin.site.register(Lease)

class ParkingModelAdmin(admin.ModelAdmin):
    model = Parking
    readonly_fields = ('uniqId',)

admin.site.register(Parking, ParkingModelAdmin)

class VehicleModelAdmin(admin.ModelAdmin):
    model = Vehicle
    readonly_fields = ('uniqId',)

admin.site.register(Vehicle, VehicleModelAdmin)

class ComplainModelAdmin(admin.ModelAdmin):
    model = Complain
    readonly_fields = ('uniqId',)

admin.site.register(Complain, ComplainModelAdmin)

class MeetingModelAdmin(admin.ModelAdmin):
    model = Meeting
    readonly_fields = ('uniqId',)

admin.site.register(Meeting, MeetingModelAdmin)

class NoticeModelAdmin(admin.ModelAdmin):
    model = Notice
    readonly_fields = ('uniqId',)

admin.site.register(Notice, NoticeModelAdmin)

admin.site.register(BillSetup)

admin.site.register(Maintenance)