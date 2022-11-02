from pyfacebook import GraphAPI

api = GraphAPI(app_id="APP_ID", app_secret="APP_SECRET", oauth_flow=True)

api.get_authorization_url()

api.exchange_long_lived_user_access_token()
