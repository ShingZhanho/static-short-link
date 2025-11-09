# j-shi.ng - Django URL Shortener

A Django-based URL shortener service with a custom admin portal.

## Features

- **Simple Jumps**: Clean URL redirects that ignore parameters
- **Parameter Forwarding**: Forward URL parameters to destination
- **Custom Admin Portal**: Password-protected management interface at `/admin`
- **Click Tracking**: Monitor how many times each link is accessed
- **Search & Filter**: Easily find and manage your short links
- **Active/Inactive Links**: Toggle links on and off without deleting

## URL Structure

- **Short Links**: `j-shi.ng/go/<slug>` (e.g., `j-shi.ng/go/google`)
- **Admin Portal**: `j-shi.ng/admin`
- **Login**: `j-shi.ng/auth/login`

## Jump Types

### Simple Jump
URL parameters are ignored. The link redirects to the exact destination regardless of query parameters.

**Example:**
- Configured: `/go/google` → `https://google.com`
- Access: `/go/google?test=1` → Redirects to `https://google.com`

### Parameter Forward
URL parameters are passed through to the destination URL.

**Example:**
- Configured: `/go/bing` → `https://bing.com`
- Access: `/go/bing?kw=hello` → Redirects to `https://bing.com?kw=hello`

## Quick Start

### First-Time Setup

1. Create a superuser account:
```bash
ssh -i ~/.ssh/digital_ocean_mbp root@188.166.254.83
cd /var/www/j-shi.ng
source venv/bin/activate
python manage.py createsuperuser
```

2. Visit `http://188.166.254.83/admin` and log in

### Creating Short Links

1. Log in to the admin portal
2. Click "Create New Link"
3. Fill in:
   - **Short URL Path**: The slug after `/go/` (can include slashes)
   - **Destination URL**: Full URL with `http://` or `https://`
   - **Jump Type**: Simple or Parameter Forward
   - **Description**: Optional notes
   - **Active**: Enable/disable the link

### Managing Links

- **Edit**: Modify slug, destination, or jump type
- **Enable/Disable**: Toggle active status
- **Delete**: Permanently remove a link
- **Search**: Find links by slug, destination, or description

## Development Workflow

1. Make changes locally
2. Commit and push to the `production` branch:
```bash
git add .
git commit -m "Your changes"
git push origin production
```

3. GitHub Actions will automatically deploy to your droplet

## Technical Details

- **Framework**: Django 5.2.8
- **Database**: SQLite (default) or PostgreSQL
- **Server**: Gunicorn + Nginx
- **Auto-deployment**: GitHub Actions → DigitalOcean

## Documentation

- `QUICKSTART.md` - Quick deployment guide
- `GITHUB_SECRETS_SETUP.md` - Detailed configuration
- `DEPLOYMENT.md` - Full deployment documentation
