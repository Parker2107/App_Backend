# Backend

## Implementaion

This repo contains the User and Admin side Backend that is to be used for the application. The user, when first entering, will register using their google account / whatever the frontend seems fit and the Backend will recieve the userProfile in one json call.

While registering, if the user enters "\_admin\_" anywhere in their username, they will be marked as admin and during Login the next time, they will be able to login using only Admin login.

## DataBase Formats

### User Profile

1. Registration Number (Unique)
2. Name
3. Email (Unique)
4. Hostel
5. Block
6. Room
7. Phone Number
8. Admin (Boolean)

### Form Data

1. Registration Number
2. Name
3. Domains

## Routes

### Send data for new register

curl -X POST http://127.0.0.1:8000 -H "Content-Type: application/json" -d '**_Enter JSON Format here_**'

### Get list of all data

curl -X GET http://127.0.0.1:8000 -H "Content-Type: application/json"

### Check specific registration number

curl -X GET http://127.0.0.1:8000/check/ **_Registration Number_** -H "Content-Type: application/json"

### Delete all data

curl -X DELETE http://127.0.0.1:8000/delete -H "Content-Type: application/json"

### Delete specific registration number

curl -X DELETE http://127.0.0.1:8000/delete/ **_Registration Number_** -H "Content-Type: application/json"

### Edit entire profile

curl -X PUT http://127.0.0.1:8000/edit/ **_Registration Number_** -H "Content-Type: application/json" -d '**_Enter JSON Format here_**'

### Edit specific fields of a profile

curl -X PATCH http://127.0.0.1:8000/edit/ **_Registration Number_** -H "Content-Type: application/json" -d '**_Enter JSON Format here_**'

### Upload Form submission by a student

curl -X POST http://127.0.0.1:8000/upload -H "Content-Type: application/json" -d '**_Enter JSON Format here_**'

### Recieve list of all Form submissions

curl -X GET http://127.0.0.1:8000/upload -H "Content-Type: application/json"

### Recieve list of all registered students in an event

curl -X GET http://127.0.0.1:8000/upload_sheet/?api_key=API_KEY&sheet_name=Workshop_A

### Upload data of all registered students in an event

curl -X POST "http://127.0.0.1:8000/upload_sheet/" \
 -H "api_key: API_KEY" \
 -F "file=@/Users/yourname/Documents/attendance.xlsx" \
 -F "sheet_name=Spring_Seminar" \
 -F "event_date=2025-03-23"

### Delete a specific sheet

curl -X DELETE "http://127.0.0.1:8000/delete_sheet/?api_key=API_KEY&sheet_name=EVENT_NAME"

### Edit the attendance status from an event

curl -X PATCH "http://127.0.0.1:8000/api/update_attendance/" \
	-H "Content-Type: application/json" \
	-H "api_key: API_KEY" \
	-d '{
            "sheet_name": "Spring_Seminar",
            "records": [
				{
					"ParticipantId": "12345",
					"ParticipantName": "John Doe",
					"SessionAttended": "A"
				},
				{
					"ParticipantId": "67890",
					"ParticipantName": "Jane Smith",
					"SessionAttended": "A"
				}
			]
        }'

        
By default, all the attendance for every person is P in the dB, **Only send the people's attendance that are A**.

## Reset migrations

1. Change the model in models.py
2. Remove migrations folder
3. Drop the Database / Delete db.sqlite3
4. python3 manage.py makemigrations <app_name>
5. python3 manage.py migrate
6. If added a new Model, change serializer.py
7. Make sure URL exists and views function exists

## TODO

1. Create a table for storing list of NS forms.
2. Make a cascading key attribute in the NS model for connecting the rows to their respective NS.
3. Setup a timer system that does not allow the user to send requests to the dB after 4:00 PM
4. find better alternatives for Supabase to host the dB
