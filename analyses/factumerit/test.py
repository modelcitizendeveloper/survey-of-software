
from authentik.sources.oauth.models import UserOAuthSourceConnection
import json
import base64

conn = UserOAuthSourceConnection.objects.last()
if conn:
    # id_token is a JWT - decode the payload
    parts = conn.access_token.split('.')  # This might be the access token, not id_token
    print("Token parts:", len(parts))

Or we bypass MAS entirely - manually set email in Authentik for now:

from authentik.core.models import User
u = User.objects.get(username="ivantohelpyou")
u.email = "ivan@ivantohelpyou.com"
u.save()
print("Email set manually")