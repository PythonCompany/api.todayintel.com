# V1 NLP API

Work in progress

## Build
We are using a Make file for running the app and building the docker image


## How to run

To run the application you will first have to pull the image locally. For doing that you will have first to pull the image locally

```commandline
docker pull cornatul/nlp:v1
```

To run the application you will have to run the following command

```commandline
docker run -p 8000:8000 cornatul/nlp:v1
```


### Development
If you want to change anything to the image please feel free

```commandline
make up-dev
```

### Production
To run this n production run the following command

```commandline
make up
```

## How to build 



### Production
```commandline
make build-fresh
```


## Documentation 

This is a NLP app that allows you the user to perform simple nlp tasks

### Endpoints

1. /docs - It's an endpoint that will allow you to see and test live 
