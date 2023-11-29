# Cloud and Edge Computing: lab materials

## Folder structure

Right now 2 main folder present:
```
cloudedgecomputing
|
└─── docs: contains slides and documentations
|
└─── base-dcoker-and-compose: basic examples of docker and docker compose use
```

### docs

Folder right now contain mainly slides, but eventually open documentation collected online will be included

### base docker and compose 

The folder container a series of basic exampla of docker and docker compose use. Particularly in the case of docker use, mostly it contains examples of Dockerfile and how to write them.

`docker-compose.yml` is the extended version of `short.docker-compose.yml`, it contains most of the possibile configuration you can insert inside a docker compose with reference to specific documentationa. `short.docker-compose.yml` is the shortened version of the same, where useless or unused parameters have been removed.

`prod-like.docker-compose.yml` is a modified version of `short.docker-compose.yml` that implements some prod like features. Above all, every time we define something that is service specific (names, variables, image and tag, options value, etc.). Moreover, common aspect are condensed using **fragment** notation: https://docs.docker.com/compose/compose-file/10-fragments/, a built-in YAML feature. 

### development history

In each project folder I will put a `README.md` containing detailed explaination about the projet development history.

Right now existing projects are
```
|
└─── base-docker-and-compose
|
|
```

#### `base-docker-and-compose`

A simple Flask project, we start by running only a docker with postgres for our local flask app, then we will build the whole infrastracture with docker compose.