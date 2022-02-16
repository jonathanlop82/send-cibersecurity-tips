FROM python:3

ADD main.py /
ADD requeriments.txt /
RUN pip install -r requeriments.txt
CMD [ "python", "./main.py" ]