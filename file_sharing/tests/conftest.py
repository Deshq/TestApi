import uuid
import pytest


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_password():
   return 'test_password'

@pytest.fixture
def create_user(db, django_user_model, test_password):
   def cr_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return cr_user

@pytest.fixture
def auto_login_user(db, api_client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       api_client.login(username=user.username, password=test_password)
       return api_client, user
   return make_auto_login

@pytest.fixture
def create_superUser(db, django_user_model, test_password):
   def cr_superuser(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_superuser(**kwargs)
   return cr_superuser

@pytest.fixture
def auto_login_superUser(db, api_client, create_superUser, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_superUser()
       api_client.login(username=user.username, password=test_password)
       return api_client, user
   return make_auto_login

@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


