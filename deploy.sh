#!/bin/bash

# Lifestyle Analytics Platform Deployment Script
# This script sets up the application for development or production

set -e  # Exit on any error

echo "🏋️‍♀️ Lifestyle Analytics Platform Deployment"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if Python is installed
check_python() {
    print_header "🐍 Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_status "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_header "📦 Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
        print_status "pip found: $PIP_VERSION"
    else
        print_error "pip3 is not installed. Please install pip3."
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_header "🔧 Setting up virtual environment..."
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_status "Virtual environment created successfully!"
    else
        print_warning "Virtual environment already exists."
    fi
}

# Activate virtual environment
activate_venv() {
    print_header "🚀 Activating virtual environment..."
    source venv/bin/activate
    print_status "Virtual environment activated!"
}

# Install dependencies
install_dependencies() {
    print_header "📚 Installing dependencies..."
    if [ -f "requirements.txt" ]; then
        print_status "Installing packages from requirements.txt..."
        pip install -r requirements.txt
        print_status "Dependencies installed successfully!"
    else
        print_error "requirements.txt not found!"
        exit 1
    fi
}

# Setup environment variables
setup_env() {
    print_header "⚙️ Setting up environment variables..."
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cat > .env << EOL
# Flask Configuration
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///lifestyle_analytics.db

# Email Configuration (Optional - for report sending)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Report Configuration
UPLOAD_FOLDER=reports
EOL
        print_status ".env file created with default values!"
        print_warning "Please update the email configuration in .env file if you want to send reports via email."
    else
        print_warning ".env file already exists. Skipping creation."
    fi
}

# Initialize database
init_database() {
    print_header "🗄️ Initializing database..."
    print_status "Creating database tables..."
    python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"
    print_status "Database initialized successfully!"
}

# Load sample data
load_sample_data() {
    print_header "📊 Loading sample data..."
    read -p "Do you want to load sample data for demonstration? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Loading sample data..."
        python3 init_sample_data.py
        print_status "Sample data loaded successfully!"
    else
        print_status "Skipping sample data loading."
    fi
}

# Create necessary directories
create_directories() {
    print_header "📁 Creating necessary directories..."
    mkdir -p reports
    mkdir -p static/uploads
    print_status "Directories created successfully!"
}

# Run the application
run_application() {
    print_header "🚀 Starting the application..."
    print_status "Application will be available at: http://localhost:5000"
    print_status "Press Ctrl+C to stop the application"
    echo
    python3 app.py
}

# Main deployment function
main() {
    print_header "🏋️‍♀️ Starting Lifestyle Analytics Platform Setup"
    echo
    
    # Check prerequisites
    check_python
    check_pip
    
    # Setup application
    create_venv
    activate_venv
    install_dependencies
    setup_env
    create_directories
    init_database
    load_sample_data
    
    echo
    print_header "✅ Setup completed successfully!"
    echo
    print_status "🔑 Demo Login Credentials (if sample data was loaded):"
    echo "   Beginner User - Email: demo@beginner.com, Password: demo123456"
    echo "   Advanced User - Email: demo@advanced.com, Password: demo123456"
    echo
    
    # Ask if user wants to start the application
    read -p "Do you want to start the application now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_application
    else
        print_status "Setup complete! Run 'python3 app.py' to start the application."
        print_status "Don't forget to activate the virtual environment: source venv/bin/activate"
    fi
}

# Handle script interruption
trap 'echo -e "\n${RED}[ERROR]${NC} Setup interrupted by user"; exit 1' INT

# Run main function
main "$@"