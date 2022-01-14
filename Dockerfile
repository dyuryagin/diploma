FROM python:3.8
WORKDIR /backend
COPY requirements.txt /backend
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /backend
ENTRYPOINT ["python3"]
CMD ["app.py"]
