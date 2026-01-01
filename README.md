# **Docker Notes**

- Docker is a virtualization software.
- Makes developing and deploying applications much easier.
- Packages applications with all the necessary dependencies, configuration, system tools and run-time.

### How did it work before Docker?

First let's us see what problems does Docker solves?
1. Development process before containers
    - Each developers need to install and configure all services directly on their OS on their local machines. And, installation process is different for each OS environment.
    
    Docker standardizes the process of running any service on any local development environment. If you want any dependencies then you just have to run a command `docker run ...` and docker will fetch the dependencies from the internet and install and configure it for you.

2. Deployment process before containers?
    - Traditionally the process, would look like, developement team would produce a artifact, or a installation instructions telling how to install and configure app on the server?
    - Now the development team would give this to operations team and they will handle its installation and configuration apps and its dependencies.

    So, here the installations and configurations are done directly on the server's OS, which is very error-prone and you can have various problems during the setup process. You can also have dependency's version conflicts.
    
    Another problem could be miscommunication between development and operation team, because everything here is in textual format. There could some step that could be missed due to human error, andd when this error happens then operations team will have to go back to development team for solving the error.

    With containers this process could be simplified, because now the developers could create an application package that includes not only just the code, but also the required dependencies and its configurations too.

    Instead of textual, everything is packaged inside the `Docker artifact` or `Docker image`. And since, its encapsulated into one package, there's no need of configurations on the server (except Docker runtime).

Now, they only have to run the Docker command to fetch and run the Docker image.

Fetching (pulling):
```docker
docker pull IMAGE_NAME
```

Running:
```docker
docker run IMAGE_NAME
```

This makes the deployment process way easier on the operations side. And, yes the operations team will have to

- Install Docker runtime on the server

But that's just a one-time effort.

### Virtual machine and Docker

In your mind, you might be thinking if Docker is a virtualization tool, then why not use Virtual Machine.

First, lets understand how OS works, an OS contain two important layers:
- OS kernel
- OS applications layer

Virtual machines have a full OS, along with its kernel, system services, and then your application at the top, making it very heavy.

VMs are actually computer inside a computer.

Docker, on the other hand, doesn't have its own OS, and it runs on the host's OS kernel. Docker is just your code and its dependencies.

VMs works but they are painful and heavy at large scale deployments.

Docker gives you environment consistency, speed and scalability, CI/CD and automation.

Still, VM's aren't replaced by Docker, because when you need more security and stronger isolation, then VM are still relevant.

### Compatibility issue with the Docker

If there's a use case where you want to use _Linux_ based Docker image, then you cannot use it on _Windows_ machine.

Because, the _Linux_ based Docker image would need _Linux's kernel_ to run that application, and when you run that image on a _Windows_ machine, then it won't be able to run on _Windows's kernel_.

And, most containers are _Linux_ based. 

Originally, the Docker was built for Linux OS, but later Docker made an update and made **_Docker Desktop_**, for _Windows_ and _Mac_.

### How **_Docker Desktop_** works?

_Docker Desktop_ uses a _Hypervisor layer_ with a lightweight _Linux_ distro, containing a _Linux Kernel_, this makes running the _Linux_ based Docker containers possible on _Windows_ and _Mac_.

### Docker Images and Docker Containers

**_Docker Image_** is a package artifact that contains:
- Your code
- Runtime (Python, Node, Java, etc.)
- Libraries & dependencies
- OS-level files (lightweight Linux layers, etc.)
- Instructions to start the program

Docker images are _read-only_, _immutable_, _resuable_ and can be _shared_. Docker images aren't runtime entity.

And, Docker Images are built in layers:
- Base OS layer
- Runtime layer (could be Python, Node, Java)
- Dependencies layer
- Your program code layer

And, Docker is efficient, as if two images require the same image, then Docker saves them only once.

While, **_Docker Container_** is a live, running instance of the image.

What Docker does is, it takes the image, adds a writable layer on top, starts processing it, and then isolate it from the system. The running thing is called **_container_**.

All containers can have same _images_, but they will have different _IDs_, _lifecycles_, _data_.

You can run multiple containers from 1 image.

### Running of Docker

Docker contains Docker GUI and Docker CLI Client.

While using Docker CLI, you can:<br>
1. Check list of images available locally
    ```
    docker images
    ```
2. Check list of running containers:<br>
    ```
    docker ps
    ```

We also have _Docker Desktop_ if you want to use Docker in GUI.

<img src = "images\Screenshot 2025-12-29 153711.png">

Above, you see in the `Images` tab, you'll see the list of all the _Docker Images_. The _blue dot_, you see on the second image means that a container is made of this image.

<img src = "images\Screenshot 2025-12-29 154216.png">

Above, in the `Containers` tab, you'll see the list of all the _Docker Containers_. When there's a _blue dot_, it means that the container is running, otherwise it's not.

### Docker Registry

Lets us say that we want to run a container, so you would need a _Docker Image_. So, where do you get the _Docker Images_?

That's where, **_Docker Registries_** come into picture, there are image storage and distribution systems for _Docker Images_. There are many Docker Images stored over there.

There are official images available from applications like _Redis_, _Mongo_, _Postgres_, etc.

Docker itself has its one of the biggest _Docker Registry_ called, **_Docker Hub_**.

<img src = "images\Screenshot 2026-01-01 122158.png">

Official Docker Image of MongoDB

<img src = "images\Screenshot 2026-01-01 122504.png">

### Image Versioning

Technologies changes, therefore there are updates in the technologies, so there are versions in the technologies.

So, for each version of any technology, a new _Docker Image_ will be created.

- _Docker images_ are versioned.
- Different versions are identified by **_tags_**.
- _Docker tags_ are used to identify images by name.
- **_"latest"_** tag mostly refers to the newest release.

### Pull an Image

- Go to the _Docker Hub_, and locate the _image_ you want to pull.
- Then, look at the command on the page of the image that you've located. The command will be like (here, we took example of `nginx`).

```docker
docker pull nginx:1.23
```

- Then, go to the _Docker CLI_, or click on the `Terminal` of the _Docker Desktop_, and type the command.
- You can also, pull a specific tag of the image by,<br>
`docker pull {name}:{tag}`.
- Then, press Enter, to start downloading the _Docker image_.

### Run an Image

To run an _image_, we use command
```docker
docker run nginx
```

Usually, the command for running the Docker Image is<br>
`docker run {name}:{tag}`

And, now _Docker Container_ is running.<br>
You can now look for it by running this command
```docker
docker ps
```

- Docker generates a random name for the container automatically if you don't specify one.

In order to run a _Docker Container_ without blocking the terminal, we can use `-d` in the command, which stands for _detach_.
```docker
docker run -d nginx:1.23
```

### Port Binding

Port binding is often called port mapping.

Port binding connects a port on your host machine to a port inside the Docker container.

Let's understand this by an analogy:<br>
Container = apartment<br>
Port = door number<br>
Host = building<br>
Port binding = front desk forwarding visitors to the right apartment

Docker containers run on a specific port, and it is different for different technologies.

The port for **_PyTorch_** won't be same for **_MongoDB_**.<br>
For example the port for `nginx` is `80`.

Syntax of port binding:
```docker
docker run -p HOST_PORT:CONTAINER_PORT IMAGE_NAME
```

```docker
docker run -p 8000:8000 my-fastapi-app
```

