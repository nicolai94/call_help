from django.urls import path, include
from rest_framework.routers import DefaultRouter
from breaks.views import dicts, replacements

router = DefaultRouter()

router.register(r'replacements', viewset=replacements.ReplacementView, basename='replacements')
router.register(r'dicts/statuses/breaks', viewset=dicts.BreakStatusView, basename='breaks-statuses')
router.register(r'dicts/statuses/replacements', viewset=dicts.ReplacementStatusView, basename='replacements-statuses')

urlpatterns = [
]

urlpatterns += path('breaks/', include(router.urls)),
