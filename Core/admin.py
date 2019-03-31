from django.contrib import admin
from .models import UserType, Profile, MemberGroup, Membership, State, City, Address, Society, Group, Doc, FloorEnum, FloorPlan, UnitPlan, Elevator, Building, Floor, Flat, FlatOwner, Lease, Parking, Vehicle, Complain, Meeting,  Notice, BillSetup, Maintenance


class CityModelInline(admin.TabularInline):
    model = City
    extra = 1

class StateModelAdmin(admin.ModelAdmin):
    field = ['name']
    inlines = [CityModelInline]

admin.site.register(State, StateModelAdmin)


admin.site.register(UserType)

admin.site.register(Profile)

admin.site.register(MemberGroup)

admin.site.register(Membership)

admin.site.register(Address)

admin.site.register(Society)

admin.site.register(Group)

admin.site.register(Doc)

admin.site.register(FloorEnum)

admin.site.register(FloorPlan)

admin.site.register(UnitPlan)

admin.site.register(Elevator)

admin.site.register(Building)

admin.site.register(Floor)

class FlatModelAdmin(admin.ModelAdmin):
    model = Flat
    readonly_fields = ('uniqId',)

admin.site.register(Flat, FlatModelAdmin)

admin.site.register(FlatOwner)

admin.site.register(Lease)

admin.site.register(Parking)

admin.site.register(Vehicle)

admin.site.register(Complain)

admin.site.register(Meeting)

admin.site.register(Notice)

admin.site.register(BillSetup)

admin.site.register(Maintenance)