import os, requests

def token(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials")
    
    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)
    
    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate",
        headers={"Authorization": token}
    )

    if response.status_code == 200:
        print("Token validated")
        return response.text, None
    else:
        print("Non-valid token")
        return None, (response.text, response.status_code)