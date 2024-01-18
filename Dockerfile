####### 👇 SIMPLE SOLUTION (x86 and M1) 👇 ########
FROM python:3.10-bookworm

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY cdmx911 cdmx911
COPY setup.py setup.py
RUN pip install .

# COPY Makefile Makefile
# RUN make reset_local_files

#CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
