from pyfacebook import GraphAPI

api = GraphAPI(app_id="APP_ID", app_secret="APP_SECRET", oauth_flow=True)

api.get_authorization_url()

# I couldn't figure this part out. I'm not sure what is supposed to go in the place
# of "url redirected" from the link, but I think we want to use a long lived user
# access token instead of the regular one like they had in the pypi link. 
api.exchange_long_lived_user_access_token()
