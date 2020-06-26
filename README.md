# Flip video streamer

## Quick start
1. Copy .env.example to .env
2. Change envs values if need

Make sure you have a docker client up and running on your machine.
* Clone this repo.
* Build image `$docker build --tag flip:latest ./` (on root directory)
* Run this image in a container `$ docker run -p 5000:5000 --env-file .env -it flip`