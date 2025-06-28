# Installation Guide

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 7+, macOS 10.12+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 512 MB available memory
- **Storage**: 50 MB free disk space
- **Graphics**: Any graphics card supporting 1024x768 resolution
- **Audio**: Sound card (optional - game works without audio)

### Recommended Requirements
- **Python**: 3.9 or higher
- **RAM**: 1 GB available memory
- **Storage**: 100 MB free disk space
- **Graphics**: Dedicated graphics card
- **Audio**: Stereo sound system or headphones

## 🚀 Installation Methods

### Method 1: Quick Install (Recommended)

1. **Download Python** (if not already installed):
   - Visit [python.org](https://python.org/downloads/)
   - Download Python 3.8 or higher
   - Install with "Add to PATH" option checked

2. **Download the Game**:
   ```bash
   git clone <repository-url>
   cd retro-platform
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Game**:
   ```bash
   python retro_platform_game.py
   ```

### Method 2: Virtual Environment (Recommended for Developers)

1. **Create Virtual Environment**:
   ```bash
   python -m venv retro-game-env
   ```

2. **Activate Virtual Environment**:
   
   **Windows:**
   ```cmd
   retro-game-env\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source retro-game-env/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Game**:
   ```bash
   python retro_platform_game.py
   ```

5. **Deactivate When Done**:
   ```bash
   deactivate
   ```

### Method 3: System-Wide Install

1. **Install Dependencies Globally**:
   ```bash
   pip install pygame>=2.5.0 numpy>=1.21.0
   ```

2. **Run the Game**:
   ```bash
   python retro_platform_game.py
   ```

## 🔧 Platform-Specific Instructions

### Windows

#### Using Command Prompt:
```cmd
# Check Python version
python --version

# Install pip if not available
python -m ensurepip --upgrade

# Install game dependencies
pip install pygame numpy

# Run the game
python retro_platform_game.py
```

#### Using PowerShell:
```powershell
# Same commands as Command Prompt
python --version
pip install pygame numpy
python retro_platform_game.py
```

### macOS

#### Using Terminal:
```bash
# Check Python version
python3 --version

# Install dependencies
pip3 install pygame numpy

# Run the game
python3 retro_platform_game.py
```

#### Using Homebrew (if installed):
```bash
# Install Python via Homebrew
brew install python

# Install dependencies
pip3 install pygame numpy

# Run the game
python3 retro_platform_game.py
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install system dependencies for pygame
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Install game dependencies
pip3 install pygame numpy

# Run the game
python3 retro_platform_game.py
```

### Linux (CentOS/RHEL/Fedora)

```bash
# Install Python and pip
sudo dnf install python3 python3-pip

# Install system dependencies
sudo dnf install python3-devel SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel

# Install game dependencies
pip3 install pygame numpy

# Run the game
python3 retro_platform_game.py
```

## 🐛 Troubleshooting Installation

### Common Issues and Solutions

#### Issue: "python: command not found"
**Solution:**
- **Windows**: Reinstall Python with "Add to PATH" checked
- **macOS/Linux**: Use `python3` instead of `python`

#### Issue: "pip: command not found"
**Solution:**
```bash
# Install pip
python -m ensurepip --upgrade

# Or use python3
python3 -m ensurepip --upgrade
```

#### Issue: "Permission denied" when installing packages
**Solution:**
```bash
# Use --user flag
pip install --user pygame numpy

# Or use virtual environment (recommended)
python -m venv game-env
source game-env/bin/activate  # Linux/macOS
# or
game-env\Scripts\activate     # Windows
pip install pygame numpy
```

#### Issue: pygame installation fails on Linux
**Solution:**
```bash
# Install system dependencies first
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Then install pygame
pip3 install pygame
```

#### Issue: "No module named 'numpy'"
**Solution:**
```bash
# Install numpy explicitly
pip install numpy>=1.21.0

# Verify installation
python -c "import numpy; print('NumPy version:', numpy.__version__)"
```

#### Issue: Game runs but no sound
**Causes and Solutions:**
- **Audio drivers**: Update your audio drivers
- **Audio device**: Ensure audio device is working
- **Permissions**: Check audio permissions for Python
- **Dependencies**: Reinstall pygame with audio support

#### Issue: Game window doesn't appear
**Solutions:**
- Check if window is minimized or behind other windows
- Try running in windowed mode
- Update graphics drivers
- Check display resolution settings

## ✅ Verification

### Test Your Installation

1. **Test Python**:
   ```bash
   python --version
   # Should show Python 3.8 or higher
   ```

2. **Test pygame**:
   ```bash
   python -c "import pygame; print('Pygame version:', pygame.version.ver)"
   ```

3. **Test numpy**:
   ```bash
   python -c "import numpy; print('NumPy version:', numpy.__version__)"
   ```

4. **Test Audio**:
   ```bash
   python -c "import pygame; pygame.mixer.init(); print('Audio system OK')"
   ```

5. **Run the Game**:
   ```bash
   python retro_platform_game.py
   ```

### Expected Output
When you run the game, you should see:
- A game window opens (1024x768 resolution)
- Sound loading messages in console
- Game starts with level 1
- Player character appears on screen
- Sound effects play when jumping/moving

## 🔄 Updating

### Update Dependencies
```bash
# Update to latest versions
pip install --upgrade pygame numpy

# Or update specific package
pip install --upgrade pygame
```

### Update Game
```bash
# Pull latest changes (if using git)
git pull origin main

# Check for new dependencies
pip install -r requirements.txt
```

## 🗑️ Uninstallation

### Remove Virtual Environment
```bash
# Deactivate if active
deactivate

# Remove directory
rm -rf retro-game-env  # Linux/macOS
rmdir /s retro-game-env  # Windows
```

### Remove System-Wide Packages
```bash
pip uninstall pygame numpy
```

### Remove Game Files
```bash
# Remove game directory
rm -rf retro-platform  # Linux/macOS
rmdir /s retro-platform  # Windows
```

## 📞 Support

If you encounter issues not covered here:

1. **Check Console Output**: Look for error messages
2. **Verify Requirements**: Ensure all dependencies are installed
3. **Try Virtual Environment**: Isolate from system packages
4. **Update Everything**: Update Python, pip, and packages
5. **Check Documentation**: Review other .md files in the project

For persistent issues, please create an issue in the repository with:
- Your operating system and version
- Python version (`python --version`)
- Error messages (full traceback)
- Steps you've already tried
