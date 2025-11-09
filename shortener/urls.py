from django.urls import path
from . import views

urlpatterns = [
    # Redirect endpoint
    path('go/<path:path>', views.redirect_view, name='redirect'),
    
    # Portal endpoints
    path('admin/', views.portal_home, name='portal_home'),
    path('admin/create/', views.link_create, name='link_create'),
    path('admin/edit/<int:pk>/', views.link_edit, name='link_edit'),
    path('admin/delete/<int:pk>/', views.link_delete, name='link_delete'),
    path('admin/toggle/<int:pk>/', views.link_toggle_active, name='link_toggle'),
]
