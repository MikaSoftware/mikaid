# Tutorial
This tutorial explains how to setup this project for all your micro-services in your web-application. For this tutorial we are assuming you are setting a web-application which is called "Mika Software Corporation".


## Instruction
### Application Authorization
#### Add Application

1. Start by creating an administrator user account.

  ```
  python manage.py create_admin_user "bart@mikasoftware.com" "123password" "Bart" "Mika";
  ```

2. Next create a password grant application which will be used for our web-application. It is important that you associate the admin user account with this password authorization.

  ```
  python manage.py setup_resource_server_authorization "bart@mikasoftware.com"
  ```

3. Copy and save the output, you should see something like this. This information will be used for all the micro-services / web-application that you are building:

  ```
  Resource Server - Auth Type: password
  Resource Server - Client ID: DH3JtqAJ9sHB5dNDe1EVkVptsfZRkkgshaoLnfmr
  Resource Server - Client Secret: uS1cgnF2YxBl0RvxhdD3KLpI1dorTGqkUPEcxiAKAnZ2MZYuIMmOwoz0KVmJ15HCyKSMSaD19ZHxMTp0VerWhtsbWSR3gZeRnGJfthV37xK0bcdaunqZOkqcSrMXsxlr
  Resource Server - Access Token: DNvWPIcCNZulYrx1zIBPTu8DEANYn9
  ```

4. Update your ``.env`` file with the above information.


### User
#### Add User and Login

1. Create a test user account.

  ```
  python manage.py create_regular_user 0 "john@smith.com" "123password" "John" "Smith";
  ```

2. Login with the regular user account.

  ```
  curl -X POST -d "password=123password&email=john@smith.com" http://localhost:8000/api/login

  (Alternative)
  curl -X POST -d "grant_type=password&username=john@smith.com&password=123password" -u"rOQjJQHCrYzVjppbSJgna2yz96fYvEzJCuQf7923:nXC84pw6t7QvnMQvNd7Q0MkfeW0ZFwGcgKVuN5EiwpPnAclxVenp5PeOnxgatFpYEjPtmIlaiJb28HOqh8CdNxzSSknmdoEhvhVpwfgpcTQRod388h1fjZD1YGUeRWR2" http://localhost:8000/o/token/
  ```

3. The results should look something like this:

  ```
  {
      "token":"H7jfbBjGqz0DPK6siK3uU6M1sIwadW",
      "scope":"read,write,introspection"
  }
  ```

#### Introspection

Introspection should be used on your micro-service to verify the token works.

```
curl -H "Authorization: Bearer DNvWPIcCNZulYrx1zIBPTu8DEANYn9" -d "token=H7jfbBjGqz0DPK6siK3uU6M1sIwadW" -X POST http://127.0.0.1:8000/api/introspect;
```

The results should be something like this:

```
{
    "active":true,
    "client_id":3,
    "email":"john@smith.com",
    "scope":"read write introspection",
    "exp":"2019-01-15T01:57:29.432765Z"
}
```

### Registration

1. If you'd like to register a brand new user through the API endpoint then run the following.

  ```
  curl -X POST -d "password=123password&password_repeat=123password&tenant_id=0&first_name=John&last_name=AppleSeed&email=john@appleseed.com" http://localhost:8000/api/register
  ```

  2. The API endpoint should basically return something like this:

  ```
  {"token":"I2zhui1SH6561HGfo4GKBJkywdrVF1","scope":"read,write,introspection","client_id":3,"email":"john@appleseed.com","exp":"3795-01-14T20:41:26.025735Z"}
  ```

### Misc

curl -H "Authorization: Bearer DNvWPIcCNZulYrx1zIBPTu8DEANYn9" http://127.0.0.1:8000/api/users;
curl -H "Authorization: Bearer DNvWPIcCNZulYrx1zIBPTu8DEANYn9" http://127.0.0.1:8000/api/user/1/;
