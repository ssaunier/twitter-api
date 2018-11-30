Starting point for Day 4 of Python API Week.

```bash
pipenv install --dev
pipenv run nosetests
```

Don't forget to *apply migrations if you just forked the git repository* :
```bash
pipenv run python manage.py db upgrade
```

:point_right: Previously, you should have manually created a `flask_db` and a `flask_db_test` databases like so:

For a windows environment, in a gitbash terminal :
```bash
winpty psql -U postgres -c "CREATE DATABASE flask_db"
winpty psql -U postgres -c "CREATE DATABASE flask_db_test"
```

For an unix environment, in a terminal :
```bash
psql -U postgres -c "CREATE DATABASE flask_db"
psql -U postgres -c "CREATE DATABASE flask_db_test"
```

:point_right: Don't forget to create a `.env` file *in your project folder*, then add your `DATABASE_URL` as previously:
```
DATABASE_URL=postgresql://postgres:<password_if_necessary>@localhost/flask_db
```

Ex:
```
DATABASE_URL=postgresql://postgres:root@localhost/flask_db
```

:point_right: Don't forget to *start your redis server* and to add `REDIS_URL` to your `.env` file :
```
REDIS_URL=redis://localhost:6379
```

:point_right: To launch the api :

```bash
FLASK_ENV=development pipenv run flask run
```

:point_right: [localhost:5000](http://localhost:5000) for Swagger documentation.
