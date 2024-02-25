from django.urls import path
from . import views

urlpatterns = [
    path('assets/create', views.CreateAssetUploadEndpoint.as_view()),
    path('assets/<uuid:id>', views.GetAssetUploadEndpoint.as_view()),
    path('assets/<uuid:id>/finalize', views.FinalizeAssetUploadEndpoint.as_view()),
    path('assets/<uuid:id>/extend', views.ExtendAssetLifetimeEndpoint.as_view()),
    path('assets/<uuid:id>/inspections/<str:inspection_type>', views.GetAssetInspectionEndpoint.as_view()),
    path('marktplaats/fetch', views.FetchMarktplaatsEndpoint.as_view()),
]
