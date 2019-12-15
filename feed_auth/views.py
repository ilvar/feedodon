import json

from django.http import HttpResponse
from django.shortcuts import redirect, render

from feed_auth.forms import AuthForm


def oauth_authorize(request):
    if request.method == "POST":
        form = AuthForm(data=request.POST)
        if form.is_valid():
            api_key = form.cleaned_data["api_key"]
            redirect_url = request.GET["redirect_uri"] + "?code=%s" % api_key
            
            scheme = redirect_url.split(":")[0]
            from django.http.response import HttpResponseRedirectBase
            if scheme not in HttpResponseRedirectBase.allowed_schemes:
                HttpResponseRedirectBase.allowed_schemes += [scheme]
            
            return redirect(redirect_url, permanent=False)
    else:
        form = AuthForm()
    return render(request, "feed_auth.html", {"form": form})


def oauth_token(request):
    code = request.GET.get("code", request.POST["code"])
    return HttpResponse(json.dumps({"access_token": code}), content_type="application/json")