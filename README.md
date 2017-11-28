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

## Some Snapshots


