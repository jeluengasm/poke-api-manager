from rest_framework import routers

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'
