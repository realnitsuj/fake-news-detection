# Backend Web Server

This is the backend web server powered by Python and FastAPI.

## Usage with docker

```sh
sudo docker build -t myimage .
sudo docker run -d --name mycontainer -p 80:80 myimage

# or, as a oneliner
sudo docker build -t myimage . && sudo docker rm mycontainer && sudo docker run -d --name mycontainer -p 80:80 myimage
```

## Usage without docker

### Run development server

You can run the development server using the following command :

```sh
uv run fastapi dev
```

### Export dependencies

```sh
uv export > requirements.txt
```

## Resources

- [FastAPI-Crud](https://testdriven.io/blog/fastapi-crud/)
  - [GitHub Repo](https://github.com/testdrivenio/fastapi-crud-async/blob/master/docker-compose.yml)
- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/first-steps/)
