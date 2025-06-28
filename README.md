# 🎮 Retro Platform Fighter - Diamond Quest

A classic 2D platformer game built with Python and Pygame, featuring 10 challenging levels, power-ups, combat mechanics, and procedurally generated sound effects.

![Game Screenshot](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 🎯 Core Gameplay
- **10 Progressive Levels** with increasing difficulty
- **Combat System** with punch and kick attacks
- **Diamond Collection** with regular and super diamonds
- **Power-Up System** with 4 different abilities
- **Boss Battles** at the end of each level
- **Lives System** with respawning mechanics

### 🔊 Audio System
- **13 Sound Effects** including combat, collection, and power-up sounds
- **Procedural Sound Generation** using mathematical algorithms
- **Dynamic Audio** that responds to game events

### 💎 Power-Up System
- **Speed Boost** (Yellow) - 80% movement speed increase
- **Jump Boost** (Green) - 40% jump height increase  
- **Invincibility** (Magenta) - Complete damage immunity
- **Strength** (Orange) - Increased attack damage

### 🤖 Enemy AI
- **Smart Robots** with patrol and chase behaviors
- **Adaptive Bosses** with multiple attack patterns
- **Difficulty Scaling** based on level progression

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd retro-platform
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python retro_platform_game.py
   ```

### Alternative Installation (using virtual environment)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python retro_platform_game.py
```

## 🎮 How to Play

### Controls
| Key | Action |
|-----|--------|
| **Arrow Keys** or **WASD** | Move and Jump |
| **Spacebar** | Jump |
| **X** | Punch |
| **Z** | Kick |
| **ESC** | Quit Game |
| **R** | Restart (Game Over screen) |
| **Enter** | Next Level (Level Complete screen) |

### Gameplay Mechanics

#### 🏃 Movement
- Use arrow keys or WASD to move left/right
- Jump with Spacebar, Up Arrow, or W key
- Player has realistic physics with gravity and momentum

#### ⚔️ Combat
- **Punch (X)**: Quick attack with moderate damage
- **Kick (Z)**: Slower attack with higher damage
- Attacks must be within range and at similar height to enemies
- Visual effects show attack impact and range

#### 💎 Collection
- **Regular Diamonds**: Worth 1 diamond and 10 points each
- **SuperDiamonds**: Worth 5 diamonds and 50 points each
- Diamonds serve as health - losing all diamonds costs a life
- Collect diamonds to maintain your health pool

#### 🔋 Power-Ups (SuperDiamonds)
- **Yellow (Speed)**: Increases movement speed by 80% for 10 seconds
- **Green (Jump)**: Increases jump height by 40% for 10 seconds
- **Magenta (Invincible)**: Complete immunity to damage for 5 seconds
- **Orange (Strength)**: Increases attack damage for 10 seconds

#### 🎯 Objectives
1. Collect diamonds and power-ups
2. Defeat all robots in each level
3. Fight and defeat the boss
4. Progress through all 10 levels
5. Achieve the highest score possible

## 📊 Level Progression

| Level | Robots | Platform Difficulty | Boss HP | Challenge |
|-------|--------|-------------------|---------|-----------|
| 1-2   | 6-9    | Large platforms   | 100-175 | ⭐ Tutorial |
| 3-4   | 11-12  | Medium platforms  | 250-325 | ⭐⭐⭐ Intermediate |
| 5-6   | 16-18  | Narrow platforms  | 400-475 | ⭐⭐⭐⭐⭐ Advanced |
| 7-8   | 18-27  | Tiny platforms    | 550-625 | ⭐⭐⭐⭐⭐⭐⭐ Expert |
| 9-10  | 36-44  | Minimal platforms | 700-850 | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ Master |

## 🛠️ Technical Details

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum
- **Storage**: 50 MB available space
- **Audio**: Sound card (optional, game works without audio)

### Dependencies
- **pygame**: Game engine and graphics
- **numpy**: Sound generation and mathematical operations
- **Python Standard Library**: Built-in modules for game logic

### Performance
- **Target FPS**: 60 FPS
- **Resolution**: 1024x768 pixels
- **World Size**: 3000x768 pixels
- **Memory Usage**: ~50-100 MB during gameplay

## 🎵 Audio System

### Sound Effects
The game includes 13 different sound effects:
- Combat sounds (punch, kick, hit)
- Collection sounds (diamonds, power-ups)
- Game state sounds (level complete, life lost)
- Power activation sounds

### Audio Features
- **Procedural Generation**: All sounds are mathematically generated
- **No External Files Required**: Sounds are created in real-time
- **Fallback System**: Game works even if audio fails
- **Volume Control**: Sounds are balanced for gameplay

## 🏗️ Project Structure

```
retro-platform/
├── retro_platform_game.py      # Main game file
├── requirements.txt            # Python dependencies
├── README.md                  # This documentation
├── sounds/                    # Generated sound files
│   ├── jump.wav
│   ├── punch.wav
│   ├── kick.wav
│   └── ... (other sound files)
├── ENHANCEMENTS.md           # Feature documentation
├── SOUND_SYSTEM.md           # Audio system details
├── LEVEL_EXPANSION.md        # Level design documentation
└── COLLISION_FIXES.md        # Technical fixes documentation
```

## 🎨 Game Design

### Visual Style
- **Retro Aesthetic**: Classic 2D platformer look
- **Bright Colors**: High contrast for visibility
- **Smooth Animations**: 60 FPS gameplay
- **Visual Effects**: Attack impacts, power-up glows, particle effects

### Difficulty Curve
- **Progressive Challenge**: Each level introduces new difficulties
- **Skill Development**: Players learn mechanics gradually
- **Strategic Depth**: Power-ups become essential in later levels
- **Replayability**: High scores encourage multiple playthroughs

## 🐛 Troubleshooting

### Common Issues

#### Game Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade pygame numpy
```

#### No Sound
- Check if audio device is working
- Try running: `python -c "import pygame; pygame.mixer.init(); print('Audio OK')"`
- Game will work without sound if audio fails

#### Performance Issues
- Close other applications to free memory
- Lower system resolution if needed
- Ensure Python is not running in debug mode

#### Controls Not Responding
- Make sure game window has focus
- Try clicking on the game window
- Check if keys are working in other applications

### Getting Help
If you encounter issues:
1. Check the troubleshooting section above
2. Verify all requirements are installed
3. Try running the game in a fresh virtual environment
4. Check the console output for error messages

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd retro-platform

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the game
python retro_platform_game.py
```

### Code Style
- Follow PEP 8 Python style guidelines
- Use descriptive variable names
- Comment complex game logic
- Maintain consistent indentation

### Adding Features
1. Test thoroughly on all levels
2. Ensure backward compatibility
3. Update documentation
4. Add appropriate sound effects

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🎯 Achievements & Scoring

### Score System
- **Regular Diamond**: 10 points
- **SuperDiamond**: 50 points  
- **Robot Defeated**: 100 points
- **Boss Defeated**: 500 points
- **Level Completion Bonus**: Varies by level

### Tips for High Scores
1. **Collect Everything**: Don't miss any diamonds
2. **Use Power-Ups Strategically**: Save them for difficult sections
3. **Perfect Combat**: Defeat enemies efficiently
4. **Speed Runs**: Complete levels quickly for bonus points
5. **No Deaths**: Maintain all lives for maximum score

## 🚀 Future Enhancements

### Planned Features
- [ ] Save/Load game progress
- [ ] Multiple difficulty modes
- [ ] Additional power-up types
- [ ] Multiplayer support
- [ ] Level editor
- [ ] Achievement system
- [ ] Leaderboards

### Technical Improvements
- [ ] Optimized rendering
- [ ] Better collision detection
- [ ] Enhanced AI behaviors
- [ ] More visual effects
- [ ] Background music system

---

**Enjoy playing Retro Platform Fighter - Diamond Quest!** 🎮✨

For questions, suggestions, or bug reports, please create an issue in the repository.
