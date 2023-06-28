
# Fuse Blog

The social platform Fuse Blog is an inspiring and dynamic online community where users can share their ideas, thoughts and experiences with other members. Our goal is to provide a convenient and attractive platform for the exchange of information and interaction between users.


## Authors

- [@robiya07](https://www.github.com/robiya07)


## Features

- Reading Other Users' Posts: Users have the ability to view posts created by other members and get inspired, informed, or simply entertained by content created by the community

- User-created posts: We encourage active user participation by giving them the opportunity to create their own posts. This means that each member can become an author and share their ideas, impressions and useful information with the rest of the community

- Authentication: To ensure the security and privacy of users, our platform has implemented an authentication system. This allows users to create accounts, log in, and keep their data secure

- User Profile: Each member has their own profile where they can introduce themselves and share additional information about themselves. Users can customize their profile, upload avatars, and view their previous posts

- Post Categories (Many-to-Many): We offer a category system that allows users to categorize their posts according to different topics or interests. This makes it easier to find and filter content for users who are looking for specific information or want to find posts on a specific topic

- Changing the status of a post: The admin panel provides a function to change the status of a post. Admins can change the status of a post, such as active, canceled, or pending. This allows administrators to control the availability of posts and influence their visibility to other users

- Jumping to a post's detail page: Administrators have the ability to go directly to a post's detail page from the admin panel. This allows them to quickly view information about a particular post, including comments and interactions with the author or other contributors
## Screenshots

![Home Page](https://github.com/robiya07/fuse_blog/blob/master/medias/readme/Screenshot%20from%202023-06-28%2016-39-22.png)



![All Posts](https://github.com/robiya07/fuse_blog/blob/master/medias/readme/Screenshot%20from%202023-06-28%2016-39-28.png)



![About Page](https://github.com/robiya07/fuse_blog/blob/master/medias/readme/Screenshot%20from%202023-06-28%2016-39-37.png)



![Contact Page](https://github.com/robiya07/fuse_blog/blob/master/medias/readme/Screenshot%20from%202023-06-28%2016-39-43.png)



![Profile Page](https://github.com/robiya07/fuse_blog/blob/master/medias/readme/Screenshot%20from%202023-06-28%2016-42-44.png)



![Edit Profile Page](https://github.com/robiya07/fuse_blog/blob/master/medias/readme/Screenshot%20from%202023-06-28%2016-43-48.png)
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Create a virtual environment

```bash
  python3 -m venv .venv
```

Activate virtual environment

```bash
  . .venv/bin/activate
```

Migrate

```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
```

Install dependencies

```bash
  pip install -r requirements/base.txt
  pip install -r requirements/development.txt
  pip install -r requirements/production.txt
```

Start the server

```bash
  python3 manage.py runserver
```
