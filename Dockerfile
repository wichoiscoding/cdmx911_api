####### 👇 SIMPLE SOLUTION (x86 and M1) 👇 ########
FROM python:3.10-bookworm

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY data data
COPY fast_api fast_api


# COPY Makefile Makefile
# RUN make reset_local_files

CMD  uvicorn fast_api.fast:app --host 0.0.0.0 --port $PORT
