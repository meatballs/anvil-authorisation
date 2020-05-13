# Authorisation
A server module for [Anvil Applications](https://anvil.works) that provides user authentication and role based authorisation
for server functions.

## Installation
There are two methods to install this module within your own application:

### 1. As a Dependency

  * Create a clone of this application within your own Anvil account using this link:

    [<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:CSPYXZNIBW5CVI6Y=AVI3ULSEJJC6HGEF7WTNTA7G)
  
  * At anvil, open the app in which you'd like to include authorisation and, its settings menu, select 'Dependencies',
    and select your new cloned app in the dropdown.

### 2. By Direct Inclusion

  * In your anvil application, create a new module in the server code section and name it 'authorisation'
  * Copy the entire content of `server_code/authorisation.py` from this repository into your 'authorisation' module

### Data Tables
Regardless of the method you used above, you will also need to setup the Users and Data
Table services in your app:

  * Ensure that you have added the 'Users' service to your app
  * In the 'Data Tables' service, add:
  	* a table named 'permissions' with a text column named 'name'
	* a table named 'roles' with a text column named 'name' and a 'link to table'
	column named 'permissions' that links to multiple rows of the permissions table
	* a new 'link to table' column in the Users table named 'roles' that links
	to multiple rows of the 'roles' table

## Usage

You can clone a demonstration of this module in use from:

[<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:LJIUHT6HFPGSOADD=P4ZGVKL3NTPHS67RFKHA66CW)

### Users and Permissions

* Add entries to the permissions table. (e.g. 'can_view_stuff', 'can_edit_sensitive_thing')
* Add entries to the roles table (e.g. 'admin') with links to the relevant permissions
* In the Users table, link users to the relevant roles

### Server Functions
The module includes two decorators which you can use on your server functions:

#### authentication_required
Checks that a user is logged in to your app before the function is called and raises
an error if not. e.g.:

```python
import anvil.server
from Authorisation.authorisation import authentication_required

@anvil.server.callable
@authentication_required
def sensitive_server_function():
  do_stuff()
```
#### authorisation_required
Checks that a user is logged in to our app and has sufficient permissions before the
function is called and raises an error if not:

```python
import anvil.server
from Authorisation.authorisation import authorisation_required

@anvil.server.callable
@authorisation_required("can_edit_sensitive_thing")
def sensitive_server_function():
  do_stuff()
```
You can pass either a single string or a list of strings to the decorator. The function
will only be called if the logged in user has ALL the permissions listed.

Notes:
  * The import lines in the examples above assume you have installed the authorisation module as a
  dependency. If you used direct inclusion, you will need to import from your own copy of
  the module.
  * The order of the decorators matters. `anvil.server.callable` must come before either
  of the authorisation module decorators.
