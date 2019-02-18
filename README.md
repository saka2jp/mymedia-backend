# mymedia backend

Runnning Locally
---
Make sure you have [Docker Compose](https://docs.docker.com/compose/install/).

```sh
$ cp .env.example .env
$ docker-compose up
```

Your app should now be running on http://0.0.0.0:8000/polls/

Super user is created automatically by Docker Compose.

|Email|Password|
|:-:|:-:|
|admin@example.com|admin|


Deploying to Heroku
---
1. Create [New tag](https://gitlab.com/jumpyoshim/django-polls/tags/new)
   - Tag naming rules conform to [Semantic Versioning](https://semver.org/)

1. Execute deploy job with the tag you created


Coverage Report
---
The coverage report is generated by [pytest-cov](https://github.com/pytest-dev/pytest-cov).

See the link below:

https://my_media.gitlab.io/backend
