
# PANTRY MANAGER APP
#### Video Demo:  <URL TBD>
#### Description:

This is a pantry manager app, designed as part of the Final Project submission for the the Harvard CS50x course. The web app is
a pantry manager app.

# Usage:

When the user first opens the app, they can either Register themselves by providing a username, password, and email or Log In
if they already have an account.

Once logged in, the default home page will be the current pantry inventory - this is maintained up to date based on any change
made by the user. The user may use the Add to Pantry to add a new item into the pantry inventory. Alternatively, the Update
Pantry page uses a form with dropdown lists to allow the user to select and existing item and enter the new quantity for that
item.

Another feature of this app is the Pantry Minimum Requirement feature. Upon log in, the user can click on Pantry Min to view
the minimum pantry inventory that is set-up by the user. Using the Edit Pantry Min link, users can either add a new item
to the minimum pantry inventory, or can click on the Edit Pantry Requirement to update an existing requirenent. The latter
view consists of a form with with dropdown lists allowing the user to select an existing item under minimum requirement and
enter a new value for the minimum requirement.

Additionally, leveraging on the min pantry requirement feature, the webpage provides a Restock List link. Using this link,
the user can view a list of items from the min requirement list which are in insufficient stock in the user's pantry. A button
at the page bottom allows the user to send a Restock List to the email address entered during registration.

Another feature of this app is the ability to find recipes that use maximum of the items in the users pantry inventory. This is
done using Spoonacular's free API.

# Database
The user data, pantry inventory, and minimum requirements are stored in three seperate SQL tables.

# Technologies Used
This web app uses a combination of HTML, CSS, Python, and Javascript. SQL is used for the database storage and frameworks
used include Flask and Bootstrap.
