import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from foundation.models import User


class MikaIDAuthentication(authentication.BaseAuthentication):
    """
    Authentication class used to introspect the oAuth 2.0 bearer token with
    the remote oAuth server to verify the token is valid and load the user
    profile in the django request. If the token is valid but the user does not
    have the record then this class will fetch the user profile and save it
    locally to this web-app. If the token is invalid then a 403 error gets
    generated.

    The following variables must be defined in the ``settings.py`` file:
    - MIKAID_RESOURCE_SERVER_INTROSPECTION_URL
    - MIKAID_RESOURCE_SERVER_INTROSPECTION_TOKEN
    """

    def authenticate(self, request):
        # The following code will extract the oAuth 2.0 token from the
        # request made by the user.
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        auth_token = str(auth).replace("Bearer ", "")

        # The following code will take the token and introspect it with
        # the oAuth 2.0 authentication server.
        introspection_url = "http://127.0.0.1:8000/api/introspect"
        introspection_token = "8xwZiccAwfNZsaa9ZSU7rb6QXXDx2k"
        headers = {"Authorization": "Bearer {}".format(introspection_token)}
        response = requests.post(
            introspection_url,
            data={"token": auth_token}, headers=headers
        )

        # Format the data to be in a JSON format.
        results_json = response.json()

        # Extract the response data.
        is_active = results_json.get('active', False)
        client_id = results_json.get('client_id', False)

        # Is the token valid?
        if is_active == False:
           raise exceptions.AuthenticationFailed('Token is not valid.')

        try:
            # Attempt to lookup the user account for the specific ID.
            user = User.objects.get(id=client_id) # get the user
        except User.DoesNotExist:
            # Perform a fetch request to the remote API server to get our
            # user account for the ID value.
            response = requests.get(
                "http://127.0.0.1:8000/api/user/"+str(client_id)+"/", headers=headers
            )

            # Convert the results into a JSON format.
            results_json = response.json()

            # Attempt to create our user and error if we fail.
            user = User.objects.create_user_from_api(results_json)
            if user is None:
               raise exceptions.AuthenticationFailed('Failed creating the user.')

        # We have a successfull authentication then return our user account.
        # To understand more why we are doing this then look into an source code
        # of Django REST Framework.
        # https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
        return (user, None)
