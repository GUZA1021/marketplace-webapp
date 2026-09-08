Make sure you have installed it from their website : https://docs.docker.com/desktop/setup/install/windows-install/

Restart your pc and make sure that its installed with cmd: docker --version
Also, make sure that virtulization is enabled. Go to task manager -> performance

Then download wsl if you havent with: wsl --install and Restart
If you download it, then make a user and password by opening ubuntu on windows

Open the docker desktop app and if the engine is running you can build the app with 2 different ways:
1
docker build -t flaskapp .

Then run it
docker run -p 5000:5000 flaskapp

2 This method also has data persistance. We tell Docker to use our yaml file, which specifies a volume. A volume
is a file that Docker will keep track of (in this case our DB), so that when we create a new container by running the app,
it uses the same version of the DB, rather than discarding it and making a new one for the container. Note that 
these changes to the DB are not reflected in instance/marketplace.db locally, but that Docker keeps it internally.
-docker compose build
docker compose up (alternative: docker compose up -d)
You can also use docker compose up --build, which will do both of these in a single line

Then you can open the web app on http://localhost:5000/ or open the link in cmd/Docker

Note: For artefact 2 use 5002 instead of 5000.