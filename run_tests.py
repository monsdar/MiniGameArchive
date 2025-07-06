#!/usr/bin/env python
"""
Test runner script for MiniGameArchive
"""
import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_command(command, description):
    """Run a command and handle errors"""
    logger.info(f"Running: {description}")
    logger.debug(f"Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=project_root
        )
        logger.info(f"✓ {description} completed successfully")
        if result.stdout:
            logger.debug(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} failed")
        logger.error(f"Error: {e.stderr}")
        return False


def run_django_tests(test_pattern=None, verbosity=2, coverage=False):
    """Run Django tests with optional coverage"""
    logger.info("Starting Django test suite...")
    
    # Set Django settings for testing
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.test_settings')
    
    # Build test command
    test_command = [
        sys.executable, 'manage.py', 'test',
        '--verbosity', str(verbosity),
        '--settings=tests.test_settings'
    ]
    
    if test_pattern:
        test_command.append(test_pattern)
    else:
        test_command.append('tests')
    
    # Add coverage if requested
    if coverage:
        try:
            import coverage
            logger.info("Running tests with coverage...")
            test_command = [
                sys.executable, '-m', 'coverage', 'run', '--source=.',
                'manage.py', 'test', '--verbosity', str(verbosity),
                '--settings=tests.test_settings'
            ]
            if test_pattern:
                test_command.append(test_pattern)
            else:
                test_command.append('tests')
        except ImportError:
            logger.warning("coverage package not installed, running tests without coverage")
    
    # Run tests
    success = run_command(test_command, "Django tests")
    
    # Generate coverage report if coverage was enabled
    if coverage and success:
        logger.info("Generating coverage report...")
        coverage_command = [sys.executable, '-m', 'coverage', 'report']
        run_command(coverage_command, "Coverage report")
        
        # Generate HTML coverage report
        logger.info("Generating HTML coverage report...")
        html_command = [sys.executable, '-m', 'coverage', 'html']
        run_command(html_command, "HTML coverage report")
    
    return success


def run_linting():
    """Run code linting checks"""
    logger.info("Running code linting...")
    
    # Check if flake8 is available
    try:
        import flake8
        flake8_command = [sys.executable, '-m', 'flake8', 'games', 'tests']
        success = run_command(flake8_command, "Flake8 linting")
    except ImportError:
        logger.warning("flake8 not installed, skipping linting")
        success = True
    
    return success


def run_security_checks():
    """Run security checks"""
    logger.info("Running security checks...")
    
    # Check if bandit is available
    try:
        import bandit
        bandit_command = [
            sys.executable, '-m', 'bandit', '-r', 'games',
            '-f', 'txt', '-o', 'bandit-report.txt'
        ]
        success = run_command(bandit_command, "Bandit security check")
    except ImportError:
        logger.warning("bandit not installed, skipping security checks")
        success = True
    
    return success


def check_dependencies():
    """Check if required dependencies are installed"""
    logger.info("Checking dependencies...")
    
    required_packages = [
        'django',
        'whitenoise',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.error("Please install them with: pip install -r requirements.txt")
        return False
    
    logger.info("✓ All required dependencies are installed")
    return True


def setup_test_environment():
    """Set up test environment"""
    logger.info("Setting up test environment...")
    
    # Create necessary directories
    directories = ['logs', 'media', 'staticfiles']
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
        logger.debug(f"Created directory: {dir_path}")
    
    # Run migrations for test database
    logger.info("Running migrations...")
    migrate_command = [
        sys.executable, 'manage.py', 'migrate',
        '--settings=tests.test_settings'
    ]
    success = run_command(migrate_command, "Database migrations")
    
    return success


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description='Run MiniGameArchive tests')
    parser.add_argument(
        '--test-pattern',
        help='Specific test pattern to run (e.g., tests.test_models)'
    )
    parser.add_argument(
        '--verbosity', '-v',
        type=int,
        default=2,
        help='Test verbosity (0-3)'
    )
    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='Run tests with coverage reporting'
    )
    parser.add_argument(
        '--lint', '-l',
        action='store_true',
        help='Run code linting'
    )
    parser.add_argument(
        '--security', '-s',
        action='store_true',
        help='Run security checks'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all checks (tests, linting, security)'
    )
    parser.add_argument(
        '--setup-only',
        action='store_true',
        help='Only set up test environment, don\'t run tests'
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("MiniGameArchive Test Runner")
    logger.info("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Set up test environment
    if not setup_test_environment():
        logger.error("Failed to set up test environment")
        sys.exit(1)
    
    if args.setup_only:
        logger.info("Test environment setup complete")
        return
    
    # Determine what to run
    run_tests = True
    run_lint = args.lint or args.all
    run_security = args.security or args.all
    
    success = True
    
    # Run linting
    if run_lint:
        if not run_linting():
            success = False
    
    # Run security checks
    if run_security:
        if not run_security_checks():
            success = False
    
    # Run tests
    if run_tests:
        if not run_django_tests(args.test_pattern, args.verbosity, args.coverage):
            success = False
    
    # Summary
    logger.info("=" * 60)
    if success:
        logger.info("✓ All checks passed!")
        sys.exit(0)
    else:
        logger.error("✗ Some checks failed!")
        sys.exit(1)


if __name__ == '__main__':
    main() 