
# Project Proposal

  

### What goal will your website be designed to achieve?
This site is for users who want to be able to share their tools with the local community. It allows for a user to enter the item(s) that they are willing to lend, and in return see local users who are also willing to lend items.

### What kind of users will visit your site? In other words, what is the demographic of your users?
This application is great for anyone who is in need without being able to shell out for expensive equipment.

### What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.
I am going to use a maps api, the top contenders are: 
* Google Maps
* Mapquest
* Mapbox

### In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information:

* #### What does your database schema look like?
    The database will consist of 2 tables in Postgres. _there is potential for other tables to assist with location, payments, etc but probably in a future update_. The initial 2 will be:
    * Users(id, username, email, password, first_name, last_name, location)
    * Tools(id, tool_name/tool_type, username/id FK) (_possibly photo url_)

* #### What kinds of issues might you run into with your API?
    * Figuring out how to handle tool types, because models/features can vary heavily with this. Possibly adding a photo feature to assist with the differentiation.
    * Location of users - using an address would be too personal. Using a zip code could cause issues with maps showing where it is if multiple results appear.

* #### Is there any sensitive information you need to secure?
    * Location will have to be sensitively handled
    * Passwords

* #### What functionality will your app include?
   * Standard CRUD for the most part, with some extra features via the api

* #### What will the user flow look like?
    1. A user lands on the home/landing page
    2. There will be calls to register/login
    3. A user will register - at time of registration they will also need to add at least one tool
    4. Once signed up, users can search for and see local results of tools in their area

* #### What features make your site more than CRUD? Do you have any stretch goals?
    * The initial app will be simple: creating and searching tools locally. Some stretch goals are as follows: 
    <br>
       1. Prohibiting a user from signing up without adding a tool
       2. Not allowing a user to remove a tool if they only own one
       3. Showing a map of "pins" where tools are (roughly) based off their user.