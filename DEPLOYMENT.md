# Heroku Deployment Guide

## Prerequisites
1. Heroku CLI installed
2. GitHub repository set up
3. Heroku account

## Setup Steps

### 1. Create Heroku App
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:essential-0
```

### 2. Set Environment Variables in Heroku
```bash
heroku config:set SECRET_KEY="your-super-secret-key"
heroku config:set DEBUG=False
```

### 3. Configure GitHub Secrets
In your GitHub repository, go to Settings > Secrets and variables > Actions and add:

- `HEROKU_API_KEY`: Your Heroku API key (from Account Settings)
- `HEROKU_APP_NAME`: Your Heroku app name
- `HEROKU_EMAIL`: Your Heroku account email

### 4. Deploy
Push to main/master branch and the GitHub Action will automatically deploy to Heroku.

## Manual Deployment (Alternative)
```bash
# Add Heroku remote
heroku git:remote -a your-app-name

# Build frontend
cd frontend
npm run build
cd ..

# Copy frontend build to static
mkdir -p static
cp -r frontend/build/* static/

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Post-Deployment
1. Run migrations: `heroku run python manage.py migrate`
2. Create superuser: `heroku run python manage.py createsuperuser`
3. Collect static files: `heroku run python manage.py collectstatic --noinput`

## Environment Variables Needed
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: Automatically set by Heroku Postgres addon

## Files Created for Deployment
- `.github/workflows/deploy.yml`: GitHub Actions workflow
- `Procfile`: Heroku process definition
- `requirements.txt`: Updated with production dependencies
- `.gitignore`: Git ignore file
- Updated `settings.py`: Production configuration