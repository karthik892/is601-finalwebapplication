FROM python:3.8
ENV SENDGRID_API_KEY='<api-key-here>'
EXPOSE 5000
ENV SENDGRID_API_KEY='<api-key-here>'
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

CMD python app.py