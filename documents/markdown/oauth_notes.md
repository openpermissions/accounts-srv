#OAuth notes

*   [use OAuth 2.0](https://tools.ietf.org/html/rfc6749)
*   [use flow for the client credentials authorization grant](https://tools.ietf.org/html/rfc6749#section-4.4)
*   [use JWT bearer access tokens](https://tools.ietf.org/html/rfc7519)
*   [use scopes to control access to resources](https://tools.ietf.org/html/rfc6749#section-3.3)

##Sequence diagram: 
![Sequence Diagram](images/oauth-seq.png "Sequence Diagram")

## Authorization Grant

The OAuth 2 spec describes a number of authorization grant flows. The client credentials grant is very simple and seems to most appropriate for machine-to-machine communication where there is not a user interactively granting access to a resource. The flow consists of the following steps:

1.  The client authenticates with the authorization server and requests a token
2.  If the client is authenticated, the authorization server responds with an access token

The client will authenticate itself using Basic authentication with a client ID (could be the service or organisation ID?) and a client secret, as described in the OAuth spec ([https://tools.ietf.org/html/rfc6749#section-4.3.2](https://tools.ietf.org/html/rfc6749#section-4.3.2)). Additionally the client will need to provide a scope parameter, which will limit the scope of the received access token (see the scopes section below).

A constraint when using the client credentials grant is that the client must be able to keep their credentials secure, but this is fine for server-side applications.

##Access Tokens

An inherent risk with bearer tokens is that a malicious actor that intercepts the token will be able to impersonate the client. The following steps will mitigate this risk:

*   All communication MUST use HTTPS
*   The token will expire after a relatively short period of time
*   The token's scope will limit the actions that can be performed with an intercepted token (e.g. a token for reading a resource cannot be used to modify the resource)

A stronger mitigation measure would be to use a MAC token ([https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-05](https://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-05)), which would require a client to use a symmetric key to prove their identity (similarly to OAuth1). MAC tokens would be more secure since an intercepted access token would be useless without gaining access to the symmetric key which is known only to the client and authorization service. But the security comes at the cost of greater complexity for the client and it would make it very difficult to delegate access to a resource (e.g. we require the ability to allow the onboarding service to add data to the repository on the client's behalf, but to do this the onboarding service would need access to the client's key). Additionally, the OAuth MAC token spec is both controversial and still a draft.

The access token will be a JSON Web Token that contains the expiry, client's organisation ID and the token's scope, and will be cryptographically signed by the authorization service. Initially, the JWT will not provide many benefits as resource owners will still need to send the token to the authorization service to verify access to the resource. However, JWTs could in the future help reduce the amount of network traffic in the authorization workflow and would cost little to implement since we already have code for using JWTs.

##Scopes

Suggested scopes are:

*   **read** - grants access to read any resource the client is permitted to read
*   **transform** - permits the client to use the transformation service
*   **write:repository_id**- a parameterised scope that grants access to write to the specified repository, e.g. "write:1234" is the scope for writing to repository 1234\. The authorization service should not provide an access token unless the client has access to the repository.

