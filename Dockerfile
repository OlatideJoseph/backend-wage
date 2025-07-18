FROM python:3.9

WORKDIR /usr/local/app

COPY . /usr/local/app/

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home wage

EXPOSE 8000

USER wage

CMD ["gunicorn", "auto_wage_schedule.wsgi:application", "-w", "4", "-b", "0.0.0.0:8000"]
