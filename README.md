# Borrowbooks 
A web2py powered application with the idea for managing Books. Basically, the application has the following key features -

-  Users to create a profile and choose one of the packages (Golds/Diamond/Silver) where each package will allow certain number
   of books to be borrowed.
-  Users can Search for books, Add a book to their wishlist, Borrow books, Leave the reviews and give ratings
-  An admin interface which will allow to manage the data. By default, when a new user registers for a account, it is put to 
   pending state. Once verified, user(s) can start browing the site and borrow books.
-  Email notification on registering an account and its verification
-  Bootstrap3 enabled, toastr javascript notifications used for info/error messages, custom Google styled Paginator, Review and
   Rating support.
   
## Getting Started
To use this application, you would need the following :-

**Web2py** : version 2.14.6 or higher

**PIL**    : version 1.1.7 or higher *( This is basically used for image compression while adding a new entry using admin interface and database population with seed data)*

You can populate the database with some random data including images using the following script

`borrowbooks/scripts/populate_database.py`

## LIVE Demo : [Click Here](https://sarbjit87.pythonanywhere.com/borrowbooks/default/index)

## Some Snapshots

### Homepage

![home1](https://user-images.githubusercontent.com/4709020/33297552-a5eca5f6-d3af-11e7-8414-0c42f1b7be40.png)
![home2](https://user-images.githubusercontent.com/4709020/33297554-a811aca0-d3af-11e7-9d92-c8e41fca1889.png)

### View Book Description

![viewdescription](https://user-images.githubusercontent.com/4709020/33297558-ab1e9962-d3af-11e7-8b56-f63a846d5e5f.png)

### Search 

![search](https://user-images.githubusercontent.com/4709020/33297561-ae98ba50-d3af-11e7-9f28-8587e6190a4b.png)

### Review and Notification

![reviews](https://user-images.githubusercontent.com/4709020/33297328-5e04b2c0-d3ae-11e7-992d-1e96183e7610.png)

![notification](https://user-images.githubusercontent.com/4709020/33297564-b0e72ea4-d3af-11e7-92bf-75a46527d708.png)

