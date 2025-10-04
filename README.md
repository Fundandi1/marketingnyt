# MarketingNyt.dk

A production-ready Django/Wagtail content management system optimized for SEO, performance, and editorial workflow. Built specifically for marketing news and content publishing.

## 🚀 Features

### Content Management
- **Wagtail CMS** with intuitive editorial interface
- **StreamField** for flexible content creation (Rich Text, Headings, Images, Quotes, Callouts, FAQ)
- **Category system** for content organization
- **Tag management** for content discovery
- **Article scheduling** and revision control
- **Featured articles** system

### SEO Optimization
- **Automatic sitemap generation** (`/sitemap.xml`)
- **Robots.txt** with proper directives (`/robots.txt`)
- **Canonical URLs** on all pages
- **Meta tags** (title, description, OpenGraph, Twitter Cards)
- **JSON-LD structured data** (Organization, NewsArticle, BreadcrumbList)
- **Clean URL structure** (`/artikler/<slug>/`, `/kategori/<slug>/`)
- **RSS/Atom feed** (`/feed.xml`)
- **301 redirects** management via Wagtail

### Performance
- **Redis caching** (page cache + template fragments)
- **Whitenoise** for static file serving with compression
- **Image optimization** with WebP/AVIF support
- **Lazy loading** for non-critical images
- **Critical CSS** placeholder
- **Preconnect/Preload** optimization hooks

### Technical Stack
- **Python 3.12** + **Django 5.0** + **Wagtail 6.0**
- **PostgreSQL** database (SQLite for development)
- **Redis** for caching
- **Gunicorn** WSGI server
- **Docker** containerization
- **Fly.io** deployment ready

## 📋 Requirements

- Python 3.12+
- Poetry (for dependency management)
- PostgreSQL (for production)
- Redis (for caching)

## 🛠 Local Development

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Marketingnyt.dk

# Install dependencies and setup project
make setup
```

This will:
- Install Python dependencies via Poetry
- Copy `.env.example` to `.env`
- Run initial database migrations
- Create necessary directories

### 2. Configure Environment

Edit `.env` file with your settings:

```bash
# Basic settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - uses SQLite by default)
DATABASE_URL=postgres://user:password@localhost:5432/marketingnyt

# Redis (optional - uses dummy cache if not available)
REDIS_URL=redis://localhost:6379/0
```

### 3. Create Superuser and Sample Data

```bash
# Create admin user
make superuser

# Create sample categories and articles
poetry run python manage.py create_sample_data
```

### 4. Run Development Server

```bash
make run
```

Visit http://localhost:8000 to see the site and http://localhost:8000/admin/ for the Wagtail admin.

## 📝 Content Management

### Creating Articles

1. Go to Wagtail Admin (`/admin/`)
2. Navigate to Pages → Home
3. Add child page → Article Page
4. Fill in:
   - **Title**: Article headline
   - **Summary**: Brief description (used for meta description)
   - **Category**: Select from available categories
   - **Author**: Author name
   - **Cover Image**: Featured image
   - **Body**: Use StreamField blocks:
     - Rich Text: Regular content
     - Heading: H2/H3 headings
     - Quote: Pull quotes
     - Image: Images with captions
     - Callout: Highlighted information boxes
     - FAQ List: Frequently asked questions
   - **Tags**: Add relevant tags
   - **Is Featured**: Check to show on homepage

### Managing Categories

Categories are managed as Wagtail Snippets:
1. Go to Snippets → Categories
2. Add/edit categories with name, slug, and description

### Site Settings

Global settings are managed via Snippets → Site Settings:
- Site name and branding
- Default meta tags
- Social media handles
- Default OpenGraph image

## 🚀 Deployment

### Fly.io Deployment

1. **Install Fly.io CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   flyctl auth login
   flyctl launch --no-deploy
   ```

3. **Set Environment Variables**
   ```bash
   flyctl secrets set SECRET_KEY="your-production-secret-key"
   flyctl secrets set DATABASE_URL="your-postgres-url"
   flyctl secrets set REDIS_URL="your-redis-url"
   ```

4. **Deploy**
   ```bash
   flyctl deploy
   ```

### Environment Variables for Production

```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=marketingnyt.dk,your-domain.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/0
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

## 🌐 Domain Setup with Cloudflare

### 1. Add Domain to Fly.io
```bash
flyctl certs create marketingnyt.dk
flyctl certs create www.marketingnyt.dk
```

### 2. Configure Cloudflare DNS

Add these DNS records in Cloudflare (with proxy enabled):

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | @ | [Fly.io IPv4] | ✅ |
| AAAA | @ | [Fly.io IPv6] | ✅ |
| CNAME | www | marketingnyt.dk | ✅ |

### 3. Cloudflare Settings

- **SSL/TLS**: Full (strict)
- **Always Use HTTPS**: On
- **Auto Minify**: CSS, JavaScript, HTML
- **Brotli Compression**: On
- **Caching Level**: Standard

## 📊 SEO Setup

### 1. Google Search Console

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Add property: `https://marketingnyt.dk`
3. Verify ownership (DNS or HTML file method)
4. Submit sitemap: `https://marketingnyt.dk/sitemap.xml`

### 2. Google Analytics

Add your Google Analytics tracking code to the base template or use Google Tag Manager.

### 3. Social Media

Configure social media meta tags in Site Settings:
- Twitter handle
- Facebook page
- LinkedIn company page

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
poetry run pytest --cov=. --cov-report=html

# Run linting
make lint

# Format code
make format
```

## 📈 Performance Monitoring

### Core Web Vitals

Monitor your site's Core Web Vitals:
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

### Tools
- Google PageSpeed Insights
- Google Search Console Core Web Vitals report
- WebPageTest.org
- GTmetrix

## 🔧 Management Commands

### Import Articles
```bash
# Import from CSV
poetry run python manage.py import_articles articles.csv --format=csv --category=seo

# Import from Markdown
poetry run python manage.py import_articles articles.md --format=markdown
```

### Suggest Internal Links
```bash
# Generate link suggestions
poetry run python manage.py suggest_internal_links --min-score=0.3 --output-format=csv
```

### Create Sample Data
```bash
# Create sample categories and articles for development
poetry run python manage.py create_sample_data
```

## 🏗 Architecture

```
marketingnyt/
├── marketingnyt/          # Django project settings
│   ├── settings/          # Environment-specific settings
│   │   ├── base.py       # Base settings
│   │   ├── dev.py        # Development settings
│   │   ├── prod.py       # Production settings
│   │   └── test.py       # Test settings
│   ├── urls.py           # URL configuration
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
├── news/                  # Main app
│   ├── models.py         # Page models (HomePage, ArticlePage, etc.)
│   ├── blocks.py         # StreamField blocks
│   ├── views.py          # Custom views (robots.txt, sitemap, etc.)
│   ├── admin.py          # Wagtail admin configuration
│   ├── templatetags/     # Custom template tags
│   └── management/       # Management commands
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS, images)
├── Dockerfile           # Docker configuration
├── fly.toml            # Fly.io deployment config
└── pyproject.toml      # Python dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the [Django documentation](https://docs.djangoproject.com/)
- Check the [Wagtail documentation](https://docs.wagtail.org/)
- Review the [Fly.io documentation](https://fly.io/docs/)

---

Built with ❤️ for the Danish marketing community.
