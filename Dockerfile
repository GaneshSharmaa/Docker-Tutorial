# base image
FROM python:3.9

# working directory
WORKDIR /app

# copy the requirements file into the image
COPY . /app

# run the command to install dependencies
RUN pip install -r requirements.txt

# port
EXPOSE 5000

# command to run the application
CMD ["python", "./app.py"]

