#ACL Design Notes

# Access Control Parameters

## Services

Access to a service can be restricted to:

*   Organisation by id
*   Organisation by service type (i.e. Any organisation that runs a service of that type)
*   All organisations

A service can have:

*   Read Permission (r)
*   Write Permission (w)
*   Read Write Permission(rw)
*   No permission(-)

## Buckets

Access to buckets can be restricted to:

*   Organisation by id
*   All organisations

A bucket can have:

*   Write Permission (w)
*   No permission(-)

# Access Control Hierarchy

The precedence rules for access control have been based on NTFS file access rules ([http://www.ntfs.com/ntfs-permissions-precedence.htm](http://www.ntfs.com/ntfs-permissions-precedence.htm)). However instead of a file/folder hierarchy we will use the following hierarchy:

*   All organisations
    *   Service Type
        *   Organisation Id

1.  Permissions applied directly to an organisation id (explicit permissions) will take precedence over permissions based on a service service type or all organisations.

2.  Permissions inherited from near relatives take precedence over permissions inherited from distant predecessors. (i.e: Permissions that apply to service type will take precedence over permissions applied to all organisations).

3.  If no permission level is specified for an organisation, said organisation is assumed not to have access.

### Examples

```
Service :{
   "_id": "1234",
   "organisation_id": "exampleco",
   "service_type": "repository"
```

* [{type: 'organisation\_id', value: 'exampleco', permission: 'r'}, {type: 'service\_type', value: 'repository', permission: 'w'}]: **Read Acccess**
* [{type: 'organisation\_id', value: 'hogwarts', permission: 'w'}, {type: 'service\_type', value: 'repository', permission: 'rw'}]: **Read & Write Access**
* [{type: 'organisation\_id', value: 'exampleco', permission: '-'}, {type: 'service\_type', value: 'repository', permission: 'rw'}]: **No Access**
* [{type: 'organisation\_id', value: 'hogwarts', permission: 'r'}, {type: 'service\_type', value: 'index', permission: 'w'}]: **No Access**
* [{type: 'all', value: None, permission: 'r'}, {type: 'service_type', value: 'repository', permission: 'w'}]: **Write Access**
* [{type: 'all', value: None, permission: 'r'}, {type: 'service_type', value: 'index', permission: 'w'}]: **Read Access**

# Document Structure

## Services

Access permissions for a service will be stored as part of the _Services_ document in CouchDB.

The _permissions_ key will store an array of access rule objects. Working through the list from most specific (type: 'organisation_id') to least specific type (type: 'all'), if any of the rules match, then return the permission for that rule.

```
{
   "_id": "79882e261d03790f4ebd3123a2258728",
   "_rev": "1-f7c28a105375eb169359ea5480ee7a96",
   "organisation_id": "exampleco",
   "type": "service",
   "name": "005cd23e-d9c3-4266-95a6-fdd306caf667",
   "created_by": "katie",
   "location": "http://test.com/41580bde-ce87-498d-9228-bc5e39e179b7",
   "permissions":[
       {type: 'organisation_id', value: 'exampleco', permission: 'r'}, 
       {type: 'service_type', value: 'repository', permission: 'w'}
    ]
}
```

For example, any organisations which have repository services will have write access to the above service, except for 'exampleco', who will have read access.

## Buckets

Access permissions for a bucket will be stored as part of the _Buckets_ document in CouchDB.

The _permissions_ key will store an array of access rule objects. Working through the list from most specific (type: 'organisation_id') to least specific type (type: 'all'), if any of the rules match, then return the permission for that rule.

```
{
   "_id": "79882e261d03790f4ebd3123a2258728",
   "_rev": "1-f7c28a105375eb169359ea5480ee7a96",
   "organisation_id": "exampleco",
   "name": "exampleco",
   "type": "bucket",
   "created_by": "katie",
   "state": "approved",
   "service_id": "80defa84505f48108858ab653d00855a" 
   "permissions":[
       {type: 'organisation_id', value: 'exampleco', permission: 'w'}, 
       {type: 'organisation_id', value: '4corners', permission: 'w'}
   ]
}
```

For example, any exampleco and 4corners will have write access to the above bucket.

# Defaults 

## Services

When a service is created, by default it will allow read/write access from any other service registered with the Copyright Hub. This can then be restricted via the Service UI where necessary.

## Buckets

When a bucket is created, by default it will allow write access from the organisation that the bucket belongs to. This can then be altered via the Service UI where necessary.

# Setting / Updating ACL permissions

*   Permissions for a service/bucket can be optionally set on service/bucket creation. If no permissions are provided then default ACL permissions will be set on creation. 
*   To update permissions a list of rule objects can be passed within the body of the request when performing a PUT request on /services/{service_id} or /buckets/{bucket_id}. 
*   This list of rule objects will overwrite the existing rules for a service or bucket.
*   Validation of these rules will occur within the model on update.

# Limitations

*   Access control will be limited to service-service interaction. We will not be adding access control for individual endpoints.
*   We will not be doing extra validation on dependant services. It is the responsibility of the organisation to make sure their ACL rules do not conflict between dependant services (e.g. between onboarding and repository)