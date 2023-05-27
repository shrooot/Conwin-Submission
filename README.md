To run this project:

Install the dependencies using the command: 
```sh
pip install -r requirements.txt
```

Get the client_secret.json from the google cloud platform: https://console.cloud.google.com/marketplace/product/google/calendar-json.googleapis.com
or download the one I used from here: https://www.dropbox.com/s/7pxztrdeoypafrc/client_secret.json?dl=0

Download and put the json file in the rest/ directory

Run the project using the command
```py
python3 manage.py runserver
```

API Endpoints:

```
/rest/v1/calendar/init/ -> GoogleCalendarInitView()
Starts the authentication process. Asks the user to to sign in with their account
```

```
/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()
Provides handler to handle the redirect request from google and lists the events of the user in the calendar
```

Sample output screenshot:

https://ibb.co/YDmYgK8