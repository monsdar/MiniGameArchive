# MiniGameArchive Test Suite

This directory contains the comprehensive test suite for the MiniGameArchive Django project. The tests are designed to ensure code quality, prevent regressions, and maintain the reliability of the application.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_models.py             # Model tests (database, relationships, validation)
├── test_views.py              # View tests (HTTP responses, authentication, business logic)
├── test_forms.py              # Form tests (validation, data processing)
├── test_management_commands.py # Management command tests
├── test_utils.py              # Utility function tests
├── test_settings.py           # Test-specific Django settings
└── README.md                  # This documentation
```

## Test Categories

### 1. Model Tests (`test_models.py`)
- **FocusModelTest**: Tests for the Focus model (creation, uniqueness, ordering)
- **MaterialModelTest**: Tests for the Material model
- **LabelModelTest**: Tests for the Label model
- **GameModelTest**: Tests for the Game model (CRUD operations, relationships, search)
- **TrainingSessionModelTest**: Tests for training session management
- **SessionGameModelTest**: Tests for session-game relationships
- **ModelIntegrationTest**: Integration tests for model relationships

### 2. View Tests (`test_views.py`)
- **GameListViewTest**: Tests for game listing and filtering
- **GameDetailViewTest**: Tests for game detail pages
- **CartViewTest**: Tests for training session cart functionality
- **CartAPITest**: Tests for cart API endpoints
- **LanguageViewTest**: Tests for language switching
- **SessionViewTest**: Tests for training session management
- **GameSuggestionViewTest**: Tests for game suggestion functionality
- **PrintViewTest**: Tests for print functionality
- **AuthenticationTest**: Tests for authentication requirements
- **InternationalizationTest**: Tests for i18n functionality

### 3. Form Tests (`test_forms.py`)
- **GameFormTest**: Tests for game creation and editing forms
- **TrainingSessionFormTest**: Tests for training session forms
- **GameSuggestionFormTest**: Tests for game suggestion forms
- **FormIntegrationTest**: Integration tests for forms with models

### 4. Management Command Tests (`test_management_commands.py`)
- **LoadSampleDataCommandTest**: Tests for sample data loading
- **TestI18nCommandTest**: Tests for internationalization commands
- **ManagementCommandIntegrationTest**: Integration tests for commands
- **ManagementCommandErrorHandlingTest**: Error handling tests
- **ManagementCommandPerformanceTest**: Performance tests
- **ManagementCommandLoggingTest**: Logging tests

### 5. Utility Tests (`test_utils.py`)
- **TranslationCompilationTest**: Tests for translation compilation
- **LoggingUtilityTest**: Tests for logging configuration
- **InternationalizationUtilityTest**: Tests for i18n utilities
- **FileUtilityTest**: Tests for file operations
- **ConfigurationTest**: Tests for Django settings

## Running Tests

### Quick Start
```bash
# Run all tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage

# Run specific test file
python run_tests.py --test-pattern tests.test_models

# Run with verbose output
python run_tests.py --verbosity 3
```

### Using Django's Test Runner
```bash
# Run all tests
python manage.py test tests --settings=tests.test_settings

# Run specific test class
python manage.py test tests.test_models.GameModelTest --settings=tests.test_settings

# Run specific test method
python manage.py test tests.test_models.GameModelTest.test_game_creation --settings=tests.test_settings

# Run with coverage
coverage run --source=. manage.py test tests --settings=tests.test_settings
coverage report
coverage html
```

### Advanced Options
```bash
# Run all checks (tests, linting, security)
python run_tests.py --all

# Run only linting
python run_tests.py --lint

# Run only security checks
python run_tests.py --security

# Set up test environment only
python run_tests.py --setup-only
```

## Test Configuration

### Test Settings (`test_settings.py`)
The test settings provide:
- In-memory SQLite database for fast test execution
- Disabled migrations for faster setup
- Test-specific logging configuration
- Simplified middleware stack
- Test-specific static and media file handling

### Environment Variables
Tests use the following environment variables:
- `DJANGO_SETTINGS_MODULE=tests.test_settings`
- `DJANGO_DEBUG=True`

## Test Data

### Fixtures
Tests create their own test data using Django's `setUp()` methods. This ensures:
- Tests are isolated and independent
- No reliance on external data
- Fast test execution
- Predictable test results

### Sample Data
The `load_sample_data` management command is tested to ensure it:
- Creates all required data types
- Establishes proper relationships
- Handles duplicate data gracefully
- Performs within acceptable time limits

## Coverage

### Code Coverage
The test suite aims for high code coverage:
- **Models**: 100% coverage of model methods and relationships
- **Views**: 95%+ coverage of view logic and error handling
- **Forms**: 100% coverage of form validation and processing
- **Management Commands**: 100% coverage of command functionality

### Coverage Reports
```bash
# Generate coverage report
python run_tests.py --coverage

# View HTML coverage report
open htmlcov/index.html
```

## Best Practices

### Test Organization
1. **One test class per model/view/form**
2. **Descriptive test method names** (e.g., `test_game_creation_with_valid_data`)
3. **Comprehensive docstrings** explaining test purpose
4. **Proper setup and teardown** methods

### Test Data Management
1. **Use setUp() for common test data**
2. **Create minimal test data** for each test
3. **Clean up after tests** (Django handles this automatically)
4. **Use factories for complex objects** when needed

### Assertions
1. **Test one thing per test method**
2. **Use specific assertions** (e.g., `assertContains` for responses)
3. **Test both positive and negative cases**
4. **Verify side effects** (e.g., database changes)

### Performance
1. **Use in-memory database** for fast execution
2. **Disable migrations** during tests
3. **Minimize database queries** in tests
4. **Use bulk operations** when creating test data

## Continuous Integration

### GitHub Actions
The test suite is designed to run in CI/CD pipelines:
```yaml
- name: Run tests
  run: python run_tests.py --all
```

### Pre-commit Hooks
Consider adding pre-commit hooks to run tests before commits:
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: django-tests
        name: Django Tests
        entry: python run_tests.py
        language: system
        pass_filenames: false
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure you're in the project root
cd /path/to/MiniGameArchive

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

#### Database Issues
```bash
# Reset test database
python manage.py flush --settings=tests.test_settings

# Run migrations
python manage.py migrate --settings=tests.test_settings
```

#### Coverage Issues
```bash
# Install coverage
pip install coverage

# Clear coverage data
coverage erase
```

### Debugging Tests
```bash
# Run single test with debug output
python manage.py test tests.test_models.GameModelTest.test_game_creation --settings=tests.test_settings -v 3

# Use pdb for debugging
python -m pdb manage.py test tests.test_models --settings=tests.test_settings
```

## Adding New Tests

### For New Models
1. Create test class in `test_models.py`
2. Test CRUD operations
3. Test relationships and constraints
4. Test model methods
5. Test validation rules

### For New Views
1. Create test class in `test_views.py`
2. Test HTTP responses
3. Test authentication requirements
4. Test business logic
5. Test error handling

### For New Forms
1. Create test class in `test_forms.py`
2. Test validation
3. Test data processing
4. Test error messages
5. Test form submission

### For New Management Commands
1. Create test class in `test_management_commands.py`
2. Test command execution
3. Test error handling
4. Test output formatting
5. Test performance

## Test Maintenance

### Regular Tasks
1. **Update tests** when models/views change
2. **Review coverage reports** monthly
3. **Remove obsolete tests** when features are removed
4. **Add tests** for new features before implementation

### Performance Monitoring
1. **Monitor test execution time**
2. **Identify slow tests** and optimize
3. **Use parallel test execution** when possible
4. **Profile test database usage**

## Resources

### Documentation
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

### Tools
- **coverage**: Code coverage measurement
- **flake8**: Code linting
- **bandit**: Security linting
- **pytest**: Alternative test runner (optional)

### Best Practices
- [Testing Django Applications](https://docs.djangoproject.com/en/stable/topics/testing/overview/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) 