
## Setup Instruction
1. Setup the virtual environment.

  ```
  virtualenv -p python3.6 env
  source env/bin/activate
  ```

2. Install the dependencies.

  ```
  pip install -r requirements.txt
  ```

3. Setup the ``postgres`` database.

  ```sql
  drop database mikaid_db;
  create database mikaid_db;
  \c mikaid_db;
  CREATE USER django WITH PASSWORD '123password';
  GRANT ALL PRIVILEGES ON DATABASE mikaid_db to django;
  ALTER USER django CREATEDB;
  ALTER ROLE django SUPERUSER;
  CREATE EXTENSION postgis;
  ```

4. Populate the environment variables for our project.

  ```
  ./setup_credentials.sh
  ```

5. Go inside the environment variables.

  ```
  vi ./uservault/uservault/.env
  ```

6. Edit the file to suite your needs.

7. In your console, go ahead and initialize the project with your own values.

  ```
  python manage.py migrate
  python manage.py setup_app
  ```

8. Please update your ``env`` file with the outputs.
