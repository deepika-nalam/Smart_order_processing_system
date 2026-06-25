# Smart Order Processing System

A scalable order processing backend built with Django REST Framework, featuring JWT authentication, product management, order lifecycle handling, payment processing, and inventory tracking.

## Tech Stack

- **Backend:** Python, Django REST Framework
- **Database:** PostgreSQL
- **Caching:** Redis
- **Task Queue:** Celery (async email notifications, background jobs)
- **Auth:** JWT (JSON Web Tokens)
- **Testing:** Pytest

## Features

- **User Authentication** — Register, login, and token refresh using JWT-based auth
- **Product Management** — CRUD operations with category filtering and Redis-cached retrieval
- **Order Processing** — Create orders, track status transitions, validate stock availability
- **Payment Processing** — Payment creation with database transactions ensuring atomicity and stock consistency
- **Inventory Tracking** — Real-time stock validation and automatic decrement on successful payment
- **Async Notifications** — Celery-powered email notifications for order confirmations and status updates

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│   Client    │────▶│  Django API  │────▶│PostgreSQL │
└─────────────┘     └──────┬───────┘     └───────────┘
                           │
                    ┌──────┴───────┐
                    │              │
               ┌────▼────┐   ┌────▼────┐
               │  Redis   │   │ Celery  │
               │ (Cache)  │   │ (Queue) │
               └──────────┘   └─────────┘
```

## Project Structure

```
├── accounts/          # User registration, login, JWT auth
├── products/          # Product CRUD, category management, caching
├── orders/            # Order creation, status management, validation
├── payment/           # Payment processing, stock transactions
├── smart_order_processing_system/  # Django settings, URLs, Celery config
├── pytest.ini         # Test configuration
└── manage.py
```

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis

### Installation

```bash
# Clone the repository
git clone https://github.com/deepika-nalam/Smart_order_processing_system.git
cd Smart_order_processing_system

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file)
# DB_NAME=smart_orders_db
# DB_USER=smart_user
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5433
# REDIS_URL=redis://localhost:6379/0

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

### Running Tests

```bash
pytest
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/accounts/register/` | POST | User registration |
| `/api/accounts/login/` | POST | JWT token pair |
| `/api/accounts/token/refresh/` | POST | Refresh access token |
| `/api/products/` | GET, POST | List/create products |
| `/api/products/<id>/` | GET, PUT, DELETE | Product detail |
| `/api/orders/` | GET, POST | List/create orders |
| `/api/orders/<id>/` | GET, PUT | Order detail/status update |
| `/api/payment/` | POST | Process payment |

## Key Design Decisions

- **Database Transactions:** Payment processing uses `select_for_update()` to prevent race conditions during concurrent stock updates
- **Redis Caching:** Product listings are cached with TTL-based invalidation to reduce DB load
- **Celery Workers:** Email notifications are offloaded to background workers to keep API response times fast
- **Stock Validation:** Orders are validated against available inventory at creation time and again at payment time (double-check pattern)

## License

MIT
