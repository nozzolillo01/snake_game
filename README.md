# Flask Game Application

A Flask-based web application featuring a snake game with user dashboard and security features.

## Features

- Snake game implementation
- User dashboard
- Rate limiting protection
- Security headers
- CORS support
- WebSocket integration
- Logging system
- Database integration
- Environment configuration

## Prerequisites

- Python 3.11+
- Redis (for rate limiting)
- SQLite (for database)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
FLASK_ENV=development  # or production
```

## Project Structure

```
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── database.py         # Database initialization
├── requirements.txt    # Project dependencies
├── routes/            
│   ├── dashboard.py    # Dashboard routes
│   └── game.py        # Game routes
├── static/
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── templates/          # HTML templates
└── utils/
    └── logging_config.py  # Logging configuration
```

## Security Features

- Rate limiting (200 requests per day, 50 per hour)
- Security headers:
  - X-Content-Type-Options
  - X-Frame-Options
  - X-XSS-Protection
  - Content-Security-Policy
  - Strict-Transport-Security
  - X-Permitted-Cross-Domain-Policies
  - Referrer-Policy
  - Cache-Control

## API Rate Limits

- Default: 200 requests per day
- Hourly: 50 requests per hour

## Running the Application

Development mode:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Logging

Logs are stored in the `logs/` directory:
- `app.log`: Application logs
- `security.log`: Security-related events

## Error Handling

- Rate limit exceeded (429)
- Internal Server Error (500)

## WebSocket Events

The application uses Flask-SocketIO for real-time communication.

## Database

SQLite database (`game.db`) is used for data storage.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License.