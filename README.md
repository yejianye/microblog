Web application: Micro blog 
===========================
This application is a micro-blog with very basic features such as posting feed and follow a friend. My goal is to use it as an example project to test out various ideas and architectures in web backend development including
- Design abstraction layers and APIs
- Distributed cache
- NoSQL
- Database sharding
etc

The features of this simple microblog application includes
- Create a new user
- Follow/unfollow users
- Post a feed
- View friends' feeds ordered by timeline

API Spec
--------
This is the spec of end-user APIs for this microblog application. All endpoints would return JSON-formatted data. For POST requests, the parameter is passed as JSON in request body.

### User Object
A `User` object has the following attributes
- id
- username
- email
- password
- bio

### GET /users/<user-id>
Fetch a user by its id

### POST /users
Create a new user with the following args
- username
- email
- password
- bio (optional)

Both `username` and `email` needs be unique

### GET /users/<user-id>/followers
Get a list of users that follow specific user

### GET /users/<user-id>/followings
Get a list of users that specific user is following

### POST /users/<user-id>/follow/<other-id>
Follow another user with `other-id`

### POST /users/<user-id>/unfollow/<other-id>
Unfollow another user with `other-id`

### GET /users/<user-id>/feeds
Fetch feeds from specific user

### GET /users/<user-id>/friend-feeds
Fetch friend feeds for specific user

### GET /feeds/<feed-id>
Fetch a specific feed

### POST /feeds
Post a new feed
- user_id
- content

mbref:
-----
This is a naive implementation used as a baseline for other implementations.
