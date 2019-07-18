# Blog_API

## Set environment variables
### For Flask
SET FLASK_ENV=development
### For Postgres
SET DATABASE_URL=postgres://postgres:{yourpassword}@localhost:5432/blog_api_db <br/>
Don't forget to create the database in pgAdmin or use this command: <br/>
createdb blog_api_db
### For the key
SET JWT_SECRET_KEY=MyKEY

## Make migration

When the database is created, you need to make the migration to create the table <br/>
python manage.py db init <br/>
python manage.py db migrate <br/>
python manage.py db upgrade <br/>
