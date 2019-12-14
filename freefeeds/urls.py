from django.urls import path

from freefeeds import views

urlpatterns = [
    path('accounts/verify_credentials', views.verify_credentials),
    path('accounts/<int:uid>/statuses', views.timelines_account),

    path('timelines/public', views.timelines_public),
    path('timelines/home', views.timelines_home),
    path('statuses/<int:md_id>', views.status_detail),
    path('statuses/<int:md_id>/context', views.status_context),

    path('filters', views.filters),
    path('notifications', views.notifications),
    
    path('instance', views.instance_info),
    path('apps', views.apps),
]
