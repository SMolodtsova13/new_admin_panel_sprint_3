set -e

HOST="$1"
PORT="$2"
shift 2

while ! nc -z $HOST $PORT; do   
  sleep 1
done

echo '✅ Выполняем миграции...'
python manage.py migrate --noinput

echo '📦 Собираем статику...'
python manage.py collectstatic --noinput

echo '🚀 Запускаем uWSGI...'
exec uwsgi --strict --ini /opt/app/uwsgi.ini
