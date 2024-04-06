import re
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()


class Chatwoot:
    def __init__(self):
        self.api_access_token = os.environ.get('api_access_token')
        self.account_id = os.environ.get('account_id')
        self.base_url = os.environ.get('base_url')
        self.portal_id = 'healsane'
        self.author_id = os.environ.get('author_id')
    
    @staticmethod
    def sluggify(text, separator='-'):
        """
        Convert text into a URL-friendly slug.

        Parameters:
        - text (str): The text to be converted.
        - separator (str): The separator to use between words. Default is '-'.

        Returns:
        - str: The sluggified text.
        """
        # Convert to lowercase
        slug = text.lower()
        # Replace non-word characters and spaces with the separator
        slug = re.sub(r'\W+|_', separator, slug)
        # Replace multiple separators with a single separator
        slug = re.sub(r'{0}+'.format(separator), separator, slug)
        # Remove leading and trailing separators
        slug = slug.strip(separator)
        return slug

    def add_category(self, description, name, slug, locale=None, position=None, associated_category_id=None, parent_category_id=None):
        """
        Adds a new category to a portal in Chatwoot.
        :param account_id: The numeric ID of the account.
        :param user_api_access_token: The API key for user authorization.
        :param description: Category description.
        :param locale: Category locale.
        :param name: Category name.
        :param slug: Category slug.
        :param position: Category position in the portal list.
        :param portal_id: The numeric ID of the portal.
        :param associated_category_id: ID to associate similar categories (optional).
        :param parent_category_id: ID of the parent category (optional).
        :return: The response from the Chatwoot API.
        """
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/portals/{self.portal_id}/categories"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "api_access_token": self.api_access_token
        }
        payload = {
            "description": description,
            # "locale": locale,
            "name": name,
            "slug": slug,
            "position": position,
            "portal_id": self.portal_id,
            "account_id": self.account_id,
            "associated_category_id": associated_category_id,
            "parent_category_id": parent_category_id
        }
        # Filter out None values from the payload
        payload = {k: v for k, v in payload.items() if v is not None}

        response = requests.post(url, json=payload, headers=headers)
        return response
    
    def add_article(self, title, content, category_id, status="draft"):
        """
        Adds a new article to a portal in Chatwoot.
        
        :param title: The title of the article.
        :param content: The text content of the article.
        :param category_id: The numeric ID of the category under which to add the article.
        :param slug: URL-friendly identifier for the article (optional).
        :param meta: Metadata for search (optional).
        :param position: Article position in category (optional).
        :param status: Status of the article (optional).
        :param author_id: The numeric ID of the author (optional).
        :param folder_id: The numeric ID of the folder (optional).
        :param associated_article_id: ID to associate similar articles (optional).
        :return: The response from the Chatwoot API.
        """
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/portals/{self.portal_id}/articles"
        
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "api_access_token": self.api_access_token
        }
        payload = {
            "title": title,
            "content": content,
            "slug": self.sluggify(title + str(random.randint(1, 100))),
            "meta": {},
            "status": status,
            "portal_id": self.portal_id,
            "account_id": self.account_id,
            "author_id": 1,
            "category_id": category_id,
        }
        
        # Filter out None values from the payload
        payload = {k: v for k, v in payload.items() if v is not None}

        response = requests.post(url, json=payload, headers=headers)
        return response

    def get_categories(self):
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/portals/{self.portal_id}/categories"
        
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "api_access_token": self.api_access_token
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        data= data['payload']

        categorie_ids = dict()
        
        for categorie in data:
            categorie_ids[categorie['slug']] = categorie['id']
        return categorie_ids

    def list_articles(self):
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/portals/{self.portal_id}/articles"

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "api_access_token": self.api_access_token
        }

        ids = list()
        
        page = 1
        params = {"page": page}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        data= data['payload']
        
        
        while data:
            for article in data:
                ids += [article['id']]
            
            page += 1
            params = {"page": page}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            data= data['payload']
        
        return(ids)
    
    def publish_article(self, id):
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/portals/{self.portal_id}/articles/{id}"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "api_access_token": self.api_access_token
        }

        payload = {
            "status": 1,
        }

        response = requests.patch(url, json=payload, headers=headers)


def main():
    # Example usage
    user_api_access_token = "your_user_api_access_token_here"
    account_id = 123  # Replace with your account ID
    description = "Example category description"
    locale = "en"
    name = "Example Category"
    slug = "example-category"
    position = 1
    portal_id = 456  # Replace with your portal ID

    # Call the function
    result = add_category(account_id, user_api_access_token, description, locale, name, slug, position, portal_id)


if __name__ == "__main__":
    chatwoot = Chatwoot()
    
    result = chatwoot.list_articles()
    print(result)

    #main()