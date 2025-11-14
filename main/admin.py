from django.contrib import admin
from .models import User, Thesis, Feedback

admin.site.register(User)
admin.site.register(Thesis)
admin.site.register(Feedback)
