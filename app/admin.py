from django.contrib import admin
from .models import Doctor , BloodDonation , DoctorInfo , DoctorInfoExtend
# Register your models here.


admin.site.register( Doctor )

admin.site.register( BloodDonation )




admin.site.register( DoctorInfo )

admin.site.register( DoctorInfoExtend )