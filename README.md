# MiniGameArchive

This project is the MiniGameArchive. A Django website to manage games and exercises you can do with your sports team during training sessions. I'm a Basketball trainer myself, but the project can be used to manage games of all sorts.

It features:
* A backend to manage exercises
* A front page that let's you filter and search through the exercises
* A detail page that shows the exercise with everything you need to know
* The ability to add exercises to a training plan, so you can easily create plans for the next training session
* The ability to print single exercises or training plans so you have everything available in your next training session

## What is a Game?

A game, or an exercise, is something you can do with your team during your training sessions. It's a small competition you run or something that helps the players get better at a specific skill.

It typically consists of the following information:

* **Name:** Short descriptive name of the game. Example: "Fruit Bowl"
* **Focus:** What is this game focusing on? Example: "Dribbling, Teamwork, Layups, ...". Could be multiple depending on the exercise.
* **Description:** Detailed description. At best these are in short list format, so that during the training session you can glance over the game card and see what it's about
* **Player number:** For how many players is the exercise? It it done by just 1 or 2 players, or do you need a bigger group, like a 8+ game? When it's only a few player you can decide to split a larger group into many subgroups all doing the exercise on their own
* **Variants:** These are variations that add new aspects to the exercise, making it more fun or harder for better players
* **Material:** What is needed to do the exercise? Example: Basketball, Halfcourt, Hoop, Wall, ...
* **Duration:** Typical duration of the exercise (5min, 10+ min, ...)
* **Labels:** Additional, custom labels are helping to sort and filter the exercises

## What is a Training Session?

A training session typically consists of multiple games. It typically has a structure like first playing a warmup game, then focusing on 1-2 specific skillsets and in the end do a cool-down game.

## Managing the Games

The page provides a full backend to manage the data. Users that do not have access to the backend can enter their suggestions through the frontends, which an admin can then review and release into the database.

## Using the site for preparation

The typical user-flow let's the coach search and filter for games. When he finds one that he'd like to run, he can add it to a Training Session (this is designed to work like a shopping card on an E-Commerce site). When he finished the session he can decide to print out game cards for the single games and session card for the whole training session. That way he has everything available when he's running the actual practice session.

The printouts are designed to be printed in business card format (front and back page), so it's easy to have them on hand and give some help when checking for the details while working with the team.

## Technology Stack

* **Backend:** Django 5.0
* **Frontend:** Bootstrap 5 + Alpine.js
* **Database:** SQLite (default) or PostgreSQL
* **Deployment:** Docker

## Features

### Frontend Features
- **Responsive Design:** Works on desktop, tablet, and mobile devices
- **Real-time Filtering:** Alpine.js-powered filtering and search
- **Shopping Cart:** Add games to training sessions like an e-commerce site
- **Print Functionality:** Business card format printing for games and sessions
- **Modern UI:** Clean, intuitive interface with Bootstrap 5

### Backend Features
- **Game Management:** Full CRUD operations for games
- **User Suggestions:** Public can suggest new games for admin review
- **Training Sessions:** Create and manage training plans
- **Admin Interface:** Comprehensive Django admin panel
- **Session-based Cart:** Persistent cart functionality

## Installation

### Quick Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MiniGameArchive
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

4. **Access the application:**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/
   - Admin credentials: admin/admin123

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Load sample data:**
   ```bash
   python manage.py load_sample_data
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Docker Deployment

The website comes in a Docker container and can be simply started by running the following command:

```bash
docker run -it -v ./data:/data -p 8080:8080 monsdar/minigamearchive:latest
```

### Environment Variables

By default it uses SQLite to store data, but you can also connect it to a Postgres DB by using the following env vars:

* `POSTGRES_HOST`
* `POSTGRES_PORT`
* `POSTGRES_DB`
* `POSTGRES_USER`
* `POSTGRES_PASSWORD`

The following configuration options are available as well via env vars:

* `DJANGO_ALLOWED_HOSTS`: Set this to the host address you'd like to run the page under
* `DJANGO_PRODUCTION`: Set this to any value to have the application run in production mode. Else debugging will be enabled
* `DJANGO_SECRET_KEY`: Set your own Django secret key. Should be at least 32 char in length
* `DJANGO_CSRF_TRUSTED_ORIGINS`: Define which addresses the page trusts for loading scripts etc

## Usage

### For Coaches

1. **Browse Games:** Visit the main page to see all available games
2. **Filter & Search:** Use the sidebar filters to find specific types of games
3. **Add to Cart:** Click "Add to Cart" on games you want to include
4. **Create Session:** Go to your cart and create a training session
5. **Print:** Print individual game cards or the entire session

### For Administrators

1. **Access Admin:** Login to the Django admin panel
2. **Manage Games:** Add, edit, or remove games
3. **Review Suggestions:** Approve or reject user-submitted games
4. **Manage Categories:** Add focus areas, materials, and labels

## Development

### Project Structure

```
MiniGameArchive/
├── minigamearchive/          # Django project settings
├── games/                    # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Forms
│   ├── admin.py             # Admin interface
│   └── management/          # Custom commands
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   └── games/              # Game-specific templates
├── static/                  # Static files (CSS, JS)
├── tests/                   # Test suite
│   ├── test_models.py      # Model tests
│   ├── test_views.py       # View tests
│   ├── test_forms.py       # Form tests
│   ├── test_management_commands.py # Management command tests
│   ├── test_utils.py       # Utility tests
│   └── test_settings.py    # Test-specific settings
├── data/                    # Database and media files
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── setup.py                # Setup script
└── run_tests.py            # Test runner script
```

### Adding New Features

1. **Models:** Add new fields to `games/models.py`
2. **Views:** Create new views in `games/views.py`
3. **Templates:** Add templates in `templates/games/`
4. **URLs:** Update `games/urls.py` with new routes
5. **Admin:** Register new models in `games/admin.py`
6. **Tests:** Add corresponding tests in the `tests/` directory

### Testing

The project includes a comprehensive test suite to ensure code quality and prevent regressions.

#### Running Tests
```bash
# Run all tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage

# Run specific test file
python run_tests.py --test-pattern tests.test_models

# Run all checks (tests, linting, security)
python run_tests.py --all
```

#### Test Coverage
The test suite covers:
- **Models**: Database operations, relationships, validation
- **Views**: HTTP responses, authentication, business logic
- **Forms**: Validation, data processing, error handling
- **Management Commands**: Command execution, error handling
- **Utilities**: Helper functions, configuration

For detailed testing information, see [tests/README.md](tests/README.md).

## Support

Feel free to open GitHub issues whenever you find an issue or look for an improvement. If you'd like to support my work in general consider [buying me a coffee](https://buymeacoffee.com/monsdar) ☕.
