FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /RestaurantLunchVoting
WORKDIR /RestaurantLunchVoting
COPY requirements.txt /RestaurantLunchVoting/
RUN pip install -r requirements.txt
COPY . /RestaurantLunchVoting/