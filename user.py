import time
import requests
from bs4 import BeautifulSoup
import re
import random

class User:
    def __init__(self, profile_url, driver, cookie, X_IG_App_ID):
        self.driver = driver
        self.profile_url = profile_url
        self.cookie = cookie
        self.X_IG_App_ID = X_IG_App_ID
        self.page_source = ""
        self.bio = ""
        self.name = ""
        self.pk_id = ""
        self.following = []
        self.followers = []

        # Call the initialization methods to populate data
        self.set_page_source()
        self.set_bio()
        self.set_name()
        self.set_pk_id()
        self.set_following()
        self.set_followers()

    def set_page_source(self):
        """
        Load the Instagram profile page and set the page source.
        """
        self.driver.get(self.profile_url)

        # Wait to ensure the page has fully loaded
        time.sleep(random.randint(5, 15))  # Adjust sleep time if necessary

        # Scroll down the page to simulate user interaction (to trigger lazy loading)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(5, 15))

        # Get the updated page source (HTML code)
        self.page_source = self.driver.page_source

    def set_bio(self):
        """
        Extract the user's bio from the page source.
        """
        soup = BeautifulSoup(self.page_source, "html.parser")

        # Find the <div> containing the text like "Public figure"
        public_figure_div = soup.find("div", class_="_ap3a _aaco _aacu _aacy _aad6 _aade")
        title = "" if not public_figure_div else public_figure_div.text.strip() + " "

        # Regular expression to capture the bio part from the <meta> tag's content attribute
        bio_pattern = re.compile(r'content=".*? - .*? \(@.*?\) on Instagram: &quot;(.*?)&quot;', re.DOTALL)

        # Search for the pattern in the page source
        bio_match = bio_pattern.search(self.page_source)

        if bio_match:
            # Extract the bio and replace HTML entities with actual characters
            self.bio = title + bio_match.group(1).replace("&quot;", '"').replace("&amp;", "&")

    def set_name(self):
        """
        Extract the user's name from the page source.
        """
        soup = BeautifulSoup(self.page_source, 'html.parser')

        # Find the meta tag with property="og:title"
        meta_tag = soup.find('meta', attrs={'property': 'og:title'})

        if meta_tag:
            content = meta_tag.get('content', '')
            # Extract the name before the parentheses
            self.name = content.split('(')[0].strip()
        else:
            self.name = ""

    def set_pk_id(self):
        """
        Extract the user's Instagram ID (pk_id) from the page source.
        """
        # Look for the pattern of the Instagram ID using 'profile_id'
        pattern = re.compile(r'"profile_id":"(\d+)"')

        # Search for the ID
        match = pattern.search(self.page_source)

        if match:
            self.pk_id = match.group(1)

    def set_following(self):
        """
        Fetch the list of users that this user is following using the Instagram API.
        """
        url = f"https://www.instagram.com/api/v1/friendships/{self.pk_id}/following/"

        # Set the headers with the provided IG App ID and Session Cookie
        headers = {
            "X_IG_App_ID": self.X_IG_App_ID,
            "Cookie": f"sessionid={self.cookie}"
        }

        try:

            time.sleep(random.randint(5, 15))
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Iterate over each user in the JSON response
                for user in data.get("users", []):
                    username = user.get("username")
                    # Store the username in the following list
                    self.following.append(f"https://www.instagram.com/{username}/")
            else:
                print(f"Failed to retrieve following data. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def set_followers(self):
        """
        Fetch the list of users that follow this user using the Instagram API.
        """
        url = f"https://www.instagram.com/api/v1/friendships/{self.pk_id}/followers/"

        # Set the headers with the provided IG App ID and Session Cookie
        headers = {
            "x-ig-app-id": self.X_IG_App_ID,
            "cookie": f"sessionid={self.cookie}"
        }

        try:

            time.sleep(random.randint(5, 15))
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Iterate over each user in the JSON response
                for user in data.get("users", []):
                    username = user.get("username")
                    # Store the username in the followers list
                    self.followers.append(f"https://www.instagram.com/{username}/")
            else:
                print(f"Failed to retrieve followers data. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
    def get_profile_url(self):
        """
        Get the profile URL.
        """
        return self.profile_url

    def get_cookie(self):
        """
        Get the session cookie.
        """
        return self.cookie

    def get_X_IG_App_ID(self):
        """
        Get the Instagram App ID.
        """
        return self.X_IG_App_ID

    def get_page_source(self):
        """
        Get the page source.
        """
        return self.page_source

    def get_bio(self):
        """
        Get the bio.
        """
        return self.bio

    def get_name(self):
        """
        Get the name of the user.
        """
        return self.name

    def get_pk_id(self):
        """
        Get the Instagram profile ID (pk_id).
        """
        return self.pk_id

    def get_following(self):
        """
        Get the list of users the profile is following.
        """
        return self.following

    def get_followers(self):
        """
        Get the list of users following the profile.
        """
        return self.followers
    
    def __str__(self):
        return f"Link: {self.profile_url}\nPK_id: {self.pk_id}\nName: {self.name}\nFollowers: {self.followers}\nFollowing: {self.following}\n{self.bio}"
