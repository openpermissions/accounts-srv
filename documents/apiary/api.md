FORMAT: 1A
HOST: https://acc-stage.copyrighthub.org

# Open Permissions Platform Accounts Service
Provides party accounts, and against a party account can be registered organisations, services and repositories.

## Standard error output
On endpoint failure there is a standard way to report errors.
The output should be of the form

| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| errors   | An array of errors        | array  |

## Error
| Property | Description                                 | Type   |
| :------- | :----------                                 | :---   |
| source   | The name of the service producing the error | string |
| message  | A description of the error                  | string |

# Authorization

The majority of endpoints will require you to provide an access token in the authorization header.

## Requesting a Token
In order to obtain an access token you will need to perform the following steps:

1. [Register with the service](#reference/users/users-resource/register-a-new-user)
2. [Verify your account](#reference/users/user-verification-resource/verify-user)
3. [Login](#reference/login/login-user/authenticate-user-and-obtain-token)

Logging in will return an authorization token in the response body.

## Using your Token

You will need to provide this token wherever **Authorization: [TOKEN]**
is indicated in the headers for an endpoint.

### Example
Authorization: e4dcd05e-c503-11e5-9912-ba0be0483c18

## Token Expiration
Tokens will expire after 24 hours, after which time you will need to log in again to obtain a new access token.

# Cross-origin resource sharing (CORS)
The API supports cross-origin requests from any origin using CORS.

# Account service objects

## The User object
| Property            | Description                           | Type    |
| :-------            | :----------                           | :---    |
| id                  | User's id                             | string  |
| email               | Contact email address                 | string  |
| first_name          | User's first name                     | string  |
| last_name           | User's last name                      | string  |
| phone               | Contact phone number                  | string  |
| organisations       | Organisations user belongs to         | object  |
| verified            | Verification status                   | string  |
| has_agreed_to_terms | User has agreed to Terms & Conditions | boolean |

## The organisation object
| Property            | Description                                         | Type   |
| :-------            | :----------                                         | :---   |
| id                  | Organisation ID                                     | string |
| name                | Organisation name                                   | string |
| state               | Organisation State                                  | string |
| created_by          | The user who created the organisation               | string |
| description         | Description                                         | string |
| address             | Address                                             | string |
| phone               | Phone                                               | string |
| email               | Email                                               | email  |
| website             | Website                                             | string |
| facebook            | Facebook page                                       | string |
| twitter             | Twitter handle                                      | string |
| google+             | Google+ account                                     | string |
| instagram           | Instagram account                                   | string |
| youtube             | Youtube page                                        | string |
| linkedin            | Linkedin page                                       | string |
| myspace             | MySpace page                                        | string |
| reference_links     | Object of reference link urls for organisation      | object |
| modal_header_text   | Text to display in header of Licence Modal popup    | string |
| modal_footer_text   | Text to display in footer of Licence Modal popup    | string |
| modal_link_text     | Text to display in link of Licence Modal popup      | string |
| modal_link_url      | Url to link to in link of Licence Modal popup       | url    |
| star_rating         | 1-5 Rating of Organisation                          | number |

## The Role object
| Property | Description     | Type   |
| :------- | :----------     | :---   |
| name     | Role Name       | string |
| id       | Role Id         | string |

## The Service object
| Property        | Description                      | Type   |
| :-------        | :----------                      | :---   |
| id              | Service ID within the OPP        | string |
| name            | Name of the Service              | string |
| location        | Location of the service          | url    |
| organisation_id | Id of associated organisation    | string |
| service_type    | The service type                 | string |
| created_by      | The user who created the service | string |
| permissions     | Permission object                | object |
| state           | Approval state of the service    | string |


## The Repository object
| Property          | Description                            | Type   |
| :---------------- | :------------------------------------- | :----- |
| id                | Repository id                          | string |
| name              | Repository name                        | string |
| created_by        | Id of user that created the repository | string |
| organisation      | An organisation object                 | object |
| service           | A service object                       | object |
| state             | Repository approval state              | string |
| permissions       | Permission object                      | object |


## Permission Object

Access to services and repositories is controlled by an access control list (ACL).
Each rule in the ACL is an array with 2 items; an object that contains
organisation ID's and/or service types, and the access level.

| Property          | Description                                                  | Type   |
| :-------          | :----------                                                  | :---   |
| type              | Type of access control ('organisation_id' or 'service_type') | string |
| value             | Id or type to apply access control to                        | string |
| permission        | Access Level                                                 | string |


### Example

In this example,
 + `org1` has read write access
 + any organisation with an onboarding service has read write access
 + `org2` has no access

```json
{
  "permissions": [
    {"type": "organisation_id", "value": "org1", "permission": "rw"},
    {"type": "service_type", "value": "onboarding", "permission": "rw"},
    {"type": "service_type", "value": "org2", "permission": "-"},
  ]
}
```

# Account service enums

## Approval State

Currently applicable to organisations, services and repositories.

| State    | Description                            |
| :----    | :----------                            |
| pending  | Pending approval from administrator    |
| approved | Has been approved and is ready to use  |
| rejected | Has been rejected and cannot be used   |

## Access levels

| Access Level | Description                            |
| :----------- | :----------                            |
| w            | Permitted to write to the resource     |
| r            | Permitted to read the resource         |
| rw           | Permitted to read / write the resource |
| -            | Denied access to the resource          |

## Service Types

| Service Types  |
| :------------  |
| external       |
| authorisation  |
| identity       |
| index          |
| onboarding     |
| query          |
| repository     |
| resolution     |
| transformation |

# Group Service Information

## Accounts Service information [/v1/accounts]
Information on the service

### Retrieve service information [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service information   | object |

##### Service information
| Property     | Description                    | Type   |
| :-------     | :----------                    | :---   |
| service_name | The name of the api service    | string |
| version      | The version of the api service | string |

+ Request Get basic API information

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "service_name": "Open Permissions Platform Accounts Service",
                    "version": "0.1.0"
                }
            }

# Group Capabilities

## Service Capabilities [/v1/accounts/capabilities]
Returns the service capabilities i.e. max accepted length of a
field etc.

### Retrieve Service Capabilities [GET]
#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service capabilities  | object |

##### Service capabilities
| Property                     | Description                                | Type  |
| :-------                     | :----------                                | :---- |
| max_length_email             | Max length of contact email address        | int   |
| max_length_password          | Max length of User password                | int   |
| max_length_first_name        | Max length of User's first name            | int   |
| max_length_last_name         | Max length of User's last name             | int   |
| max_length_phone             | Max length of phone number                 | int   |
| min_length_role_name         | Min length of role name                    | int   |
| max_length_role_name         | Max length of role name                    | int   |
| min_length_organisation_name | Min length of organisation name            | int   |
| max_length_organisation_name | Max length of organisation name            | int   |
| min_length_service_name      | Min length of service name                 | int   |
| max_length_service_name      | Max length of service name                 | int   |
| min_length_service_location  | Min length of service location (URL or IP) | int   |
| max_length_service_location  | Max length of service location (URL or IP) | int   |

+ Request Get capabilities

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "max_length_email": 256,
                    "max_length_password": 128,
                    "max_length_first_name": 256,
                    "max_length_last_name": 256,
                    "max_length_phone": 24,
                    "min_length_role_name": 3,
                    "max_length_role_name": 128,
                    "min_length_organisation_name": 512,
                    "max_length_organisation_name": 512,
                    "min_length_service_name": 3,
                    "max_length_service_name": 128,
                    "min_length_service_location": 10,
                    "max_length_service_location": 512
                }
            }

# Group Login
This endpoint handles login and session management.

## Login user [/v1/accounts/login]
Performs the login. Takes in an email address and password.

### Authenticate user and obtain token [POST]
#### Input
|Property|Description          |Type  |Mandatory|
|:-------|:--------------------|:-----|:--------|
|email   |Contact email address|string|yes      |
|password|User password        |string|yes      |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Authentication data       | object |

##### Authentication data
| Property | Description | Type   |
| :------- | :---------- | :----- |
| token    | User token  | string |
| user     | User        | object |

+ Request Login (application/json)

    + Headers

            Accept: application/json

    + Body

            {
                "email": "john.bull@mycompany.com",
                "password": "3832j942cu2d"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "token": "d419d20c-e14f-4b52-98d6-0e8717a68f28",
                    "user": {
                        "id": "a user id",
                        "email": "john.bull@mycompany.com",
                        "first_name": "John",
                        "last_name": "Bull",
                        "phone": "0123456789",
                        "verified": true
                    }
                }
            }


+ Request Attempt to log in with invalid email and password (application/json)

    + Headers

            Accept: application/json

    + Body

            {
                "email": "non.exitsting@email.com",
                "password": "3832j942cu2d"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "message": "Please provide valid credentials",
                        "source": "accounts"
                    }
                ]
            }


+ Request Attempt to log in without email or password (application/json)

    + Headers

            Accept: application/json

    + Body

            {
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

             {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide valid credentials"
                    }
                ]
            }

# Group Users

## Users Resource [/v1/accounts/users]

### Get all users [GET]

#### Authorization
Logged in

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Array of users            | array  |

+ Request Get all users

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                data: [
                    {
                        "id": "the user id",
                        "first_name": "John",
                        "last_name": "Bull",
                        "company": "mycompany",
                        "phone": "+44 207 123 4567",
                        "email": "john@mycompany.com",
                        "verified": true
                    }
                ]
            }

+ Request Attempt to get all users when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to get all users without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Register a new user [POST]

#### Input
| Property        | Description                              | Type    | Mandatory |
| :-------        | :----------                              | :---    | :-------- |
| email           | Contact email address                    | string  | yes       |
| password        | User password (API will run under https) | string  | yes       |
| agreed_to_terms | User has agreed to Terms & Conditions    | boolean | yes       |
| first_name      | The users first name                     | string  | no        |
| last_name       | The users last name                      | string  | no        |
| phone           | Contact phone number                     | string  | no        |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The new user              | object |

+ Request Register a new User (application/json)

    + Headers

            Accept: application/json

    + Body

            {
                "first_name": "John",
                "last_name": "Bull",
                "phone": "+44 207 123 4567",
                "email": "john.bull@mycompany.com",
                "password": "3832j942cu2d"
                "agreed_to_terms": true
            }

+ Response 200 (application/json; charset=UTF-8)

            {
                "status": 200,
                "data": {
                    "first_name": "John",
                    "last_name": "Bull",
                    "phone": "+44 207 123 4567",
                    "email": "john.bull@mycompany.com",
                    "agreed_to_terms": true
                    "verified": false
                }
            }


+ Request Attempt to re-register an already existing user (application/json)

    + Headers

            Accept: application/json

    + Body

            {
                "first_name": "John",
                "last_name": "Bull",
                "phone": "+44 207 123 4567",
                "email": "john.bull@mycompany.com",
                "password": "3832j942cu2d"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "User with email jonh.bull@mycompany.com already exists"
                    }
                ]
            }


+ Request Attempt to register with missing password and invalid email (application/json)

    + Headers

            Accept: application/json

    + Body

            {
                "first_name": "John",
                "last_name": "Bull",
                "company": "mycompany",
                "phone": "+44 207 123 4567",
                "email": "this.is.an.invalid.email",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide email and password"
                    }
                ]
            }

## User Resource [/v1/accounts/users/{user_id}]

+ Parameters
    + user_id (required, string, `user1`)  ... ID for the user

### Get a user [GET]

#### Authorization
Logged in

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The user                  | object |


+ Request Get a user (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "first_name": "John",
                    "last_name": "Bull",
                    "company": "mycompany",
                    "phone": "+44 207 123 4567",
                    "email": "john@mycompany.com",
                    "verified": true
                }
            }


+ Request Get a user that does not exist (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

+ Request Attempt get a user when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt get a user without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Update user [PUT]

#### Authorization
Logged in

#### Input
| Property        | Description                              | Type    | Mandatory |
| :-------        | :----------                              | :---    | :-------- |
| email           | Contact email address                    | string  | no        |
| password        | User password (API will run under https) | string  | no        |
| agreed_to_terms | User has agreed to Terms & Conditions    | boolean | no        |
| first_name      | The users first name                     | string  | no        |
| last_name       | The users last name                      | string  | no        |
| phone           | Contact phone number                     | string  | no        |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The updated user          | object |

+ Request Update email (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "email": "new_email@mycompany.com"
            }

+   Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "first_name": "John",
                    "last_name": "Bull",
                    "email": "new_email@mycompany.com",
                    "verified": true
                }
            }


+ Request Update email that already exists (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "email": "new_email@mycompany.com"
            }

+   Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "User with email new_email@mycompany.com already exists"
                    }
                ]
            }

+ Request Attempt to update user when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to update user without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Delete user [DELETE]

#### Authorization
Logged in

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Operation result          | object |

##### Operation result
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| message  | A message describing the outcome | string |

+ Request Delete a user (application/json)
    + Headers

            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "message": "user deleted"
                }
            }


+ Request Attempt to delete user when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to delete user without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

+ Request Attempt to delete a user with invalid user ID (application/json)

    + Headers

            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

## User Verification Resource [/v1/accounts/users/{user_id}/verify]

When you register with the service, you will be sent a verification email to the email address you signed up with.
This email will contain a 'verification hash', which can be used to verify your account.

+ Parameters
    + user_id (required, string, `user1`)  ... ID of the user

### Verify user [PUT]

#### Input
| Property          | Description              | Type   | Mandatory |
| :-------          | :----------              | :---   | :-------- |
| verification_hash | User's verification hash | string | yes       |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The user                  | object |


+ Request verify user (application/json)
    + Headers

            Accept: application/json

    + Body

            {
                "verification_hash": "1234567890"
            }

+   Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "first_name": "John",
                    "last_name": "Bull",
                    "email": "new_email@mycompany.com",
                    "verified": True
                }
            }


+ Request verify user that has already been verified (application/json)

    + Headers

            Accept: application/json

    + Body

            {
                "verification_hash": "1234567890"
            }

+   Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "first_name": "John",
                    "last_name": "Bull",
                    "email": "new_email@mycompany.com",
                    "verified": True
                }
            }


+ Request verify user with invalid verification hash(application/json)
    + Headers

            Accept: application/json

    + Body

            {
                "verification_hash": "invalid_hash"
            }

+   Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "The verification hash provided does not match the hash stored.",
                        "field": "verification_hash"
                    }
                ]
            }

## User Password Resource [/v1/accounts/users/{user_id}/password]

+ Parameters
    + user_id (required, string, `user1`)  ... ID of the user

### Update user password [PUT]

#### Authorization
Logged in

#### Input
| Property  | Description              | Type   | Mandatory |
| :-------  | :----------              | :---   | :-------- |
| previous  | User's previous password | string | yes       |
| password  | User's new password      | string | yes       |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Operation result          | object |

##### Operation result
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| message  | A message describing the outcome | number |

+ Request Update password (application/json)
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "previous": "Password1",
                "password": "Password2"
            }

+   Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "message": "password changed"
                }
            }


+ Request Update invalid password (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "previous": "Password1",
                "password": "P"
            }

+   Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "password must be between 3 and 128 characters"
                    }
                ]
            }


+ Request Update password with invalid previous password (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "previous": "Password",
                "password": "Password2"
            }

+   Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide valid credentials"
                    }
                ]
            }

+ Request Attempt to update password when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to update password without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

## User Roles resource [/v1/accounts/users/{user_id}/roles]

+ Parameters
    + user_id (required, string, `user1`)  ... ID of the user

### Get all organisation-roles [GET]

#### Authorization
Logged in

#### Output
| Property | Description                        | Type   |
| :------- | :----------                        | :---   |
| status   | The status of the request          | number |
| data     | Array of organisation-role objects | array  |

#### Organisation-role object
| Property        | Description        | Type   |
| :-------        | :----------        | :---   |
| organisation_id | Organisation ID    | string |
| role            | Role Object        | object |
| join_state      | Join state of join | string |

+ Request all organisation-roles (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                    "organisation_id": "global",
                    "role": {
                            "name": "User",
                            "id": "user"
                            },
                    "join_state": "approved"
                    },
                    {
                    "organisation_id": "org1",
                    "role": {
                            "name": "Admin",
                            "id": "admin"
                            },
                    "join_state": "approved"
                    }
                ]
            }


+ Request all organisation-roles with invalid user id (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Invalid 'user_id'"
                    }
                ]
            }

+ Request Attempt to get organisation-roles when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to get organisation-roles without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Set global role for user [POST]

#### Authorization
Logged in as System Administrator

#### Input
| Property  | Description   | Type   | Mandatory |
| :-------  | :----------   | :---   | :-------- |
| role_id   | Id of role    | string | yes       |

#### Output
| Property | Description                    | Type   |
| :------- | :----------                    | :---   |
| status   | The status of the request      | number |
| data     | User object with updated roles | object |

+ Request update global role (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "role_id": "admin"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "first_name": "John",
                    "last_name": "Bull",
                    "email": "new_email@mycompany.com",
                    "verified": True,
                    "organisations": {
                        "global": {
                            "join_state": "approved",
                            "role": "admin"
                        }
                    }
                }
            }


+ Request update invalid global role (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "role_id": "invalid_role"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts:,
                        "message": "Invalid Role id"
                    }
                ]
            }

+ Request Attempt to update global role when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to update global role without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

# Group Links

## Links resource [/v1/accounts/links]

#### Organisation-link object
| Property        | Description        | Type   |
| :-------        | :----------        | :---   |
| organisation_id | Organisation ID    | string |
| link            | Link URL           | url    |


### Get organisations Reference links [POST]
Get the reference links for all organisations. The URLs can be used to find licensing options for an offer not found in a repository.

#### Input
| Property       | Description                      | Type   | Mandatory |
| :-------       | :----------                      | :---   | :---      |
| source_id      | The ID of the asset              | string | yes       |
| source_id_type | The type of the asset            | string | yes       |

#### Output
| Property | Description                        | Type   |
| :------- | :----------                        | :---   |
| status   | The status of the request          | number |
| data     | Array of organisation-link objects | array |


+ Request all organisations' links

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "organisation_id": "exampleco",
                        "link": "https://exampleco.com/asset1"
                    },
                    {
                        "organisation_id": "testco",
                        "link": "https://testco.com/asset1"
                    },
                ]
            }

# Group Organisations

## Organisations resource [/v1/accounts/organisations{?state}]

### Get all organisations [GET]

#### Authorization
Logged in

#### Output
| Property | Description                   | Type   |
| :------- | :----------                   | :---   |
| status   | The status of the request     | number |
| data     | Array of organisation objects | array  |

+ Parameters
    + state (optional, enum[string])
        State of the organisation
        + Members
            + `approved`
            + `pending`
            + `rejected`

+ Request all organisations

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "id": "4abf6deef518043137abeefb0d005f66",
                        "name": "an organisation",
                        "state": "approved"
                    },
                    {
                        "id": "5abf6deef518043137abeefb0d005f66",
                        "name": "another organisation",
                        "state: "pending"
                    }
                ]
            }

+ Request Attempt get organisations when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to get organisations without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Register a new organisation [POST]
Will register a new organisation. By default the state of the organisation will be 'pending'.

#### Authorization
Logged in

#### Input
| Property            | Description                                        | Type   | Mandatory |
| :-------            | :-----------------------                           | :---   | :-------- |
| name                | name of the organisation                           | string | yes       |
| description         | Description                                        | string | no        |
| address             | Address                                            | string | no        |
| phone               | Phone                                              | string | no        |
| email               | Email                                              | email  | no        |
| website             | Website                                            | string | no        |
| facebook            | Facebook page                                      | string | no        |
| twitter             | Twitter handle                                     | string | no        |
| google+             | Google+ account                                    | string | no        |
| instagram           | Instagram account                                  | string | no        |
| youtube             | Youtube page                                       | string | no        |
| linkedin            | Linkedin page                                      | string | no        |
| myspace             | MySpace page                                       | string | no        |
| reference_links     | Object of reference link urls for organisation     | object | no        |
| modal_header_text   | Text to display in header of Licence Modal popup   | string | no        |
| modal_footer_text   | Text to display in footer of Licence Modal popup   | string | no        |
| modal_link_text     | Text to display in link of Licence Modal popup     | string | no        |
| modal_link_url      | Url to link to in link of Licence Modal popup      | url    | no        |
| star_rating         | 1-5 Rating of Organisation                         | number | no        |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The organisation object   | object |

+ Request Register a new organisation (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo organisation"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "4abf6deef518043137abeefb0d005f66",
                    "name": "demo organisation",
                    "state: "pending"
                }
            }


+ Request Attempt to register an organisation with an invalid name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": ""
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Organisation name"
                    }
                ]
            }


+ Request Attempt to register an organisation with an already existing name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "already existing organisation name"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Organisation with name 'already existing organisation name' already exists"
                    }
                ]
            }


+ Request Attempt to register a new organisation when not authenticated (application/json)

    + Body

            {
                "name": "demo organisation"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to register a new organisation without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

## Organisation resource [/v1/accounts/organisations/{organisation_id}]

+ Parameters
    + organisation_id (required, string, `org1`)  ... ID of the organisation

### Get organisation [GET]
Get an organisation

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The organisation object   | object |

+ Request An organisation

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "org1",
                    "name": "an organisation",
                    "state: "approved"
                }
            }


+ Request An invalid organisation

    + Headers

            Accept: application/json

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

### Update organisation [PUT]
Update an organisation

#### Authorization

###### Organisation is Approved
Logged in as Organisation Administrator or System Administrator

###### Organisation is not Approved
Logged in as System Administrator

#### Input
| Property            | Description                                        | Type   | Mandatory |
| :-------            | :-----------------------                           | :---   | :-------- |
| name                | name of the organisation                           | string | no        |
| state               | Organisation State                                 | string | no        |
| description         | Description                                        | string | no        |
| address             | Address                                            | string | no        |
| phone               | Phone                                              | string | no        |
| email               | Email                                              | email  | no        |
| website             | Website                                            | string | no        |
| facebook            | Facebook page                                      | string | no        |
| twitter             | Twitter handle                                     | string | no        |
| google+             | Google+ account                                    | string | no        |
| instagram           | Instagram account                                  | string | no        |
| youtube             | Youtube page                                       | string | no        |
| linkedin            | Linkedin page                                      | string | no        |
| myspace             | MySpace page                                       | string | no        |
| reference_links     | Object of reference link urls for organisation     | object | no        |
| modal_header_text   | Text to display in header of Licence Modal popup   | string | no        |
| modal_footer_text   | Text to display in footer of Licence Modal popup   | string | no        |
| modal_link_text     | Text to display in link of Licence Modal popup     | string | no        |
| modal_link_url      | Url to link to in link of Licence Modal popup      | url    | no        |
| star_rating         | 1-5 Rating of Organisation                         | number | no        |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The organisation object   | object |

+ Request update an organisation (application/json)
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "an organisation"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "org1",
                    "name": "an organisation",
                    "state": "approved"
                }
            }


+ Request Attempt to update an organisation with an invalid name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": ""
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Organisation name"
                    }
                ]
            }


+ Request Attempt to update an organisation with an already existing name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "already existing organisation name"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Organisation with such name already exists"
                    }
                ]
            }


+ Request Attempt to update a new organisation when not authenticated (application/json)

    + Body

            {
                "name": "demo organisation"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to update a field with insufficient authentication (application/json)
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "state": "approved"
            }

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action"
                    }
                ]
            }


+ Request update an invalid organisation ID (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "state": "approved"
            }

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

### Delete organisation [DELETE]

#### Authorization

###### Organisation is Approved
Logged in as Organisation Administrator or System Administrator

###### Organisation is not Approved
Logged in as System Administrator

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Operation result          | object |

##### Operation result
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| message  | A message describing the outcome | number |

+ Request Delete an organisation
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "message": "organisation deleted"
                }
            }


+ Request Attempt to delete an organisation when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to delete an organisation with insufficient authentication
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "state": "approved"
            }

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action"
                    }
                ]
            }


+ Request Attempt to delete an invalid organisation ID
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

## Organisation links resource [/v1/accounts/organisations/{organisation_id}/links]

+ Parameters
    + organisation_id (required, string, `org1`)  -- ID of the organisation

### Get organisation reference links [POST]
Query for the reference links for an organisation. The URLs can be used to find licensing options for an offer not found in a repository.

#### Input
| Property       | Description                      | Type   | Mandatory |
| :-------       | :----------                      | :---   | :---      |
| source_id      | The ID of the asset              | string | yes       |
| source_id_type | The type of the asset            | string | yes       |

#### Output
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| status   | The status of the request        | number |
| data     | The organisation's link url      | url    |

+ Request An organisation's reference links

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": "https://exampleco.com/asset1"
            }

# Group Organisations for User

## User-Organisation object
| Property   | Description                  |
| :-------   | :----------                  |
| id         | Organisation ID              |
| name       | Organisation name            |
| state      | Organisation State           |
| join_state | User-Organisation Join State |
| role       | User-Organisation Role       |

## Organisations for User resource [/v1/accounts/users/{user_id}/organisations{?join_state}]

+ Parameters
    + user_id (required, string, `user1`) ... Id of the user.
    + join_state (optional, string)
        State of the user-organisation join
        + Members
            + `approved`
            + `pending`
            + `rejected`

### Get organisations user has joined [GET]

#### Authorization
Logged in

#### Output
| Property | Description                        | Type   |
| :------- | :----------                        | :---   |
| status   | The status of the request          | number |
| data     | Array of User-Organisation objects | array  |

+ Parameters
    + join_state (optional, string)
        State of the user-organisation join
        + Members
            + `approved`
            + `pending`
            + `rejected`

+ Request Organisations for a User

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                    "id": "4abf6deef518043137abeefb0d005f66",
                    "name": "example organisation",
                    "role": "user",
                    "join_state": "approved"
                    },
                    {
                    "id": "123deef518043137abeefb012305f66",
                    "name": "another organisation",
                    "join_state": "pending"
                    }
                ]
            }

+ Request Attempt to get organisations for user when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to get organisations for user without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Join Organisation [POST]
Will create a user to an organisation relationship by providing user id and organisation id.
By default the state of the join will be 'pending'.

#### Authorization
Logged in

#### Input
|Property       |Description           |Type  |Mandatory|
|:--------------|:---------------------|:-----|:--------|
|organisation_id|id of the organisation|string|yes      |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The updated user          | object |

+ Request Create User-Organisation relationship (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "organisation_id": "org1",
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "email": "user@example.com",
                    "organisations": {
                        "global": {
                            "role": "user",
                            "join_state": "approved"
                        },
                        "org1": {
                            "role": "user",
                            "join_state": "pending"
                        }
                    },
                    "verified": true
                }
            }


+ Request Attempt to create User-Organisation relationship with an invalid user_id (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "organisation_id": "4abf6deef518043137abeefb0d005f66",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide valid user_id"
                    }
                ]
            }


+ Request Attempt to create User-Organisation relationship with an invalid organisation_id (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "organisation_id": "invalid org id",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide valid organisation_id"
                    }
                ]
            }


+ Request Attempt to create User-Organisation relationship with an unapproved organisation (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "organisation_id": "invalid org id",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide valid organisation_id"
                    }
                ]
            }


+ Request Attempt to create User-Organisation relationship when not authenticated (application/json)

    + Body

            {
                "organisation_id": "4abf6deef518043137abeefb0d005f66",
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to create User-Organisation relationship without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

## Organisation for User resource [/v1/accounts/users/{user_id}/organisations/{organisation_id}]

+ Parameters
    + user_id (required, string, `user1`) ... Id of the user
    + organisation_id (required, string, `org1`) ... Id of the organisation

### Get an organisation a user has joined [GET]

#### Authorization
Logged in

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | User-Organisation Object  | object |


+ Request an existing Organisation for a User

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "org1",
                    "name": "example organisation",
                    "role": "user",
                     "join_state": "approved"
                 }
            }


+ Request non-existing User-Organisation relationship

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "user-organisation relationship does not exist"
                    }
                ]
            }

+ Request Attempt to get Organisation for User when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to get Organisation for User without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Update the join-state or access role for a user for an organisation [PUT]

#### Authorization
Logged in as Organisation Administrator or System Administrator

#### Input
| Property   | Description        | Type   | Mandatory |
| :--------- | :----------------- | :---   | :-------- |
| join_state | The new join state | string | no        |
| role_id    | Id of role         | string | no        |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The updated user          | object |

+ Request update the state of a join between user and organisation (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "join_state": "approved"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "email": "user@example.com",
                    "organisations": {
                        "global": {
                            "role": "user",
                            "join_state": "approved"
                        },
                        "org1": {
                            "role": "user",
                            "join_state": "approved"
                        }
                    }
                }
            }


+ Request update the role of a user for an organisation (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "role_id": "administrator"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "email": "user@example.com",
                    "organisations": {
                        "global": {
                            "role": "user",
                            "join_state": "approved"
                        },
                        "org1": {
                            "role": "administrator",
                            "join_state": "approved"
                        }
                    }
                }
            }


+ Request update the join-state and role of a user for an organisation (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "join_state": "approved",
                "role_id": "administrator"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "email": "user@example.com",
                    "organisations": {
                        "global": {
                            "role": "user",
                            "join_state": "approved"
                        },
                        "org1": {
                            "role": "administrator",
                            "join_state": "approved"
                        }
                    }
                }
            }


+ Request update with no join_state or role_id (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {}

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "join_state or role_id is required"
                    }
                ]
            }


+ Request update when not authenticated (application/json)

    + Body

            {
                "join_state": "approved"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request update with insufficient authentication (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "join_state": "approved"
            }

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action"
                    }
                ]
            }

### Remove an organisation from a user [DELETE]

#### Authorization
Logged in as User being updated, Organisation Administrator or System Administrator

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The updated user object   | object |

+ Request Remove an organisation from a user

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "user1",
                    "email": "jonh.bull@mycompany.com",
                    "verified": true,
                    "organisations": {
                        "global": {
                            "role": "user",
                            "join_state": "approved"
                        }
                    }
                }
            }


+ Request Attempt to remove a user's organisation when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to remove a user's organisation with insufficient authorization

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action"
                    }
                ]
            }


+ Request An invalid user ID (application/json)
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }


+ Request An invalid organisation ID
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

# Group Services

## Services Resource [/v1/accounts/organisations/{organisation_id}/services]

+ Parameters
    + organisation_id (required, string, `org1`) ... Id of the organisation

### Register a new service [POST]
Will register a new service for an organisation using its name and a unique location.

#### Authorization
Logged in as User belonging to Organisation or System Administrator

#### Input
|Property       |Description                                     |Type  |Mandatory|
|:--------------|:-----------------------------------------------|:-----|:--------|
|name           |Name of the service                             |string|yes      |
|location       |Location of the service (IP address or HTTP URL)|string|yes      |
|service_type   |The service type                                |string|yes      |
|permissions    |Access control permissions for service          |array |no       |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service               | object |


+ Request Register a new service (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "service1",
                    "name": "demo service",
                    "created_by": "username",
                    "state": "pending",
                    "location": "http://demo.service.com:7777/v1",
                    "service_type": "repository",
                    "organisation_id": "org1",
                    "permissions": [
                       {"type": "organisation_id", "value": "org1", "permission": "rw"}
                    ]
                }
            }


+ Request Register a new service with permissions(application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "repository",
                "permissions": [
                    {"type": "service_type", "value": "onboarding", "permission": "r"}
                ]
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "id": "service1",
                    "name": "demo service",
                    "created_by": "username",
                    "state": "pending",
                    "location": "http://demo.service.com:7777/v1",
                    "service_type": "repository",
                    "organisation_id": "org1",
                    "permissions": [
                        {"type": "service_type", "value": "onboarding", "permission": "r"}
                    ]
                }
            }


+ Request Attempt to register a service with an invalid organisation (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not Found"
                    }
                ]
            }


+ Request Attempt to register a service with an invalid service_type (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "this is an invalid service type",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Service service_type"
                    }
                ]
            }


+ Request Attempt to register a service with a missing service_type (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://demo.service.com:7777/v1",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Service service_type"
                    }
                ]
            }


+ Request Attempt to register a service with an invalid location (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "this.is.an.invalid.location",
                "service_type": "repository",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Service Location"
                    }
                ]
            }


+ Request Attempt to register a service with an already existing location (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://already.existing.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 400 (application/json; charset=UTF-8)


    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Service with location 'http://already.existing.service.com:7777/v1' already exists"
                    }
                ]
            }


+ Request Attempt to register a service with an already existing name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "existing name",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Service with name 'existing name' already exists"
                    }
                ]
            }


+ Request Attempt to register a new service when not authenticated (application/json)

    + Body

            {
                "name": "demo service",
                "location": "http://already.existing.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to register a new service without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://already.existing.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

## Service Query Resource [/v1/accounts/services{?organisation_id}{?type}]

+ Parameters
    + organisation_id (required, string)  ... ID of the organisation
    + type (optional, enum[string])
        Service type
        + Members
            + `external`
            + `authorisation`
            + `identity`
            + `index`
            + `onboarding`
            + `query`
            + `repository`
            + `resolution`
            + `transformation`

### Get services [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Array of services         | array  |


+ Request Services

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "id": "service1",
                        "name": "demo service",
                        "created_by": "username",
                        "state": "pending",
                        "location": "http://demo.service.com:7777/v1",
                        "service_type": "repository",
                        "organisation_id": "org1",
                        "permissions": [
                            {"type": "organisation_id", "value": "org1", "permission": "r"}
                        ]
                    }
                ]
            }


+ Request Services for an invalid organisation

    + Headers

            Accept: application/json

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

## Service Types Resource [/v1/accounts/services/types]

### Services types [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The list of service types | array  |

+ Request a list of valid services types (application/json)

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                  "authorisation",
                  "identity",
                  "index",
                  "onboarding",
                  "query",
                  "repository",
                  "resolution",
                  "transformation"
                ]
            }

## Service Resource [/v1/accounts/services/{service_id}]

+ Parameters
    + service_id (required, string, `service1`)  ... ID of the service

### Get a service [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service               | object |

+ Request Service

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data":
                    {
                        "id": "service1",
                        "name": "demo service",
                        "created_by": "username",
                        "state": "pending",
                        "location": "http://demo.service.com:7777/v1",
                        "service_type": "repository",
                        "organisation_id": "org1",
                        "permissions": [
                            {"type": "organisation_id", "value": "org1", "permission": "r"}
                        ]
                    }

            }


+ Request a service that does not exist

    + Headers

            Accept: application/json

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

### Update service [PUT]

#### Authorization
Logged in as User who created Service, Organisation Administrator or System Administrator

#### Input
|Property       |Description                                     |Type  |Mandatory|
|:--------------|:-----------------------------------------------|:-----|:--------|
|name           |Name of the service                             |string|no       |
|location       |Location of the service (IP address or HTTP URL)|string|no       |
|service_type   |The service type                                |string|no       |
|permissions    |Access control permissions for service          |array |no       |
|state          |State of service                                |string|no       |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service               | object |

+ Request Update a service (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "new service name",
                "location": "http://demo.service.com:7777/v1"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "id": "service1",
                        "name": "new service name",
                        "created_by": "username",
                        "state": "pending",
                        "location": "http://demo.service.com:7777/v1",
                        "service_type": "repository",
                        "organisation_id": "org1",
                        "permissions": [
                            {"type": "organisation_id", "value": "org1", "permission": "r"}
                        ]
                    }
                ]
            }


+ Request Attempt to update a organisation of a service (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "repository",
                "organisation_id": "org id"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "field": "organisation_id",
                        "message": "Extra keys not allowed",
                        "source": "accounts"
                    }
                ]
            }


+ Request Attempt to update a service with an invalid service_type (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "this is an invalid service type",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Service service_type"
                    }
                ]
            }


+ Request Attempt to update a service's service_type when having insufficient permissions (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "service_type": "index",
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "field": "service_type",
                        "message": "User cannot update 'service_type' field for service"
                    }
                ]
            }


+ Request Attempt to update a service with an invalid location (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "this.is.an.invalid.location",
                "service_type": "repository"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Service Location"
                    }
                ]
            }


+ Request Attempt to update a service with an already existing location (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://already.existing.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Service with location 'http://already.existing.service.com:7777/v1' already exists"
                    }
                ]
            }


+ Request Attempt to update a service with an already existing name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "existing name",
                "location": "http://demo.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Service with name 'existing name' already exists"
                    }
                ]
            }


+ Request Attempt to update a service when not authenticated (application/json)

    + Body

            {
                "name": "demo service",
                "location": "http://already.existing.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to update a service without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "location": "http://already.existing.service.com:7777/v1",
                "service_type": "repository"
            }

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Delete service [DELETE]

#### Authorization
Logged in as User who created Service, Organisation Administrator or System Administrator

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Operation result          | object |

##### Operation result
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| message  | A message describing the outcome | number |

+ Request Delete a service
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "message": "service deleted"
                }
            }


+ Request Attempt to delete a service when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to delete a service without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

+ Request Attempt to delete an invalid service ID
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

## Service Secrets Resource [/v1/accounts/services/{service_id}/secrets]

+ Parameters
    + service_id (required, string, `service1`)  ... ID of the service

### Get all service secrets [GET]

#### Authorization

###### Service is Approved
Logged in as User belonging to Organisation or System Administrator

###### Service is not Approved
Cannot access

#### Output
| Property | Description                 | Type   |
| :------- | :----------                 | :---   |
| status   | The status of the request   | number |
| data     | List of secrets for service | array  |

+ Request Get all secrets

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    "2lpfpkpzsrv4hxqrhfjh0thmmi69sa",
                    "7b6gmbzw2pagraaz07a3p3njxt4eumk"
                ]
            }


+ Request Attempt to get service secrets when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to get service secrets without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Create new service secret [POST]

#### Authorization

###### Service is Approved
Logged in as User who created Service, Organisation Administrator or System Administrator

###### Service is not Approved
Cannot access

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The new service secret    | string |

+ Request create new service secret

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": "2lpfpkpzsrv4hxqrhfjh0thmmi69sa"
            }


+ Request Attempt to create service secret when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to create service secret without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Delete all secrets for service [DELETE]

#### Authorization

###### Service is Approved
Logged in as User who created Service, Organisation Administrator or System Administrator

###### Service is not Approved
Cannot access

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Operation result          | object |

##### Operation result
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| message  | A message describing the outcome | number |

+ Request delete service secrets

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "message": "secret credentials deleted"
                }
            }


+ Request Attempt to delete service secrets when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to delete service secrets without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

## Service Secret resource [/v1/accounts/services/{service_id}/secrets/{secret}]

+ Parameters
    + service_id (required, string, `service1`)  ... ID of the service
    + secret (required, string, `2lpfpkpzsrv4hxqrhfjh0thmmi69sa`)  ... Service secret to delete

### Delete Service Secret [DELETE]

#### Authorization

###### Service is Approved
Logged in as User who created Service, Organisation Administrator or System Administrator

###### Service is not Approved
Cannot access

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Operation result          | object |

##### Operation result
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| message  | A message describing the outcome | number |

+ Request delete service secret

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "message": "secret credential deleted"
                }
            }


+ Request Attempt to delete service secret when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to delete service secret without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

# Group Repository

## Repositories By Organisation Resource [/v1/accounts/organisations/{organisation_id}/repositories]

+ Parameters
    + organisation_id (required, string, `org1`)  ... ID of the organisation

### Get repositories for an organisation [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Array of repositories     | array  |

+ Request Repositories for an organisation

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "id": "repository1",
                        "name": "demo repository",
                        "state": "pending",
                        "created_by": "a user ID",
                        "organisation_id": "org1",
                        "permissions": [
                            {"type": "organisation_id", "value": "org1", "permission": "w"}
                        ],
                        "service": {
                          "id": "service1",
                          "service_type": "repository",
                          "organisation_id": "org1",
                          "name": "demo service",
                          "created_by": "a user ID",
                          "location": "https://localhost/",
                          "permissions": []
                        }
                    }
                ]
            }


+ Request Repositories for an invalid organisation

    + Headers

            Accept: application/json

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not found"
                    }
                ]
            }

### Register a new repository [POST]
Will register a new repository for an organisation within a repository service

#### Authorization
Logged in as User belonging to Organisation or System Administrator

#### Input
| Property        | Description                                      | Type   | Mandatory |
| :-------------- | :----------------------------------------------- | :----- | :-------- |
| name            | Name of the repository                           | string | yes       |
| service_id      | A repository service ID                          | string | yes       |
| permissions     | Array of permisisons                             | array  | no        |


#### Output
| Property | Description               | Type   |
| :------- | :------------------------ | :---   |
| status   | The status of the request | number |
| data     | The repository            | object |

+ Request Register a new repository (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "service_id": "service1",
                "permissions": [{"type": "organisation_id", "value": "org1", "permission": "w"},
                                {"type": "organisation_id", "value": "another_organisation", "permission": "w"}]
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                  "id": "repository1",
                  "name": "demo repository",
                  "state": "pending",
                  "created_by": "a user ID",
                  "organisation_id": "org1",
                  "permissions": [
                        {"type": "organisation_id", "value": "org1", "permission": "w"},
                        {"type": "organisation_id", "value": "another_organisation", "permission": "w"}
                  ],
                    "service": {
                      "id": "service1",
                      "service_type": "repository",
                      "organisation_id": "another_organisation",
                      "name": "demo service",
                      "created_by": "a user ID",
                      "location": "https://localhost/",
                      "permissions": []
                    }
                }
            }


+ Request Attempt to register a repository with an invalid organisation (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "service_id": "service1"
            }

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not Found"
                    }
                ]
            }


+ Request Attempt to register a repository with an invalid service (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "service_id": "invalid_service_id"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Service ID"
                    }
                ]
            }


+ Request Attempt to register a repository with a service that is not a repository(application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo service",
                "service_id": "index_service_id"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Service "index_service_id" is not a repository"
                    }
                ]
            }


+ Request Attempt to register a repository with an existing name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "existing name",
                "service_id": "service1"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Repository with name 'existing name' already exists"
                    }
                ]
            }


+ Request Attempt to register a new repository when not authenticated (application/json)

    + Body

            {
                "name": "existing name",
                "service_id": "service1"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to register a new repository with insufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "existing name",
                "service_id": "service1"
            }

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

## Repositories Resource [/v1/accounts/repositories]

### Get repositories [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Array of repositories     | array  |

+ Request Repositories

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "id": "repository1",
                        "name": "demo repository",
                        "default": true,
                        "state": "pending",
                        "created_by": "a user ID",
                        "organisation_id": "org1",
                        "permissions": [
                            {"type": "organisation_id", "value": "org1", "permission": "w"}
                        ],
                        "service": {
                          "id": "service1",
                          "service_type": "repository",
                          "organisation_id": "org1",
                          "name": "demo service",
                          "created_by": "a user ID",
                          "location": "https://localhost/",
                          "permissions": []
                        }
                    }
                ]
            }

## Repository Resource [/v1/accounts/repositories/{repository_id}]

+ Parameters
    + repository_id (required, string, `repository1`)  ... ID of the repository

### Get a repository [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The repository            | object |

+ Request Repository

    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                  "id": "repository1",
                  "name": "demo repository",
                  "created_by": "a user ID",
                  "organisation_id": "org1",
                  "permissions": [{"type": "organisation_id", "value": org1", "permission": "w"}],
                    "service": {
                      "id": "service1",
                      "service_type": "repository",
                      "organisation_id": "another_org",
                      "name": "demo service",
                      "created_by": "a user ID",
                      "location": "https://localhost/",
                      "permissions": []
                    }
                }
            }


+ Request a repository that does not exist

    + Headers

            Accept: application/json

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not Found"
                    }
                ]
            }

### Update repository [PUT]

#### Authorization
Logged in as User who created Repository, Repository Organisation Administrator, Service Organisation Administrator or System Administrator

#### Input
| Property        | Description                                      | Type   | Mandatory |
| :-------------- | :----------------------------------------------- | :----- | :-------- |
| name            | Name of the repository                           | string | no        |
| service_id      | The service ID                                   | string | no        |
| organisation_id | The organisation ID                              | string | no        |
| permission      | Array of permissions                             | array  | no        |
| state           | Repository approval state                        | string | no        |

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The repository            | object |

+ Request Update a repository (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo repository",
                "service_id": "service1",
                "organisation_id": "org1"
            }

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                  "id": "repository1",
                  "name": "demo repository",
                  "created_by": "a user ID",
                  "organisation_id": "org1",
                  "permissions": [{"type": "organisation_id", "value": "org1", "permission": "w"}],
                  "service": {
                      "id": "service1",
                      "service_type": "repository",
                      "organisation_id": "org1",
                      "name": "demo service",
                      "created_by": "a user ID",
                      "location": "https://localhost/",
                      "permissions": []
                    }
                }
            }


+ Request Attempt to update a repository with an invalid service_id (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo repository",
                "service_id": "this service id does not exist",
                "organisation_id": "org1"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Please provide a valid Service ID"
                    }
                ]
            }


+ Request Attempt to update a repository with an existing name (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "existing name",
                "service_id": "service1",
                "organisation_id": "org1"
            }

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": 400,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Repository with name 'existing name' already exists"
                    }
                ]
            }


+ Request Attempt to update a repository when not authenticated (application/json)

    + Body

            {
                "name": "demo repository",
                "service_id": "service1",
                "organisation_id": "org1"
            }

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }


+ Request Attempt to update a repository with insufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

    + Body

            {
                "name": "demo repository",
                "service_id": "service1",
                "organisation_id": "org1"
            }

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

### Delete repository [DELETE]

#### Authorization
Logged in as User who created Repository, Repository Organisation Administrator, Service Organisation Administrator or System Administrator

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | Operation result          | object |

##### Operation result
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| message  | A message describing the outcome | number |

+ Request Delete a repository that is not approved
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "message": "Repository deleted"
                }
            }


+ Request Delete a repository that is approved
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": {
                    "source": "accounts",
                    "message": "Cannot delete a repository that has been approved"
                }
            }


+ Request Attempt to delete a repository when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to delete a repository without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }

+ Request Attempt to delete an invalid repository ID
    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": 404,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Not Found"
                    }
                ]
            }

# Group Role

## Roles Resource [/v1/accounts/roles]

### Get all roles [GET]

#### Authorization
Logged in

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | List of role objects      | array  |

+ Request all Roles

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "id": "001",
                        "name": "role1"
                    },
                    {
                        "id": "002",
                        "name": "role2"
                    },
                    {
                        "id": "003",
                        "name": "role3"
                    }
                ]
            }

+ Request Attempt to get roles when not authenticated

    + Headers

            Accept: application/json

+ Response 401 (application/json; charset=UTF-8)

    + Body

            {
                "status": 401,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token not in Authorization header"
                    }
                ]
            }

+ Request Attempt to get roles without sufficient authorization (application/json)

    + Headers

            Accept: application/json
            Authorization: [TOKEN]

+ Response 403 (application/json; charset=UTF-8)

    + Body

            {
                "status": 403,
                "errors": [
                    {
                        "source": "accounts",
                        "message": "Token is not authorised for this action: d419d20c-e14f-4b52-98d6-0e8717a68f28"
                    }
                ]
            }
