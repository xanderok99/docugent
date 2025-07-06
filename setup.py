#!/usr/bin/env python3
"""
Setup script for the API Conference AI Agent.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def check_poetry():
    """Check if Poetry is installed."""
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
        print("✅ Poetry is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Poetry is not installed")
        print("Please install Poetry: https://python-poetry.org/docs/#installation")
        return False

def setup_environment():
    """Set up the environment file."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from template...")
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your API keys and configuration")
        else:
            print("❌ env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def install_dependencies():
    """Install project dependencies."""
    return run_command("poetry install", "Installing dependencies")

def create_data_directories():
    """Create necessary data directories."""
    data_dir = Path("data")
    logs_dir = Path("logs")
    
    data_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    
    print("✅ Data directories created")
    return True

def run_tests():
    """Run the test suite."""
    return run_command("poetry run pytest tests/ -v", "Running tests")

def main():
    """Main setup function."""
    print("🚀 Setting up API Conference AI Agent...")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_poetry():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Setting up environment", setup_environment),
        ("Creating data directories", create_data_directories),
        ("Installing dependencies", install_dependencies),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    # Optional: Run tests
    print("\n🧪 Running tests...")
    if run_tests():
        print("✅ All tests passed")
    else:
        print("⚠️  Some tests failed, but setup completed")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: poetry run python main.py")
    print("3. Visit: http://localhost:8000/docs")
    print("\n📞 For support, check the README.md file")

if __name__ == "__main__":
    main() 