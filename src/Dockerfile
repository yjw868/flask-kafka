FROM python:3.7
# COPY index.html /app/
# COPY requirements.txt /app/
# COPY app.py /app/
# WORKDIR /app
# RUN pip install -r requirements.txt
# CMD python -u app.py

WORKDIR /app

# Backup the default app files.  You could also delete these
# RUN mkdir bak && \
# 	mv main.py bak

COPY ./  ./
RUN pip3 install -r requirements.txt

# Make /app/* available to be imported by Python globally to better support several
ENV PYTHONPATH=/app
CMD python -m app.main
# CMD flask run --host=0.0.0.0 --port=80