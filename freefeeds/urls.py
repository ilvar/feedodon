from django.urls import path

from freefeeds import views

urlpatterns = [
    path('v1/accounts/verify_credentials', views.verify_credentials),
    path('v1/accounts/<int:uid>/statuses', views.timelines_account),

    path('v1/timelines/public', views.timelines_public),
    path('v1/timelines/home', views.timelines_home),
    path('v1/statuses/<int:md_id>/context', views.status_context),
    path('v1/statuses/<int:md_id>', views.status_detail),
    path('v1/statuses', views.status_post),

    path('v1/filters', views.filters),
    path('v1/notifications', views.notifications),
    
    path('v1/instance', views.instance_info),
    path('v1/apps', views.apps),
    
    path('direct_messages.json', views.direct_messages),
    path('saved_searches/list', views.saved_searches),

]
