# Deployment Guide

## Pre-Deployment Checklist

- [ ] Generate a strong SECRET_KEY
- [ ] Set FLASK_DEBUG=False for production
- [ ] Test user registration and login
- [ ] Verify CSRF protection is working
- [ ] Test all forms (add card, review, delete)

## Generate a Secure SECRET_KEY

Run this command to generate a secure secret key:

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

Copy the output and use it as your SECRET_KEY environment variable.

## Platform-Specific Instructions

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-leitner-app

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key"

# Deploy
git push heroku main

# Open app
heroku open
```

### Render

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - **Name:** your-leitner-app
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add Environment Variable:
   - Key: `SECRET_KEY`
   - Value: (paste your generated secret key)
6. Click "Create Web Service"

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Add environment variable
railway variables set SECRET_KEY="your-generated-secret-key"

# Deploy
railway up
```

### PythonAnywhere

1. Upload your code to PythonAnywhere
2. Create a new web app (Flask)
3. In the web app configuration:
   - Set the source code directory
   - Set the virtualenv path
   - Configure WSGI file to point to your app
4. Add SECRET_KEY to .env file or web app environment variables
5. Reload the web app

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
ENV FLASK_DEBUG=False

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

Build and run:

```bash
docker build -t leitner-app .
docker run -p 8000:8000 -e SECRET_KEY="your-secret-key" leitner-app
```

## Post-Deployment Testing

After deployment, test these features:

1. **Registration**
   - Try weak password (should fail)
   - Try invalid email (should fail)
   - Create valid account (should succeed)

2. **Login**
   - Try wrong password (should fail)
   - Login with correct credentials (should succeed)

3. **Dashboard**
   - Add a new card
   - Search for cards
   - Delete a card

4. **Review**
   - Mark a card as pass/fail
   - Verify box progression

## Monitoring

### Check Application Logs

**Heroku:**
```bash
heroku logs --tail
```

**Render:**
Check the Logs tab in your service dashboard

**Railway:**
```bash
railway logs
```

## Troubleshooting

### Issue: CSRF Token Errors

**Solution:** Ensure SECRET_KEY is set and consistent across requests

### Issue: Database Errors

**Solution:** 
- SQLite works for single-instance deployments
- For multi-instance, migrate to PostgreSQL

### Issue: Password Requirements Not Working

**Solution:** Clear browser cache and test registration again

## Security Recommendations

1. ✅ Always use HTTPS in production
2. ✅ Set a strong, random SECRET_KEY
3. ✅ Never commit .env or database files
4. ✅ Enable CSRF protection (already implemented)
5. ✅ Use strong password requirements (already implemented)
6. ⚠️ Consider adding rate limiting for auth endpoints
7. ⚠️ Consider adding email verification
8. ⚠️ Consider adding two-factor authentication for sensitive accounts

## Database Migration (SQLite to PostgreSQL)

If you need to scale to multiple instances:

1. Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

2. Update app.py to use PostgreSQL connection
3. Migrate data from SQLite to PostgreSQL
4. Update environment variables with database URL

## Support

For issues or questions:
- Check the README.md
- Review application logs
- Test locally with FLASK_DEBUG=True (development only)

