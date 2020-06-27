# ITEMS BETWEEN THESE HEADINGS WILL BE UPDATED
# ------------------------ UWEB URLS ------------------------------------
# add our different urls for the cms to work
from django.conf.urls import include

urlpatterns += [
    path('_cms/', include('uweb.urls')),
]
# ------------------------ UWEB URLS ------------------------------------
