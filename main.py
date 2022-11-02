from pyfacebook import GraphAPI

api = GraphAPI(app_id="2280642395432600", app_secret="921e9b85ac7198001c4199778dbd3718", oauth_flow=True)

api.get_authorization_url()

# I couldn't figure this part out. I'm not sure what is supposed to go in the place
# of "url redirected" from the link, but I think we want to use a long lived user
# access token instead of the regular one like they had in the pypi link. 
api.exchange_long_lived_user_access_token()
