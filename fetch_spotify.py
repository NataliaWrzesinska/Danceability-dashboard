import requests
import pandas as pd
import traceback

# Spotify app credentials
CLIENT_ID = '###'
CLIENT_SECRET = '###'

# Function for authentication and obtaining access token
def get_spotify_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=payload, auth=(client_id, client_secret))
    return response.json().get("access_token")

# Function to search for track/artist information on Spotify
def search_spotify(query, token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to update DataFrame with cover URLs
def update_dataset_with_covers(df, token):
    cover_urls = []
    for index, row in df.iterrows():
        try:
            search_result = search_spotify(row['track_name'], token)
            cover_url = search_result['tracks']['items'][0]['album']['images'][0]['url']
        except (IndexError, KeyError):
            cover_url = "Not Found"
        cover_urls.append(cover_url)
    df['cover_url'] = cover_urls
    return df

# Main process
def main():
    try:
        spotify_token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
        data_path = r"###"  # Corrected path with raw string
        df = pd.read_csv(###)
        updated_df = update_dataset_with_covers(df, spotify_token)
        output_path = r"###"  # Save location for the new file
        updated_df.to_csv(output_path, index=False)
        print("File has been updated and saved.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
