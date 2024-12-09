# Docker_Aska.App
1. script.sh is intended for installing Docker packages.
2. It is necessary to change the IP address in the configuration file postgres/configs/pg.hba.conf to the addresses of the hosts that will access the PostgreSQL database.
3. In the Dockerfile, change the username, password, and database name as desired.
4. In the docker-compose.yml file, also change the username, password, and database name. You can also set a custom name for the container. Also, change DATABASE_URL to yours.
5. Edit hash_creaty.py, set your password, then go into the container using docker exec -it app_container bash, and run the hash_creaty.py script, which will output the password hash. Add this hash to app/.env.
6. In app/app.py, make sure to update app.config['SQLALCHEMY_DATABASE_URI'] = and ADMIN_USERNAME = with your own values.
7. In the app.py file, in the line ALLOWED_IPS =, enter a list of IP addresses that should have access to the web application, connections from other addresses will be blocked
