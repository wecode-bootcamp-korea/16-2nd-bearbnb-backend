#./Dockerfile
FROM python:3 

# set working directory
WORKDIR /usr/src/app 

# Install packages
COPY requirements.txt ./ 
RUN pip install -r requirements.txt

# Copy all src files
COPY . . 

# Run the application on the port 8000
EXPOSE 8000   

# runserver with using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bearbnb.wsgi:application"]  

