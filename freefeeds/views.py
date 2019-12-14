import json

from django.http import HttpResponse

from freefeeds.client import Client


def _generic_feed_data(request, client_handler):
    client = Client.from_request(request)
    data = client_handler(client)
    return HttpResponse(json.dumps(data), content_type="application/json")

def verify_credentials(request):
    return _generic_feed_data(request, lambda c: c.get_me().to_md_json())

def timelines_account(request):
    return _generic_feed_data(request, lambda c: [p.to_md_json() for p in c.get_user_timeline()])

def timelines_public(request):
    return _generic_feed_data(request, lambda c: [])

def timelines_home(request):
    params = {}
    if request.GET.get("limit"):
        params["limit"] = int(request.GET.get("limit"))
    if request.GET.get("max_id"):
        params["max_id"] = int(request.GET.get("max_id"))
    if request.GET.get("since_id"):
        params["since_id"] = int(request.GET.get("since_id"))
    return _generic_feed_data(request, lambda c: [p.to_md_json() for p in c.get_get_home(**params)])

def status_detail(request, md_id):
    return _generic_feed_data(request, lambda c: c.get_post(md_id)[0].to_md_json())

def status_context(request, md_id):
    return _generic_feed_data(request, lambda c: [p.to_md_json() for p in c.get_post(md_id)[1:]])

def filters(request):
    return _generic_feed_data(request, lambda c: [])

def notifications(request):
    return _generic_feed_data(request, lambda c: c.get_notifications())

def instance_info(request):
    data = {
      "uri":"http://feedodon.rkd.pw/",
      "title":"feedik bridge",
      "version":"1"
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

def apps(request):
    # TODO save app and retrieve the data
    data = {
        "id": 0,
        "name": "Tusky",
        "website": "",
        "redirect_uri": [],
        "client_id": "client_id",
        "client_secret": "client_secret"
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

def nodeinfo_v1(request):
    data = {
        "links":[
            {
                "rel":"http://nodeinfo.diaspora.software/ns/schema/2.0",
                "href":"https://feedodon.rkd.pw/nodeinfo/2.0"
            }
        ]
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

def nodeinfo_v2(request):
    data = {
        "version":"2.0",
        "software":{
            "name":"feedodon","version":"0.1"
        },
        "protocols":["activitypub"],
        "usage":{
            "users":{"total":1,"activeMonth":1,"activeHalfyear":1},
            "localPosts":100500
        },
        "openRegistrations": False
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

