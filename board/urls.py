from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductAddView, ProductView, LocationView, UnitView, ProductListView, ProductUpdateView

router = DefaultRouter()
router.register(r'product', ProductView)
router.register(r'location', LocationView)
router.register(r'unit', UnitView)

urlpatterns = [
    path('create/', ProductAddView.as_view()),
    path('', include(router.urls)),
    path('listdetail/<str:location>/', ProductListView.as_view()),
    path('update/<str:pk>/', ProductUpdateView.as_view())
]