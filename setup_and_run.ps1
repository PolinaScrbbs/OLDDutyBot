python -m venv .venv

$activateScript = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "Не удалось найти скрипт активации виртуального окружения."
    exit 1
}

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py loaddata fixtures/db.json

python manage.py runserver