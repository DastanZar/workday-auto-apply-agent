#!/bin/bash
echo "Workday Automation Tool - Linux/macOS Installation"
echo "=================================================="

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Creating configuration file..."
if [ ! -f config.json ]; then
    cp config/config_template.json config.json
    echo "Configuration file created: config.json"
    echo "Please edit config.json with your credentials and job URLs"
else
    echo "Configuration file already exists"
fi

echo ""
echo "Making run script executable..."
chmod +x run.py

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.json with your credentials"
echo "2. Add job URLs to the configuration"
echo "3. Run: python3 run.py"
echo ""
