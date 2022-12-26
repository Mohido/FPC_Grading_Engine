FROM python:3.7.16-slim-bullseye
WORKDIR /app
# RUN apk add build-base
RUN pip3 install flask 
RUN pip3 install pandas 
RUN pip3 install numpy
COPY . .
CMD ["python3", "server.py"]
EXPOSE 50001