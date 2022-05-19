cd /app/src

while django-admin check --database default; do
	echo "Waiting for the DB to be ready."
	sleep 2
done

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
