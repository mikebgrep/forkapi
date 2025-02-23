# ForkAPI

![version](https://img.shields.io/badge/version-4.0.0-green) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  <a aria-label="Build" href="https://github.com/mikebgrep/forkapi/actions?query=Build%20and%20Push%20to%20Docker%20Registry">
    <img alt="build" src="https://img.shields.io/github/actions/workflow/status/mikebgrep/forkapi/run-tests.yml?label=Build&logo=github&style=flat-quare&labelColor=000000" />

<img align="right" src="https://github.com/mikebgrep/foodie/blob/master/assets/logo.png" height="170px" alt="Logo">

ForkApi is a Lightweight RestAPI with admin panel to manage food recipes easily. 

 
   - 🐍 Python Django & Django rest framework based
   - 🛳 Dockerfile for easy deployment + included packages for Raspberry Pi.
   - 👨‍🍳 Admin panel revamped with [jazzmin](https://github.com/farridav/django-jazzmin)
   - 🔐 Header authentication for easy access management to the API read endpoints
   - 🔐 Token authentication for create and update endpoints
   - 🪶 SQLite database support.
   - 🌐︎ FE ready made web application [fork.recipes](https://github.com/mikebgrep/fork.recipes)
   - 🔎 Search endpoints supporting pagination
   - 📋 Schedule Meal plan application
   - 🤖 AI Scrape page to recipe (scrape functionality that save a recipe by given a valid url)
   - 🤖 AI Generate recipe from a given ingredients (returns valid links with the generated recipes)
   - 🤖 AI Translate recipe to number of languages 🈹️

### Documentation
You can sneek peek into  the [documentation](https://mikebgrep.github.io/forkapi/) of the API. \
By default the installation is without SSL you can follow the instructions how to enable it.
## 

### Docker image 
( must be used with nginx folder and .env file together to work) 

- amd64 image
```
docker pull mikebgrep/forkapi:latest
```
- arm64 image
```
docker pull mikebgrep/forkapi:arm64
```
### Admin panel 
![admin](https://github.com/mikebgrep/foodie/blob/master/assets/admin.gif)

### Front End application
You can benefit from already build dockerized FE web application fork.recipes.That can be deployed together with the API.
All instructions are added in the documentations ➡ [docs](https://mikebgrep.github.io/forkapi/clients/)

## Support 
You can support the repo as clicking on the sponsorship button.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/mikebgrep)

### License
The repository use [MIT](https://opensource.org/licenses/MIT) license

