# Docker_Postgresql
1. It is necessary to change the IP address in the configuration file /configs/pg.hba.conf to the addresses of the hosts that will access the PostgreSQL database.
2. In the Dockerfile, change the username, password, and database name as desired.
3. In the docker-compose.yml file, also change the username, password, and database name. You can also set a custom name for the container.
4. script.sh is intended for installing Docker packages.
