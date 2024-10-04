## A fun pet project: a blogger web application from scratch

## Description: 
Make a blogger web application without using any 3rd web server, framework, database.

Tries not to use 3rd tools and libraries. Except for programming language built-in libraries.

This project is useful for many web developers. To show them that building a web application is simple. It consists mostly of details that we add steps by steps, according to our needs. I see many web developers are getting confused by the amounts of web frameworks, 3rd party libraries available to them, they don't even know how to do the basic without using these tools.

This project is also useful for web pentesters, bug bounty hunters. As you build this web application and its functionalities, ideas of how to attack it will frequently pop up in your head, tries to protect this web application from your own attack. 

## General ideas:
- make a web server using WebSocket library in Python
   - it listens to port 8080
- when browser calls http://localhost:8000/index or http://localhost:8000/index.html, it returns back with `<h1>hello</h1>`
- when browser calls http://localhost:8000, it returns a home page with a few hyperlinks
   - when user is not logged in, the page shows the following actions: "Articles", "Signup", "Login".
     - "Article" redirects user to a page that shows articles of all users.
     - "Signup" redirects user to a page that let user signup
     - "Login" redirects user to a page that let user login
   - when user is logged in, the page shows the following actions: "Articles", "My articles", "Add article"
     - "Article" is like above.
     - "My article" lists only articles of this user.
     - "Add article" lets users create a new article.
- access control
  - there are 2 user roles: User, Admin
  - let user signup with username & password. 
  - All signup users have User role by default. Admin user cannot be signed-up, we will hard-code him into our "passwd" file.
  - store user's username & password in a plain text file, similar to the /etc/passwd file. Don't use any SQL databases.
  - after user login, gives him an access token (how you generate this access token is up to you), user will send this access token along in every of his request. So that server can identify this user. 
  - If user has User role, when calls localhost:8080/admin, he will get 403 HTTP code and the response `<h1>unauthorized</h1>`
  - if user has Admin role, when calls localhost:8080/admin, he is responded with Admin page, this page lists title of all articles, and a "Delete" button next to each title, for admin to delete this article.
