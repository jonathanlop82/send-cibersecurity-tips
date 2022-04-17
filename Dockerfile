FROM python:3

ADD main.py /
ADD bot.jpeg /
ADD Ubuntu-Regular.ttf /
ADD requeriments.txt /
RUN pip install -r requeriments.txt
CMD [ "python", "./main.py" ]