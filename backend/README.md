
# Persino

A Django flight booking website that is working with IranAir API Service.




## Tech Stack

**Client:** HTML, CSS, JS (Bootstrap5)

**Server:** Python, Django, PostgreSQL

## Color Reference

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Color1 | ![#FA163F](https://via.placeholder.com/10/FA163F?text=+) #FA163F |
| Color2 | ![#12CAD6](https://via.placeholder.com/10/12CAD6?text=+) #12CAD6 |
| Color3 | ![#0FABBC](https://via.placeholder.com/10/0FABBC?text=+) #0FABBC |
| Color4 | ![#E4F9FF](https://via.placeholder.com/10/E4F9FF?text=+) #E4F9FF |


## Run Locally

Go to the project directory

```bash
  cd backend
```

Create virtual environments

```bash
  python -m venv .venv
```

Run virtual environments

```bash
  source .venv/bin/activate
```

Install requirements

```bash
  pip install -r requirements.txt
```

Make migrations

```bash
  python manage.py makemigrations
```

Migrate

```bash
  python manage.py migrate
```

Collect statics

```bash
  python manage.py collectstatic
```

Create super user

```bash
  python manage.py createsuperuser
```

Run project

```bash
  python manage.py runserver
```


## Additional Information

The main Django project name is `backend`. :))

`search_data` Django app is to save searching and booking data.

There is a `panel` app for admins to see all booked and searched flights.

`accounts` App will handles users like their profiles or login and signup functions.

The main app that handle main functions like Booking, Deleting,... is `apihandler`.
In this App folder, there is a folder named `data` that covers IranAir API resources and edited requests and responses.
`table source.txt` shows relations between each file and its API function.
## Demo

This is the link to demo `persino24.com`.


## Deployment

Also to deploy this project everything depends on the server but one of 
the most important things in deploying is to change file locations to 
the server's new locations in `apihandler/views.py`.
## API Documentation

IranAir Documentations are in the main location and in `Docs` folder (Not in the project's folder!).
## Features

- LogIn/LogOut/SignUp/Profile
- Search/Book/Read/Split/Change/Delete Tickets
- Responsive for mobile devices.
- Simple Admin Panel
- Saves searching and booking data.
- Bootstrap5/jQuery/lottiefiles/flickity/gsap/GoogleFonts/GoogleMaterialIcons


## TODO

- Additional browser support

- Add more integrations


## Feedback

If you have any feedback, please reach out to me at sepehr0sohrabi@gmail.com.


## Author

- [@sepehrsohrabii](https://www.github.com/sepehrsohrabii)

