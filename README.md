# MiniGameArchive

This project is the MiniGameArchive. A Django website to manage games and exercises you can do with your sports team during training sessions. I'm a Basketball trainer myself, but the project can be used to manage games of all sorts.

It features:
* A backend to manage exercises
* A front page that let's you filter and search through the exercises
* A detail page that shows the exercise with everything you need to know
* The ability to add exercises to a training plan, so you can easily create plans for the next training session
* The ability to print single exercises or training plans so you have everything available in your next training session

## What is a Game?

A game, or an exercise, is something you can do with your team during your training sessions. It's a small competition you run or something that helps the players get better at a specific skill.

It typically consists of the following information:

* **Name:** Short descriptive name of the game. Example: "Fruit Bowl"
* **Focus:** What is this game focusing on? Example: "Dribbling, Teamwork, Layups, ...". Could be multiple depending on the exercise.
* **Description:** Detailed description. At best these are in short list format, so that during the training session you can glance over the game card and see what it's about
* **Player number:** For how many players is the exercise? It it done by just 1 or 2 players, or do you need a bigger group, like a 8+ game? When it's only a few player you can decide to split a larger group into many subgroups all doing the exercise on their own
* **Variants:** These are variations that add new aspects to the exercise, making it more fun or harder for better players
* **Material:** What is needed to do the exercise? Example: Basketball, Halfcourt, Hoop, Wall, ...
* **Duration:** Typical duration of the exercise (5min, 10+ min, ...)
* **Labels:** Additional, custom labels are helping to sort and filter the exercises

## What is a Training Session?

A training session typically consists of multiple games. It typically has a structure like first playing a warmup game, then focusing on 1-2 specific skillsets and in the end do a cool-down game.

## Managing the Games

The page provides a full backend to manage the data. Users that do not have access to the backend can enter their suggestions through the frontends, which an admin can then review and release into the database.

## Using the site for preparation

The typical user-flow let's the coach search and filter for games. When he finds one that he'd like to run, he can add it to a Training Session (this is designed to work like a shopping card on an E-Commerce site). When he finished the session he can decide to print out game cards for the single games and session card for the whole training session. That way he has everything available when he's running the actual practice session.

The printouts are designed to be printed in business card format (front and back page), so it's easy to have them on hand and give some help when checking for the details while working with the team.

# Installation

The website comes in a Docker container and can be simply started by running the following command:

* `docker run --it -v ./data:/data -p 8080:8080 monsdar/minigamearchive:latest`

By default it uses SQLite to store data, but you can also connect it to a Postgres DB by using the following env vars:

* `POSTGRES_HOST`
* `POSTGRES_PORT`
* `POSTGRES_DB`
* `POSTGRES_USER`
* `POSTGRES_PASSWORD`

The following configuration options are available as well via env vars:

* `DJANGO_ALLOWED_HOSTS`: Set this to the host address you'd like to run the page under
* `DJANGO_PRODUCTION`: Set this to any value to have the application run in production mode. Else debugging will be enabled
* `DJANGO_SECRET_KEY`: Set your own Django secret key. Should be at least 32 char in length
* `DJANGO_CSRF_TRUSTED_ORIGINS`: Define which addresses the page trusts for loading scripts etc

## Support

Feel free to open GitHub issues whenever you find an issue or look for an improvement. If you'd like to support my work in general consider [buying me a coffee](https://buymeacoffee.com/monsdar) ☕.
