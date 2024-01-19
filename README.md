# Step by step of how to run the API (Local)

## Step one: You need to clone the repository url:

```
git clone git@github.com:wichoiscoding/cdmx911_api.git
```

## After the clone, you need to create your new enviroment with:

```
cd cdmx911_api
pyenv virtualenv cdmx911_api
```

## Once you have the enviroment you need to install the libraries:

```
pip install -r requirements.txt
```

## Now you can run it!

```
make run_api
```


# Step by step of how to run the API using DOCKER

## Step One:
```
echo "GAR_IMAGE=cdmx911" >> .env
echo "GCP_PROJECT=lewagon-bootcamp-404323" >> .env
echo "GCP_REGION=europe-west1" >> .env
echo "PORT=8000" >> .env
echo "BUCKET_NAME=cdmx911" >> .env

```

## Step Two:
```
docker build --tag=$GAR_IMAGE:dev .
```

## Step Three:
```
docker run -it -e PORT=$PORT -p $PORT
:$PORT $GAR_IMAGE:dev
```
