# -*- coding: utf-8 -*-
import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from generate_refresh_token import generate_token
import pickle
from update_view_count import get_video_details, update_title

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"
    new_secret_file = "token.pickle"
    credentials = None
    if os.path.exists(new_secret_file):
        print("Loading Existing credentials")
        with open(new_secret_file, "rb") as file:
            credentials = pickle.load(file)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshin Access Token...")
            credentials.refresh(Request())
        else:
            print("Generating Token...")
            credentials = generate_token(client_secrets_file, new_secret_file)
        # Get credentials and create an API client
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    video_id = "xxxxxxxxxx" ## Enter your video ID
    vid_snippet, view_count, is_changed = get_video_details(youtube, video_id)
    if is_changed:
         update_title(youtube, vid_snippet, video_id, view_count)
    else:
        pass

def get_video_details(youtube, video_id):
    # Request (This is what asks Youtube API for the channel data)
    request = youtube.videos().list(
        part="snippet,statistics",
        id="Ew0aneY5uUc"
    )
    response = request.execute()

    data = response["items"][0];
    vid_snippet = data["snippet"];

    title = vid_snippet["title"];

    views = str(data["statistics"]["viewCount"])
    
    print("data_statistics: ", data)
    print("Title of Video: " + title)
    print("Number of Views: " + views)

    change = (views not in title)
    # request = youtube.videos().list(
    #     part="statistics",
    #     id="Ew0aneY5uUc"
    # )
    # response = request.execute()
    # view_count = response['items'][0]['statistics']['viewCount']
    return vid_snippet, views, change

def update_title(youtube, vid_snippet, video_id, view_count):
    vid_snippet["title"] = "The views on this video is " + view_count
    request = youtube.videos().update(
        part="snippet",
        body={
          "id": video_id,
          "snippet": vid_snippet
        }
    )
    response = request.execute()
    print("it worked")

if __name__ == "__main__":
    main()