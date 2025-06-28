# Developer Documentation

## 🏗️ Architecture Overview

### Core Components

#### Game Engine Structure
```
retro_platform_game.py
├── SoundManager          # Audio system management
├── Player               # Player character logic
├── Platform             # Platform/terrain objects
├── Diamond              # Regular collectibles
├── SuperDiamond         # Power-up collectibles
├── Robot                # Enemy AI and behavior
├── Boss                 # Boss enemy logic
├── create_level()       # Level generation
└── main()              # Game loop and state management
```

### Class Hierarchy

#### Player Class
- **Position & Movement**: x, y coordinates, velocity, physics
- **Combat System**: Punch/kick attacks with visual effects
- **Power-Up System**: Speed, jump, invincibility, strength boosts
- **Health System**: Diamond-based health with lives
- **Animation**: Visual effects and state management

#### Enemy Classes
- **Robot**: Basic enemy with patrol/chase AI
- **Boss**: Advanced enemy with multiple attack patterns
- **Shared Features**: Health, collision, AI behaviors

#### Collectible Classes
- **Diamond**: Basic collectible (health + points)
- **SuperDiamond**: Power-up collectible with special abilities

## 🎮 Game Systems

### Physics System
```python
# Gravity and movement
GRAVITY = 0.8
PLAYER_SPEED = 6
JUMP_STRENGTH = -16

# Applied each frame
self.vel_y += GRAVITY
self.x += self.vel_x
self.y += self.vel_y
```

### Collision Detection
```python
# Two-phase collision system
# 1. Horizontal movement with side collision check
# 2. Vertical movement with landing detection
# 3. Tolerance system to prevent micro-collisions
```

### Power-Up System
```python
# Power timers (60 FPS)
self.powers = {
    "speed": 600,      # 10 seconds
    "jump": 600,       # 10 seconds  
    "invincible": 300, # 5 seconds
    "strength": 600    # 10 seconds
}
```

### Audio System
```python
# Dual audio approach
# 1. Load .wav files from sounds/ directory
# 2. Generate procedural sounds if files missing
# 3. Graceful fallback if audio system fails
```

## 🔧 Development Setup

### Environment Setup
```bash
# Create development environment
python -m venv dev-env
source dev-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional development tools
pip install pytest black flake8
```

### Code Style Guidelines

#### Python Style (PEP 8)
- **Line Length**: 88 characters (Black formatter)
- **Indentation**: 4 spaces
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Comments**: Docstrings for classes/functions, inline for complex logic

#### Game-Specific Conventions
```python
# Constants in UPPER_CASE
SCREEN_WIDTH = 1024
PLAYER_SPEED = 6

# Class names descriptive
class SuperDiamond:
class SoundManager:

# Method names action-oriented
def update_position()
def handle_collision()
def draw_effects()
```

## 🎨 Adding New Features

### Adding New Power-Ups

1. **Define Power Type**:
```python
# In SuperDiamond.__init__()
power_types = ["speed", "jump", "invincible", "strength", "new_power"]
```

2. **Add Power Logic**:
```python
# In Player.activate_power()
elif power_type == "new_power":
    self.powers["new_power"] = 480  # 8 seconds
    sound_manager.play_sound('new_power_sound')
```

3. **Implement Power Effect**:
```python
# In Player.update()
if self.powers["new_power"] > 0:
    # Apply power effect
    pass
```

4. **Add Visual Effects**:
```python
# In Player.draw()
if self.powers["new_power"] > 0:
    # Draw power visualization
    pass
```

### Adding New Enemy Types

1. **Create Enemy Class**:
```python
class NewEnemy:
    def __init__(self, x, y, enemy_type="normal"):
        # Initialize properties
        pass
    
    def update(self, platforms, player):
        # AI behavior
        pass
    
    def draw(self, screen, camera_x):
        # Rendering
        pass
```

2. **Add to Level Generation**:
```python
# In create_level()
enemies.append(NewEnemy(x, y, "tough"))
```

### Adding New Levels

1. **Extend Level Range**:
```python
# In main() game loop
if current_level > 15:  # Increase from 10
    game_state = "victory"
```

2. **Add Level Design**:
```python
# In create_level()
elif level_num == 11:
    # New level design
    platforms.extend([...])
    robots.extend([...])
    boss = Boss(x, y, 11)
```

## 🔊 Audio Development

### Adding New Sounds

1. **Generate Sound**:
```python
# In SoundManager.generate_sounds()
new_sound = self.create_simple_sound(frequency, duration)
self.sounds['new_sound'] = new_sound
```

2. **Create Sound File** (optional):
```python
# Create .wav file in sounds/ directory
# File will be loaded automatically if present
```

3. **Play Sound**:
```python
# Anywhere in game code
sound_manager.play_sound('new_sound')
```

### Sound Generation Functions
```python
# Available sound generation methods
create_simple_sound(frequency, duration)      # Pure tone
create_sweep_sound(start_freq, end_freq, duration)  # Frequency sweep
create_noise_sound(duration)                  # Noise/static
create_chord_sound(frequencies, duration)     # Multiple tones
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Player movement (all directions)
- [ ] Jumping mechanics
- [ ] Combat system (punch/kick)
- [ ] Diamond collection
- [ ] Power-up activation
- [ ] Enemy AI behavior
- [ ] Boss battles
- [ ] Level progression
- [ ] Sound effects
- [ ] Collision detection

### Automated Testing (Future)
```python
# Example test structure
import pytest
from retro_platform_game import Player, Robot

def test_player_movement():
    player = Player(100, 100)
    player.vel_x = 5
    old_x = player.x
    player.update([], 0)
    assert player.x == old_x + 5

def test_combat_range():
    player = Player(100, 100)
    robot = Robot(150, 100)  # Within range
    # Test combat mechanics
```

## 🐛 Debugging

### Common Debug Techniques

#### Print Debugging
```python
# Add debug prints
print(f"Player position: ({self.x}, {self.y})")
print(f"Player velocity: ({self.vel_x}, {self.vel_y})")
print(f"On ground: {self.on_ground}")
```

#### Visual Debugging
```python
# Draw collision rectangles
pygame.draw.rect(screen, RED, player_rect, 2)
pygame.draw.rect(screen, BLUE, platform.rect, 2)
```

#### Performance Debugging
```python
import time

start_time = time.time()
# Code to measure
end_time = time.time()
print(f"Execution time: {end_time - start_time:.4f}s")
```

### Debug Mode
```python
# Add debug flag
DEBUG = True

if DEBUG:
    # Show debug information
    debug_text = font.render(f"FPS: {clock.get_fps():.1f}", True, WHITE)
    screen.blit(debug_text, (10, SCREEN_HEIGHT - 30))
```

## 📊 Performance Optimization

### Rendering Optimization
```python
# Only draw objects on screen
if -50 < screen_x < SCREEN_WIDTH + 50:
    object.draw(screen, camera_x)

# Use dirty rectangle updates
pygame.display.update(dirty_rects)
```

### Memory Management
```python
# Remove collected objects
diamonds = [d for d in diamonds if not d.collected]
robots = [r for r in robots if r.alive]
```

### Audio Optimization
```python
# Limit concurrent sounds
if len(active_sounds) < MAX_SOUNDS:
    sound.play()
```

## 🔄 Version Control

### Git Workflow
```bash
# Feature development
git checkout -b feature/new-power-up
git add .
git commit -m "Add new power-up system"
git push origin feature/new-power-up

# Create pull request for review
```

### Commit Message Format
```
type(scope): description

feat(player): add new power-up system
fix(collision): resolve platform joint bug  
docs(readme): update installation guide
refactor(audio): improve sound generation
```

## 📈 Metrics and Analytics

### Performance Metrics
- **FPS**: Target 60 FPS, measure with `clock.get_fps()`
- **Memory**: Monitor with system tools
- **Load Time**: Measure game startup time

### Gameplay Metrics
- **Level Completion Rate**: Track player progress
- **Death Locations**: Identify difficulty spikes
- **Power-Up Usage**: Balance power-up effectiveness

## 🚀 Deployment

### Release Checklist
- [ ] All tests pass
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Version number incremented
- [ ] Changelog updated
- [ ] Cross-platform testing completed

### Distribution
```bash
# Create distribution package
python setup.py sdist bdist_wheel

# Or create executable
pip install pyinstaller
pyinstaller --onefile retro_platform_game.py
```

## 🔮 Future Architecture

### Planned Improvements
- **Component System**: Separate rendering, physics, input
- **Scene Management**: Menu, game, pause states
- **Asset Pipeline**: External sprite/sound loading
- **Save System**: Game progress persistence
- **Networking**: Multiplayer support

### Scalability Considerations
- **Modular Design**: Separate concerns
- **Configuration Files**: External game balance
- **Plugin System**: Extensible features
- **Performance Profiling**: Continuous optimization

This documentation provides the foundation for understanding and extending the retro platform game codebase.
