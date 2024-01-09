# moneio
#### Video Demo: https://youtu.be/dLLyKA20Pgo

A web application made using Django that tracks your money in your different money accounts through money in, money out, and money transfer.

## Description
You need to register or login if you already have an account to input your data to the application. The application have three main views namely, the dashboard, the transactions, and the transfers which will all be initially empty.

The first thing you need to do to use the app is to add a money account, it can be your bank, your physical wallet, or any form of money storage you have. You need atleast one money account to use the money in and money out functionality. To use the money transfer functionality, you need at least two money accounts before you can start transfering your funds from one money account to another money account.

The transactions view tracks all the money in and money out transactions for all your accounts and list them in a reverse chronological manner. Each row have details of the transaction which are the date, the name of the transaction, the name of the money account, and the transaction amount.

The transfers view tracks all the transfers you made from your accounts. Each row have details of the transfer which are the date, the name of the transfer, the money account where the amount came from, the money account where the amount go to, and the transfer amount.

The dashboard view shows all your created money accounts divided into three categories, the accounts, the floating accounts, and deductibles accounts. The accounts are money accounts you currently have. The floating accounts are money accounts you do not currently have or money owed to you. The deductibles accounts are money accounts for money you owed to others.

You can edit any detail of a money account, of a money transaction, and of a money transfer by clicking its row.

The dashboard shows the calculations of your current financial standing. The first group which is the accounts gives the total of all your current money accounts you have. The next group which is the floating accounts gives the total of all your money accounts you don't currently have. These two totals will be added to get the gross amount of money you have. The deductibles group can also be considered as floating accounts but the values are negatives because these are money you currently owed to others. The totals of the deductibles will be subtracted from the gross total resulting for the net total or the money you should have currently. The last calculation is the onhand total which is the net total minus the total of the floating accounts or the money you can have a reliable access to.

## Project Components
### moneio folder
  1. models.py - Contains the models used for the data of the application. It contains three models, the Account, the MoneyInOUt, and the Transfer.
  
      The Account model is for the user's money accounts. It has a user column for the owner of the account, a name column for the name of the account, an initial_balance and an initial_balance_date columns for the starting balance and date of the account. And a is_floating column that checks if the account is a floating account meaning the money in this account is currently not in you possession.

      The MoneyInOut model is for the user's every money transactions. It also has a user column for the owner of the transaction, a name column fo the name of the transaction, a price column for the amount of the transaction, a date column for when the transaction was made, and an account column for the account where did the transaction was made.

      The Transfer model is for user's transactions but for transferring money to any of the user's accounts. It has a user column for the owner of the transfer transaction, a name colum for the name of the transfer transaction, a price column for the amount of the transaction, a date column for the date of the transaction, and a from_account and a to_account columns for the origin and destination account of the transaction.

      Each model have a serialize function that returns a dictionary of the entry's details to be used in the views.py file.

  2. urls.py - Contains the application's paths and api endpoints.
  
      It has a path for the root path of the application where the main page of the application can be viewed, a path of the login and register page. And a logout endpoint to log out a logged in user of the app.

      The api routes of the app is for creating and editing accounts, transactions, and trasnfer transactions.

  3. views.py - Contains the login of each application's paths and api endpoints.

      authenticate_index - A function that checks if the user is authenticated and gets all the data from the database and processes the data that will be displayed in the main page. It is also used as a function decorator for the index, login_view, and register view.

      index - A function that redirects the user if they are not authenticated.

      login_view - a function that returns the login page with the get method and process the login credentials with the post method.

      logout_view - a function that logouts the user and redirects the user to the index and which in turn redirects again to the login page.

      register - a function that returns the register page with the get method and process the register credentials with the post method.

      account - a function that creates a new account for the user.

      moneio - a function that creates a new money transaction which can be money in to an account and money out from an account.

      edit_account - a function that retuns the edit account page with the get method and edits/deletes the account with the put/delete method.

      monei - a function that returns the edit money in page and edits/deletes the money in transaction with the put/delete method.

      moneo - a function that rerturn the edit money out page and edits/deletes the money out transaction with the put/delete method.

      transfer - a function that creates a new transfer transaction.

      edit_transfer - a function that return the edit transfer transaction page with the get method and edits/deletes the transaction with the put/delete method.

      #### templates/moneio
        1. layout.html - The layout of the application where every page of the app is rendered.

        2. index.html - The main page of the application with three main views, the dashboard, the transactions and the transfers. It also has the create account, create transaction, and create transfer page.

        3. login.html - The login page that shows when the user is still not authenticated.

        4. register.html - The page for creating a user account.

        5. account.html - For viewing, editing, and deleting a particular money account.

        6. moneio.html - For viewing, editing, and deleting a particular money transaction.

        7. transfer.html - For viewing, editing, and deleting a particular money transfer.

      #### static/moneio
        1. styles.css - The css file for styling the layout template.

        2. index.css - The css file for styling the main page.

        3. login.css - The css file for styling the login page.

        4. register.css - The css file for styling the register page.

        5. account.css - The css file for styling the account page.

        6. moneio.css - The css file for styling the moneio page.

        7. transfer.css - The css file for styling the transfer page.

        8. index.js - The script file for the main page. It controls what view will be displayed depending on what view is active.

        9. account.js - The script file for the account page that handles the editing and deletion of an account.

        10. moneio.js - The script file for the moneio page that handles the editing and deletion of a money transaction.

        11. transfer.js - The script file for the trarnsfer page that handles the editing and deletion of a money transfer.

## How to run the application
1. Install python
2. Install Django
3. Clone project
4. Navigate to the root directory of the project where manage.py is located
5. Run `python manage.py runserver`
