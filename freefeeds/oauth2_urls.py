from django.conf.urls import url

from oauth2_provider import views


app_name = "oauth2_provider"


base_urlpatterns = [
    url(r"^authorize$", views.AuthorizationView.as_view(), name="authorize"),
    url(r"^token$", views.TokenView.as_view(), name="token"),
    url(r"^revoke_token$", views.RevokeTokenView.as_view(), name="revoke-token"),
    url(r"^introspect$", views.IntrospectTokenView.as_view(), name="introspect"),
]


management_urlpatterns = [
    # Application management views
    #url(r"^apps$", views.ApplicationList.as_view(), name="list"),
    url(r"^apps$", views.ApplicationRegistration.as_view(), name="register"),
    url(r"^apps/(?P<pk>[\w-]+)$", views.ApplicationDetail.as_view(), name="detail"),
    url(r"^apps/(?P<pk>[\w-]+)/delete$", views.ApplicationDelete.as_view(), name="delete"),
    url(r"^apps/(?P<pk>[\w-]+)/update$", views.ApplicationUpdate.as_view(), name="update"),
    # Token management views
    url(r"^authorized_tokens$", views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
    url(r"^authorized_tokens/(?P<pk>[\w-]+)/delete$", views.AuthorizedTokenDeleteView.as_view(),
        name="authorized-token-delete"),
]


urlpatterns = base_urlpatterns + management_urlpatterns
