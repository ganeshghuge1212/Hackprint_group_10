#!/bin/bash
# Automated Setup Script for Helix RAG System
# This script automates the setup process

set -e  # Exit on error

echo "============================================================"
echo "  HELIX RAG SYSTEM - AUTOMATED SETUP"
echo "============================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check MongoDB
echo ""
echo "Checking MongoDB installation..."
if command -v mongo &> /dev/null || command -v mongod &> /dev/null; then
    print_success "MongoDB found"
    
    # Try to start MongoDB if not running
    if ! pgrep -x "mongod" > /dev/null; then
        print_info "Starting MongoDB..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew services start mongodb-community &> /dev/null || true
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo systemctl start mongodb &> /dev/null || true
        fi
    fi
else
    print_error "MongoDB is not installed!"
    echo "Please install MongoDB first:"
    echo "  - Mac: brew install mongodb-community"
    echo "  - Linux: sudo apt-get install mongodb"
    echo "  - Windows: Download from mongodb.com"
    exit 1
fi

# Create virtual environment
echo ""
echo "Setting up Python virtual environment..."
if [ -d "venv" ]; then
    print_info "Virtual environment already exists"
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
echo ""
print_info "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "Installing Python packages..."
echo "This may take 5-10 minutes..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
print_success "All packages installed"

# Create data directory
echo ""
echo "Setting up directories..."
mkdir -p data
mkdir -p faiss_indexes
mkdir -p logs
print_success "Directories created"

# Check for data files
echo ""
echo "Checking data files..."
MISSING_FILES=()
if [ ! -f "data/employee_master.csv" ]; then
    MISSING_FILES+=("employee_master.csv")
fi
if [ ! -f "data/attendance_logs_detailed.json" ]; then
    MISSING_FILES+=("attendance_logs_detailed.json")
fi
if [ ! -f "data/leave_intelligence.xlsx" ]; then
    MISSING_FILES+=("leave_intelligence.xlsx")
fi

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    print_error "Missing data files in data/ directory:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    print_info "Please copy your data files to the data/ directory"
    echo "Then run this script again or proceed to manual setup"
else
    print_success "All required data files found"
fi

# Check for API key
echo ""
echo "Checking Groq API key..."
if [ -z "$GROQ_API_KEY" ]; then
    print_error "GROQ_API_KEY environment variable not set"
    echo ""
    echo "Please get your API key from: https://console.groq.com"
    echo "Then set it:"
    echo "  export GROQ_API_KEY='your_key_here'"
    echo ""
    read -p "Enter your Groq API key now (or press Enter to skip): " API_KEY
    if [ ! -z "$API_KEY" ]; then
        export GROQ_API_KEY="$API_KEY"
        echo "GROQ_API_KEY=$API_KEY" > .env
        print_success "API key saved to .env file"
    else
        print_info "You can set it later before running the system"
    fi
else
    print_success "GROQ_API_KEY is set"
fi

# Summary
echo ""
echo "============================================================"
echo "  SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
if [ ${#MISSING_FILES[@]} -eq 0 ] && [ ! -z "$GROQ_API_KEY" ]; then
    echo "1. Load data into the system:"
    echo "   python ingest_data.py"
    echo ""
    echo "2. Start querying:"
    echo "   python query_interface.py"
else
    if [ ${#MISSING_FILES[@]} -gt 0 ]; then
        echo "1. Copy data files to data/ directory"
    fi
    if [ -z "$GROQ_API_KEY" ]; then
        echo "2. Set your Groq API key:"
        echo "   export GROQ_API_KEY='your_key_here'"
    fi
    echo "3. Run data ingestion:"
    echo "   python ingest_data.py"
    echo ""
    echo "4. Start querying:"
    echo "   python query_interface.py"
fi
echo ""
echo "For detailed instructions, see:"
echo "  - README.md (full documentation)"
echo "  - BEGINNER_GUIDE.md (step-by-step tutorial)"
echo ""
print_success "Happy querying! 🚀"
