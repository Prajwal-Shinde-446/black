# urls.py (inside your app)
from django.urls import path
from . import views

urlpatterns = [
    path('import_data/', views.import_data, name='import_data'),
    path('view', views.view, name='view'),
    path('handle_refresh', views.handle_refresh, name='handle_refresh'),
#     path('end', views.get_all_end_years, name='end'),
#     path('filter', views.your_view, name='filter'),
]
