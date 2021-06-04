from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

def generate_token(client_secret_file, new_token_output):

	flow = InstalledAppFlow.from_client_secrets_file(
	    client_secret_file,
	    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

	flow.run_local_server(
	    host='localhost',
	    port=8080,
	    prompt = 'consent',
	    authorization_prompt_message='Please visit this URL: {url}',
	    success_message='The auth flow is complete; you may close this window.',
	    open_browser=True)
	credentials = flow.credentials
	with open(new_token_output, 'wb') as f:
		print("Dumping to Pickle File...")
		pickle.dump(credentials, f)

	print('Saved New Pickle token.pickle')
	return credentials
	