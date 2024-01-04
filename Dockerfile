# Dockerfile, Image, Container
FROM python:3.11.6

# add every file in every folder
ADD . .

# install requirements.txt
RUN pip install -r requirements.txt

# run main.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]