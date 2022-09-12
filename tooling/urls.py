from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    # path('privacy', privacy, name='privacy'),

    # path('page401', page401, name='page401'),

]


# 401 Unauthorized
# 403 Forbidden
# 404 Not Found
# 415 Unsupported Media Type
# 500 Internal Server Error
# 501 Not Implemented
# 502 Bad Gateway

