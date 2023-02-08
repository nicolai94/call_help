from django.urls import path, include
from rest_framework.routers import DefaultRouter
from organisations.views import dicts, organisations, employees

router = DefaultRouter()

router.register(r'dicts/positions', viewset=dicts.PositionView, basename='reg')
router.register(r'search', viewset=organisations.OrganisationSearchView, basename='organisation-search')
router.register(r'manage', viewset=organisations.OrganisationView, basename='organisations')
# регулярное выражение для изменения id
router.register(r'manage/(?P<pk>\d+)/employees', viewset=employees.EmployeeView, basename='employees')

urlpatterns = [
]

urlpatterns += path('organisations/', include(router.urls)),
