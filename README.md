# Tool Share App
Live URL: https://toolshare-jed.herokuapp.com/

Test Username: jarnold

Test Password: password

## About This App

This application was built to encourage local community members to both share and borrow tools from those in their community. 
The idea is to eliminate the inability to buy tools when doing a single project around a home. My hope is to build up local communities
and encourage neighbors to know each other once again. Currently this app only functions properly when using USA zip codes.

### App Phase

This application is in the initial phases. Currently there are few extra features and styling is a work-in-progress. I encourage anyone
who has an interest in contributing to scroll below to learn how. 

Please feel free to leave feedback on how we can improve features and future features that you would like to see. 

### Current Features

In the initial model of this application, I wanted to make it functional without over-scoping the build. It currently allows:
- User creation
- Adding/deleting/editing tools
- Tools show up on a map and list view
- Emailing users about their specific tools

I was building the MVP, so I wanted to make sure it was truly the minimal working features before going into "extras".

## User Flow

1. When you first go to the application, you will find a landing page. This landing page will have multiple opportunities to register with
the application.
2. Once you register, you will be taken to the map where you will see content clusters of tools. Zooming in on these content clusters will 
allow you to see what tools are available in your area. The map will automatically center and zoom in once you allow location and refresh.
3. If you go to your profile, you will have multiple options. You can edit your profile, change you picture, and add/delete tools. Your 
tolls will show up according to your profile zip code. 

## MapQuest API

This application is made possible using the [MapQuest API](https://developer.mapquest.com/). The MapQuest API allows the application
a couple of unique features that would be hard to implement without it. These MapQuest features include:
- Geolocation
- An SDK
- Marker Clusters

## Technology Used

- Python (Flask)
- Jinja
- SQLAlchemy (flask-sqlalchemy)
- PostgreSQL
- JavaScript
- Bootstrap
- CSS
- HTML

## Contributing

Pull requests are welcome to contribute to this project. Each PR will be reviewed by myself or a future collaborator on this application. Follow these steps to
get this app up and running on your local machine:

**Download the code and go into the folder**
```
> git clone https://github.com/thebookofjedediah/tool_share_app.git
> cd tool_share_app
```

**Create a Virtual Environment and Enter it**
```
> python3 -m venv venv
> source venv/bin/activate
```

**Install the Requirements and Create a .env and .gitignore**
```
> pip3 install -r requirements.txt
> touch .env
> touch .gitignore
```

**Once these steps are completed, you must do a couple of things:**
1. Inside of the `.env` file, add a SECRET_KEY, MAPQUEST_CONSUMER_KEY, and a MAPQUEST_CONSUMER_SECRET variable. You can refer to the 
[MapQuest API](https://developer.mapquest.com/) to get the proper keys for MapQuest
2. Inside of the `.gitignore` file, on separate lines, add `venv`, `.env`, and `__pycache__`
3. Create a PostgreSQL Database on your local machine called `tool-share`

**Once all of the setup is complete, you can run `flask run` in your terminal to run the app.**

### Don't Know Git?
Those who are not yet familiar with Git but want to learn more about how to use it, check out these resources to dive into git workflow -
- [Git - Documentation](https://git-scm.com/doc)
- [Codecademy course](https://www.codecademy.com/learn/learn-git)
- [FCC video tutorial series](https://www.youtube.com/watch?v=vR-y_2zWrIE&list=PLWKjhJtqVAbkFiqHnNaxpOPhh9tSWMXIF)
- [How to Use Git and GitHub - FREE course on Udacity](https://www.udacity.com/course/how-to-use-git-and-github--ud775#)
- [Getting Git Right - Tutorials on Atlassian](https://www.atlassian.com/git)
- [List of useful resources & references](https://gist.github.com/eashish93/3eca6a90fef1ea6e586b7ec211ff72a5)