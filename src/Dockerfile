FROM python:3.7
# COPY index.html /app/
# COPY requirements.txt /app/
# COPY app.py /app/
# WORKDIR /app
# RUN pip install -r requirements.txt
# CMD python -u app.py

WORKDIR /app
COPY ./ ./
RUN pip3 install -r requirements.txt

# Make /app/* available to be imported by Python globally to better support several
ENV PYTHONPATH=/app
CMD python -m app.main