from django.urls import path
from . import views

urlpatterns = [
    path('kv/', views.post),
    path('kv/<int:obj_id>', views.get_put_delete)
]