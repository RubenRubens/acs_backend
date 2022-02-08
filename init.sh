cd src

while ! python manage.py sqlflush > /dev/null 2>&1 ;do
echo "Waiting for the db to be ready."
sleep 1
done

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
