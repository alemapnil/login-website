FROM python:3.13.2
WORKDIR /login-website
ADD . /login-website
RUN pip install -r w_requirements.txt
CMD ["python3","-u","app.py"]
EXPOSE 2000