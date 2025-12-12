#!/usr/bin/env python3
"""
PostgreSQL Setup Script for HealNovaAI
This script helps set up PostgreSQL database for the application.
"""

import os
import sys
import subprocess
import time

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def setup_postgresql():
    """Set up PostgreSQL database for HealNovaAI."""
    print("🚀 Setting up PostgreSQL for HealNovaAI...")

    # Check if PostgreSQL is installed
    print("\n📋 Checking PostgreSQL installation...")

    # Try to find psql
    psql_paths = [
        r"C:\Program Files\PostgreSQL\15\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\14\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\13\bin\psql.exe",
        r"C:\Program Files (x86)\PostgreSQL\15\bin\psql.exe",
        r"C:\Program Files (x86)\PostgreSQL\14\bin\psql.exe",
        r"C:\Program Files (x86)\PostgreSQL\13\bin\psql.exe",
    ]

    psql_path = None
    for path in psql_paths:
        if os.path.exists(path):
            psql_path = path
            break

    if not psql_path:
        print("❌ PostgreSQL not found. Please install PostgreSQL first:")
        print("1. Download from: https://www.postgresql.org/download/windows/")
        print("2. Install with default settings")
        print("3. Note the password you set for the 'postgres' user")
        print("4. Run this script again")
        return False

    print(f"✅ Found PostgreSQL at: {psql_path}")

    # Get database credentials
    print("\n📝 Database Configuration:")
    db_user = input("Enter PostgreSQL username (default: postgres): ").strip() or "postgres"
    db_password = input("Enter PostgreSQL password: ").strip()
    db_name = input("Enter database name (default: healnova_db): ").strip() or "healnova_db"
    db_host = input("Enter database host (default: localhost): ").strip() or "localhost"
    db_port = input("Enter database port (default: 5432): ").strip() or "5432"

    if not db_password:
        print("❌ Password is required")
        return False

    # Create database URI
    database_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Test connection and create database
    print("\n🔍 Testing database connection...")

    # Create database if it doesn't exist
    create_db_cmd = f'"{psql_path}" -U {db_user} -h {db_host} -p {db_port} -c "CREATE DATABASE {db_name};"'
    result = run_command(create_db_cmd, "Creating database")

    if not result:
        print("⚠️  Database might already exist, continuing...")

    # Test connection
    test_cmd = f'"{psql_path}" -U {db_user} -h {db_host} -p {db_port} -d {db_name} -c "SELECT version();"'
    if run_command(test_cmd, "Testing database connection"):
        print("✅ Database connection successful!")

        # Update Flask configuration
        print("\n📝 Updating Flask configuration...")

        app_py_path = os.path.join(os.path.dirname(__file__), 'app.py')
        with open(app_py_path, 'r') as f:
            content = f.read()

        # Replace the database URI
        old_uri = "app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/healnova_db'"
        new_uri = f"app.config['SQLALCHEMY_DATABASE_URI'] = '{database_uri}'"

        if old_uri in content:
            content = content.replace(old_uri, new_uri)

            with open(app_py_path, 'w') as f:
                f.write(content)

            print("✅ Flask configuration updated!")

            # Create tables
            print("\n📋 Creating database tables...")
            print("Run the following command to start the Flask app and create tables:")
            print("cd Backend && python app.py")
            print("\nThe app will automatically create all required tables on first run.")

            return True
        else:
            print("❌ Could not find database URI in app.py")
            return False
    else:
        print("❌ Database connection failed. Please check your credentials.")
        return False

if __name__ == "__main__":
    print("🩺 HealNovaAI PostgreSQL Setup")
    print("=" * 40)

    success = setup_postgresql()

    if success:
        print("\n🎉 PostgreSQL setup completed successfully!")
        print("\nNext steps:")
        print("1. Start the Flask backend: cd Backend && python app.py")
        print("2. Start the React frontend: cd client && npm run dev")
        print("3. Open http://localhost:8080 in your browser")
    else:
        print("\n❌ PostgreSQL setup failed. Please check the errors above.")
        sys.exit(1)