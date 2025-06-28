#!/usr/bin/env python3
"""
Quick start script for Retro Platform Fighter - Diamond Quest
This script checks dependencies and runs the game with helpful error messages.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again")
        return False
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")
        return True

def check_dependency(package_name, install_name=None):
    """Check if a package is installed"""
    if install_name is None:
        install_name = package_name
    
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"❌ Missing dependency: {package_name}")
        print(f"   Install with: pip install {install_name}")
        return False
    else:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package_name}: {version}")
            return True
        except ImportError:
            print(f"❌ Error importing {package_name}")
            return False

def install_dependencies():
    """Attempt to install missing dependencies"""
    print("\n🔧 Attempting to install missing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies automatically")
        print("   Please run: pip install -r requirements.txt")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        print("   Please run: pip install pygame numpy")
        return False

def run_game():
    """Run the main game"""
    try:
        print("\n🎮 Starting Retro Platform Fighter - Diamond Quest...")
        import retro_platform_game
        retro_platform_game.main()
    except ImportError as e:
        print(f"❌ Error importing game: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running game: {e}")
        return False
    return True

def main():
    """Main function to check dependencies and run game"""
    print("🎮 Retro Platform Fighter - Diamond Quest")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📦 Checking dependencies...")
    
    # Check required dependencies
    dependencies_ok = True
    dependencies_ok &= check_dependency("pygame")
    dependencies_ok &= check_dependency("numpy")
    
    # If dependencies are missing, try to install them
    if not dependencies_ok:
        print("\n⚠️  Some dependencies are missing")
        response = input("Would you like to install them automatically? (y/n): ")
        if response.lower() in ['y', 'yes']:
            if not install_dependencies():
                print("\n❌ Please install dependencies manually and try again")
                sys.exit(1)
            
            # Re-check dependencies after installation
            print("\n📦 Re-checking dependencies...")
            dependencies_ok = True
            dependencies_ok &= check_dependency("pygame")
            dependencies_ok &= check_dependency("numpy")
            
            if not dependencies_ok:
                print("❌ Dependencies still missing after installation")
                sys.exit(1)
        else:
            print("❌ Cannot run game without required dependencies")
            sys.exit(1)
    
    # Test audio system
    print("\n🔊 Testing audio system...")
    try:
        import pygame
        pygame.mixer.init()
        print("✅ Audio system initialized successfully")
        pygame.mixer.quit()
    except Exception as e:
        print(f"⚠️  Audio system warning: {e}")
        print("   Game will run without sound")
    
    # Run the game
    if not run_game():
        print("\n❌ Failed to start game")
        print("   Check the console output above for error details")
        sys.exit(1)
    
    print("\n👋 Thanks for playing!")

if __name__ == "__main__":
    main()
