# foodpact

Visualize the environmental impact of foods you eat. 🍔🍉🥦

## Application quickstart

### Basics

1. Create and activate a virtualenv
2. Install the requirements

Here for Powershell -

```powershell
git clone <this_repo>
cd <this_repo>

python -m virtualenv venv

.\venv\scripts\activate.ps1
```

### Environment variables

```powershell
set-variable -name "APP_SETTINGS" -value "project.server.config.DevelopmentConfig"
```

or

```powershell
set-variable -name "APP_SETTINGS" -value "project.server.config.ProductionConfig"
```

### Run the application

```powershell
python manage.py run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/).

### When you're done

Deactivate the virtual environment!

```powershell
deactivate
```
