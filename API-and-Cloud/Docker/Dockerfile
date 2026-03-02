#base image
FROM python:3.9-slim


#work dir
WORKDIR /app

#copy file
COPY . /app

#run 
RUN pip install -r requirements.txt

#EXPOSE 5000
EXPOSE 5000


#command to run the app
CMD ["python", "./app.py"]
