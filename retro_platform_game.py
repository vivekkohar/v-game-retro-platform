import pygame
import sys
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
WORLD_WIDTH = 3000  # Much bigger world

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Player constants - HARDER DIFFICULTY
PLAYER_SPEED = 4  # Reduced from 6 - slower movement
JUMP_STRENGTH = -14  # Reduced from -16 - lower jumps
GRAVITY = 1.0  # Increased from 0.8 - faster falling
PUNCH_RANGE = 35  # Reduced from 45 - shorter attack range
KICK_RANGE = 45  # Reduced from 55 - shorter attack range

# Sound and Music Manager
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        self.music_enabled = True
        
        # Create sound directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
            
        # Try to load sound files first, then generate if needed
        self.load_or_generate_sounds()
        
    def create_simple_sound(self, frequency, duration, sample_rate=22050, volume=0.3):
        """Create a simple sine wave sound without numpy"""
        import array
        import math
        
        frames = int(duration * sample_rate)
        arr = array.array('h')
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = math.sin(2 * math.pi * frequency * time)
            envelope = min(1.0, min(time * 10, (duration - time) * 10))
            sample = int(wave * envelope * volume * 32767)
            arr.append(sample)  # Left channel
            arr.append(sample)  # Right channel
        
        return pygame.sndarray.make_sound(arr)
    
    def create_sweep_sound(self, start_freq, end_freq, duration, sample_rate=22050, volume=0.3):
        """Create a frequency sweep sound without numpy"""
        import array
        import math
        
        frames = int(duration * sample_rate)
        arr = array.array('h')
        
        for i in range(frames):
            time = float(i) / sample_rate
            progress = time / duration
            frequency = start_freq + (end_freq - start_freq) * progress
            wave = math.sin(2 * math.pi * frequency * time)
            envelope = min(1.0, min(time * 5, (duration - time) * 5))
            sample = int(wave * envelope * volume * 32767)
            arr.append(sample)
            arr.append(sample)
        
        return pygame.sndarray.make_sound(arr)
    
    def create_noise_sound(self, duration, sample_rate=22050, volume=0.2):
        """Create a noise sound for metallic effects"""
        import array
        import random
        
        frames = int(duration * sample_rate)
        arr = array.array('h')
        
        for i in range(frames):
            time = float(i) / sample_rate
            noise = random.random() * 2 - 1
            envelope = max(0, 1 - time / duration)
            sample = int(noise * envelope * volume * 32767)
            arr.append(sample)
            arr.append(sample)
        
        return pygame.sndarray.make_sound(arr)
    
    def create_chord_sound(self, frequencies, duration, sample_rate=22050, volume=0.2):
        """Create a chord sound with multiple frequencies"""
        import array
        import math
        
        frames = int(duration * sample_rate)
        arr = array.array('h')
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = 0
            for freq in frequencies:
                wave += math.sin(2 * math.pi * freq * time) / len(frequencies)
            envelope = min(1.0, min(time * 3, (duration - time) * 3))
            sample = int(wave * envelope * volume * 32767)
            arr.append(sample)
            arr.append(sample)
        
        return pygame.sndarray.make_sound(arr)
        
    def load_or_generate_sounds(self):
        """Load sound files or generate them if they don't exist"""
        try:
            # Try to load existing sound files
            sound_files = {
                'jump': 'sounds/jump.wav',
                'punch': 'sounds/punch.wav',
                'kick': 'sounds/kick.wav',
                'diamond_collect': 'sounds/diamond_collect.wav',
                'diamond_lost': 'sounds/diamond_lost.wav',
                'robot_hit': 'sounds/robot_hit.wav',
                'boss_hit': 'sounds/boss_hit.wav',
                'superdiamond_collect': 'sounds/superdiamond_collect.wav',
                'speed_boost': 'sounds/speed_boost.wav',
                'jump_boost': 'sounds/jump_boost.wav',
                'invincible': 'sounds/invincible.wav',
                'life_lost': 'sounds/life_lost.wav',
                'level_complete': 'sounds/level_complete.wav'
            }
            
            # Check if any sound files exist
            files_exist = any(os.path.exists(file) for file in sound_files.values())
            
            if files_exist:
                # Load existing files
                for name, file_path in sound_files.items():
                    if os.path.exists(file_path):
                        try:
                            self.sounds[name] = pygame.mixer.Sound(file_path)
                            print(f"Loaded {name} from file")
                        except:
                            print(f"Failed to load {name}, will generate instead")
            
            # Generate missing sounds
            if not files_exist or len(self.sounds) < len(sound_files):
                print("Generating sounds...")
                self.generate_sounds()
                
        except Exception as e:
            print(f"Error with sound system: {e}")
            print("Generating basic sounds...")
            self.generate_sounds()
        
    def generate_sounds(self):
        """Generate simple sounds using basic pygame functionality"""
        try:
            # Basic sound effects
            self.sounds['jump'] = self.create_sweep_sound(200, 400, 0.2)
            self.sounds['punch'] = self.create_simple_sound(440, 0.1)
            self.sounds['kick'] = self.create_simple_sound(220, 0.15)
            self.sounds['diamond_collect'] = self.create_simple_sound(800, 0.3)
            self.sounds['diamond_lost'] = self.create_sweep_sound(400, 200, 0.4)
            self.sounds['robot_hit'] = self.create_noise_sound(0.1)
            self.sounds['boss_hit'] = self.create_simple_sound(150, 0.2)
            self.sounds['superdiamond_collect'] = self.create_chord_sound([523, 659, 784], 0.8)
            self.sounds['speed_boost'] = self.create_sweep_sound(300, 600, 0.3)
            self.sounds['jump_boost'] = self.create_sweep_sound(400, 800, 0.4)
            self.sounds['invincible'] = self.create_chord_sound([200, 300, 400], 1.0)
            self.sounds['life_lost'] = self.create_sweep_sound(400, 100, 1.0)
            self.sounds['level_complete'] = self.create_chord_sound([400, 500, 600, 800], 1.5)
            
            print("Generated all sounds successfully!")
            
        except Exception as e:
            print(f"Warning: Could not generate sounds: {e}")
            self.sound_enabled = False
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Warning: Could not play sound {sound_name}: {e}")
        else:
            print(f"Sound {sound_name} not found or sound disabled")
    
    def start_background_music(self):
        """Start background music (simple loop)"""
        if self.music_enabled and not self.music_playing:
            try:
                # For now, no background music - focus on sound effects
                pass
            except Exception as e:
                print(f"Warning: Could not start background music: {e}")

# Global sound manager
sound_manager = SoundManager()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.punching = False
        self.kicking = False
        self.punch_timer = 0
        self.kick_timer = 0
        self.diamonds = 30  # Reduced from 50 - less starting health
        self.lives = 2  # Reduced from 3 - fewer lives
        self.invulnerable = 0  # Invulnerability frames after taking damage
        self.animation_frame = 0
        self.punch_effect = []  # Visual punch effects
        self.kick_effect = []   # Visual kick effects
        self.jump_cooldown = 0  # Prevent infinite jumping on enemies
        
        # HARDER DIFFICULTY - New challenging mechanics
        self.stamina = 100  # Stamina system for attacks
        self.max_stamina = 100
        self.stamina_regen = 0.5  # Slow stamina regeneration
        self.attack_stamina_cost = 15  # High stamina cost for attacks
        self.jump_stamina_cost = 10  # Stamina cost for jumping
        self.low_stamina_penalty = 0.5  # Movement penalty when low stamina
        
        # Power-up system - NERFED
        self.powers = {
            "speed": 0,      # Speed boost timer
            "jump": 0,       # Jump boost timer
            "invincible": 0, # Invincibility timer
            "strength": 0    # Strength boost timer
        }
        self.power_effects = []  # Visual power effects
        self.power_cooldown = 300  # 5 second cooldown between power uses
        
    def activate_power(self, power_type):
        """Activate a power-up - HARDER DIFFICULTY with cooldowns and nerfs"""
        if self.power_cooldown > 0:
            return  # Power-ups on cooldown
            
        if power_type == "speed":
            self.powers["speed"] = 300  # Reduced from 600 - 5 seconds instead of 10
            sound_manager.play_sound('speed_boost')
        elif power_type == "jump":
            self.powers["jump"] = 300  # Reduced from 600 - 5 seconds instead of 10
            sound_manager.play_sound('jump_boost')
        elif power_type == "invincible":
            self.powers["invincible"] = 150  # Reduced from 300 - 2.5 seconds instead of 5
            sound_manager.play_sound('invincible')
        elif power_type == "strength":
            self.powers["strength"] = 300  # Reduced from 600 - 5 seconds instead of 10
            sound_manager.play_sound('speed_boost')  # Reuse speed sound for now
        
        # Set cooldown period
        self.power_cooldown = 300  # 5 second cooldown between power uses
        
        # Add visual effect
        self.power_effects.append({
            'type': power_type,
            'timer': 60,
            'size': 30
        })
    
    def update(self, platforms, camera_x):
        # Update power timers and cooldowns
        for power in self.powers:
            if self.powers[power] > 0:
                self.powers[power] -= 1
        
        if self.power_cooldown > 0:
            self.power_cooldown -= 1
        
        # HARDER DIFFICULTY - Stamina system
        # Regenerate stamina slowly
        if self.stamina < self.max_stamina:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen)
        
        # Handle input
        keys = pygame.key.get_pressed()
        
        # Movement with speed boost and stamina penalty
        base_speed = PLAYER_SPEED
        if self.powers["speed"] > 0:
            base_speed = int(PLAYER_SPEED * 1.5)  # Reduced from 1.8 - less speed boost
        
        # HARDER DIFFICULTY - Low stamina movement penalty
        if self.stamina < 20:  # Low stamina threshold
            base_speed = int(base_speed * self.low_stamina_penalty)
        
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -base_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = base_speed
            self.facing_right = True
            
        # Jumping with jump boost and stamina cost
        jump_power = JUMP_STRENGTH
        if self.powers["jump"] > 0:
            jump_power = int(JUMP_STRENGTH * 1.25)  # Reduced from 1.4 - less jump boost
            
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            # HARDER DIFFICULTY - Stamina cost for jumping
            if self.stamina >= self.jump_stamina_cost:
                self.vel_y = jump_power
                self.on_ground = False
                self.stamina -= self.jump_stamina_cost
                sound_manager.play_sound('jump')
            
        # Combat with strength boost and stamina costs
        punch_damage = 15
        kick_damage = 25
        if self.powers["strength"] > 0:
            punch_damage = 20  # Reduced from 25 - less damage boost
            kick_damage = 35   # Reduced from 40 - less damage boost
            
        if keys[pygame.K_x] and self.punch_timer <= 0:
            # HARDER DIFFICULTY - Stamina cost for attacks
            if self.stamina >= self.attack_stamina_cost:
                self.punching = True
                self.punch_timer = 25  # Increased from 20 - slower attacks
                self.stamina -= self.attack_stamina_cost
                sound_manager.play_sound('punch')
                # Add punch visual effect
                punch_x = self.x + (40 if self.facing_right else -40)
                punch_y = self.y + 20
                effect_size = 25 if self.powers["strength"] > 0 else 20
                self.punch_effect.append({
                    'x': punch_x, 'y': punch_y, 'timer': 15, 'size': effect_size,
                    'powered': self.powers["strength"] > 0
                })
            
        if keys[pygame.K_z] and self.kick_timer <= 0:
            # HARDER DIFFICULTY - Stamina cost for attacks
            if self.stamina >= self.attack_stamina_cost:
                self.kicking = True
                self.kick_timer = 35  # Increased from 25 - slower attacks
                self.stamina -= self.attack_stamina_cost
                sound_manager.play_sound('kick')
                # Add kick visual effect
                kick_x = self.x + (50 if self.facing_right else -50)
                kick_y = self.y + 30
                effect_size = 30 if self.powers["strength"] > 0 else 25
                self.kick_effect.append({
                    'x': kick_x, 'y': kick_y, 'timer': 20, 'size': effect_size,
                    'powered': self.powers["strength"] > 0
                })
            
        # Update timers
        if self.punch_timer > 0:
            self.punch_timer -= 1
        else:
            self.punching = False
            
        if self.kick_timer > 0:
            self.kick_timer -= 1
        else:
            self.kicking = False
            
        # Invincibility handling
        if self.powers["invincible"] > 0:
            self.invulnerable = max(self.invulnerable, 1)  # Stay invulnerable
        elif self.invulnerable > 0:
            self.invulnerable -= 1
        
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        
        # Update visual effects
        self.punch_effect = [effect for effect in self.punch_effect 
                           if self.update_effect(effect)]
        self.kick_effect = [effect for effect in self.kick_effect 
                          if self.update_effect(effect)]
        self.power_effects = [effect for effect in self.power_effects 
                            if self.update_power_effect(effect)]
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position with collision detection
        # Handle horizontal movement first
        old_x = self.x
        self.x += self.vel_x
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Check for horizontal collisions
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # Only block horizontal movement if player is not on top of the platform
                player_bottom = self.y + self.height
                platform_top = platform.rect.top
                
                # If player is significantly above the platform (not walking on it)
                if player_bottom < platform_top - 10:  # 10 pixel tolerance
                    # Restore old position to prevent clipping
                    self.x = old_x
                    break
        
        # Handle vertical movement
        old_y = self.y
        self.y += self.vel_y
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Check for vertical collisions
        self.on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # Landing on top of platform
                if self.vel_y > 0 and old_y + self.height <= platform.rect.top + 5:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # Hitting platform from below
                elif self.vel_y < 0 and old_y >= platform.rect.bottom - 5:
                    self.y = platform.rect.bottom
                    self.vel_y = 0
        
        # World boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > WORLD_WIDTH - self.width:
            self.x = WORLD_WIDTH - self.width
            
        # Fall off screen - lose diamonds and respawn
        if self.y > SCREEN_HEIGHT + 100:
            self.lose_diamonds(10)
            self.respawn()
            
        # Animation
        self.animation_frame += 1
    
    def update_effect(self, effect):
        """Update visual effect and return True if it should continue"""
        effect['timer'] -= 1
        effect['size'] += 1  # Expand effect
        return effect['timer'] > 0
    
    def update_power_effect(self, effect):
        """Update power activation effect and return True if it should continue"""
        effect['timer'] -= 1
        effect['size'] += 2  # Expand effect
        return effect['timer'] > 0
    
    def lose_diamonds(self, amount):
        # Invincible players don't lose diamonds
        if self.powers["invincible"] > 0:
            return
        
        # HARDER DIFFICULTY - Lose more diamonds and stamina
        actual_loss = int(amount * 1.5)  # 50% more diamond loss
        self.diamonds -= actual_loss
        self.stamina = max(0, self.stamina - 20)  # Lose stamina when taking damage
        
        sound_manager.play_sound('diamond_lost')
        if self.diamonds <= 0:
            self.diamonds = 0
            self.lose_life()
    
    def lose_life(self):
        self.lives -= 1
        sound_manager.play_sound('life_lost')
        self.diamonds = 20  # Reduced from 50 - less health on respawn
        self.stamina = 50   # Reduced stamina on respawn
        self.respawn()
    
    def respawn(self):
        self.x = 100
        self.y = SCREEN_HEIGHT - 200
        self.vel_x = 0
        self.vel_y = 0
        self.invulnerable = 180  # Increased from 120 - longer invulnerability needed
    
    def draw(self, screen, camera_x):
        # Calculate screen position
        screen_x = self.x - camera_x
        
        # Don't draw if off screen
        if screen_x < -50 or screen_x > SCREEN_WIDTH + 50:
            return
            
        # Power-up glow effects
        if self.powers["invincible"] > 0:
            # Invincible glow - pulsing magenta
            pulse = int(abs(math.sin(self.animation_frame * 0.3)) * 100) + 155
            glow_color = (pulse, 0, pulse)
            pygame.draw.circle(screen, glow_color, 
                             (int(screen_x + 16), int(self.y + 24)), 35, 3)
        
        if self.powers["speed"] > 0:
            # Speed trails
            for i in range(3):
                trail_x = screen_x - (i + 1) * 8 * (1 if self.facing_right else -1)
                trail_alpha = 100 - i * 30
                trail_color = (255, 255, 0, trail_alpha)
                pygame.draw.circle(screen, (255, 255, 0), 
                                 (int(trail_x + 16), int(self.y + 24)), 20, 2)
        
        if self.powers["jump"] > 0:
            # Jump boost - green aura
            pygame.draw.circle(screen, (0, 255, 0), 
                             (int(screen_x + 16), int(self.y + 24)), 30, 2)
        
        if self.powers["strength"] > 0:
            # Strength boost - orange glow around fists
            fist_color = (255, 100, 0)
            pygame.draw.circle(screen, fist_color, 
                             (int(screen_x + 6), int(self.y + 20)), 8, 2)
            pygame.draw.circle(screen, fist_color, 
                             (int(screen_x + 26), int(self.y + 20)), 8, 2)
        
        # HARDER DIFFICULTY - Show stamina bar above player
        if self.stamina < self.max_stamina:
            bar_width = 30
            bar_height = 4
            bar_x = screen_x + (self.width - bar_width) // 2
            bar_y = self.y - 10
            
            # Background bar
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            
            # Stamina bar
            stamina_width = int((self.stamina / self.max_stamina) * bar_width)
            stamina_color = GREEN if self.stamina > 50 else YELLOW if self.stamina > 20 else RED
            pygame.draw.rect(screen, stamina_color, (bar_x, bar_y, stamina_width, bar_height))
            
        # Flicker when invulnerable (but not when invincible power is active)
        if self.invulnerable > 0 and self.powers["invincible"] == 0 and self.invulnerable % 10 < 5:
            return
        
        # Body (boy character)
        body_color = (100, 150, 255)  # Blue shirt
        pygame.draw.rect(screen, body_color, (screen_x + 8, self.y + 16, 16, 20))
        
        # Pants
        pygame.draw.rect(screen, (50, 50, 150), (screen_x + 8, self.y + 36, 16, 12))
        
        # Head
        pygame.draw.circle(screen, (255, 220, 177), 
                         (int(screen_x + 16), int(self.y + 12)), 10)
        
        # Hair
        pygame.draw.arc(screen, BROWN, 
                       (screen_x + 6, self.y + 2, 20, 16), 0, math.pi, 3)
        
        # Eyes
        eye_x = screen_x + 16 + (2 if self.facing_right else -2)
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(self.y + 10)), 2)
        
        # Arms with enhanced combat visualization
        arm_y = self.y + 20
        if self.punching:
            # Extended arm for punch with more detail
            arm_x = screen_x + (28 if self.facing_right else 4)
            # Upper arm
            pygame.draw.line(screen, (255, 220, 177), 
                           (screen_x + 16, arm_y), (arm_x - 8, arm_y), 4)
            # Forearm
            pygame.draw.line(screen, (255, 220, 177), 
                           (arm_x - 8, arm_y), (arm_x, arm_y), 4)
            # Fist
            pygame.draw.circle(screen, (255, 200, 150), (int(arm_x), int(arm_y)), 5)
        else:
            # Normal arms
            pygame.draw.circle(screen, (255, 220, 177), 
                             (int(screen_x + 6), int(arm_y)), 3)
            pygame.draw.circle(screen, (255, 220, 177), 
                             (int(screen_x + 26), int(arm_y)), 3)
        
        # Legs with enhanced kicking visualization
        leg_y = self.y + 48
        if self.kicking:
            # Extended leg for kick with more detail
            leg_x = screen_x + (32 if self.facing_right else 0)
            # Thigh
            pygame.draw.line(screen, (255, 220, 177), 
                           (screen_x + 16, leg_y - 5), (leg_x - 8, leg_y), 5)
            # Shin
            pygame.draw.line(screen, (255, 220, 177), 
                           (leg_x - 8, leg_y), (leg_x, leg_y), 5)
            # Foot
            pygame.draw.ellipse(screen, (50, 50, 50), 
                              (leg_x - 2, leg_y - 2, 8, 4))
            # Other leg (standing)
            other_leg_x = screen_x + (8 if self.facing_right else 24)
            pygame.draw.circle(screen, (255, 220, 177), 
                             (int(other_leg_x), int(leg_y)), 3)
        else:
            # Normal legs with walking animation
            offset = math.sin(self.animation_frame * 0.3) * 2 if abs(self.vel_x) > 0 else 0
            pygame.draw.circle(screen, (255, 220, 177), 
                             (int(screen_x + 10 + offset), int(leg_y)), 3)
            pygame.draw.circle(screen, (255, 220, 177), 
                             (int(screen_x + 22 - offset), int(leg_y)), 3)
        
        # Draw visual effects
        self.draw_effects(screen, camera_x)
    
    def draw_effects(self, screen, camera_x):
        """Draw punch and kick visual effects"""
        # Draw punch effects
        for effect in self.punch_effect:
            screen_x = effect['x'] - camera_x
            if -50 < screen_x < SCREEN_WIDTH + 50:
                # Expanding circle effect
                base_color = ORANGE if effect.get('powered', False) else YELLOW
                
                # Create multiple rings for impact effect
                for i in range(4 if effect.get('powered', False) else 3):
                    radius = effect['size'] + i * 3
                    if radius > 0:
                        pygame.draw.circle(screen, base_color, 
                                         (int(screen_x), int(effect['y'])), 
                                         radius, 3 if effect.get('powered', False) else 2)
                
                # Add spark effects
                spark_count = 12 if effect.get('powered', False) else 8
                for i in range(spark_count):
                    angle = (i * (360 / spark_count)) * math.pi / 180
                    spark_x = screen_x + math.cos(angle) * effect['size']
                    spark_y = effect['y'] + math.sin(angle) * effect['size']
                    spark_size = 3 if effect.get('powered', False) else 2
                    pygame.draw.circle(screen, WHITE, 
                                     (int(spark_x), int(spark_y)), spark_size)
        
        # Draw kick effects
        for effect in self.kick_effect:
            screen_x = effect['x'] - camera_x
            if -50 < screen_x < SCREEN_WIDTH + 50:
                # Expanding arc effect for kick
                base_color = ORANGE if effect.get('powered', False) else RED
                
                # Create arc effect
                arc_count = 6 if effect.get('powered', False) else 5
                for i in range(arc_count):
                    radius = effect['size'] + i * 2
                    if radius > 0:
                        # Draw arc
                        start_angle = -math.pi/3 if effect.get('powered', False) else -math.pi/4
                        end_angle = math.pi/3 if effect.get('powered', False) else math.pi/4
                        pygame.draw.arc(screen, base_color, 
                                      (screen_x - radius, effect['y'] - radius, 
                                       radius * 2, radius * 2),
                                      start_angle, end_angle, 4 if effect.get('powered', False) else 3)
                
                # Add motion lines
                line_count = 5 if effect.get('powered', False) else 3
                for i in range(line_count):
                    line_x = screen_x + i * 6
                    line_width = 3 if effect.get('powered', False) else 2
                    pygame.draw.line(screen, base_color, 
                                   (line_x, effect['y'] - 8), 
                                   (line_x, effect['y'] + 8), line_width)
        
        # Draw power activation effects
        for effect in self.power_effects:
            screen_x = self.x - camera_x
            if -50 < screen_x < SCREEN_WIDTH + 50:
                colors = {
                    "speed": (255, 255, 0),
                    "jump": (0, 255, 0),
                    "invincible": (255, 0, 255),
                    "strength": (255, 100, 0)
                }
                color = colors.get(effect['type'], WHITE)
                
                # Expanding ring effect
                pygame.draw.circle(screen, color, 
                                 (int(screen_x + 16), int(self.y + 24)), 
                                 effect['size'], 3)
                
                # Power type text
                if effect['timer'] > 30:
                    font = pygame.font.Font(None, 24)
                    text = font.render(effect['type'].upper(), True, color)
                    screen.blit(text, (screen_x - 20, self.y - 30))

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen, camera_x):
        # Calculate screen position
        screen_x = self.rect.x - camera_x
        
        # Don't draw if completely off screen
        if screen_x + self.rect.width < 0 or screen_x > SCREEN_WIDTH:
            return
            
        # Dirt base
        dirt_rect = pygame.Rect(screen_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, BROWN, dirt_rect)
        
        # Grass top
        grass_rect = pygame.Rect(screen_x, self.rect.y, self.rect.width, 8)
        pygame.draw.rect(screen, GREEN, grass_rect)
        
        # Add some texture
        for i in range(0, self.rect.width, 16):
            if screen_x + i >= 0 and screen_x + i <= SCREEN_WIDTH:
                pygame.draw.line(screen, (100, 50, 0), 
                               (screen_x + i, self.rect.y + 8), 
                               (screen_x + i, self.rect.y + self.rect.height), 1)

class Diamond:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.collected = False
        self.animation = 0
        
    def update(self, player):
        if self.collected:
            return
            
        self.animation += 0.2
        
        # Check collision with player
        diamond_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        
        if diamond_rect.colliderect(player_rect):
            self.collected = True
            player.diamonds += 1
            sound_manager.play_sound('diamond_collect')
    
    def draw(self, screen, camera_x):
        if self.collected:
            return
            
        screen_x = self.x - camera_x
        if screen_x < -20 or screen_x > SCREEN_WIDTH + 20:
            return
            
        # Animated diamond
        offset_y = math.sin(self.animation) * 3
        points = [
            (screen_x + 8, self.y + offset_y),
            (screen_x + 4, self.y + 6 + offset_y),
            (screen_x + 8, self.y + 12 + offset_y),
            (screen_x + 12, self.y + 6 + offset_y)
        ]
        pygame.draw.polygon(screen, CYAN, points)
        pygame.draw.polygon(screen, WHITE, points, 2)

class SuperDiamond:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.collected = False
        self.animation = 0
        self.power_type = power_type  # "speed", "jump", "invincible", "strength"
        self.colors = {
            "speed": (255, 255, 0),      # Yellow
            "jump": (0, 255, 0),         # Green
            "invincible": (255, 0, 255), # Magenta
            "strength": (255, 100, 0)    # Orange
        }
        
    def update(self, player):
        if self.collected:
            return
            
        self.animation += 0.3
        
        # Check collision with player
        diamond_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        
        if diamond_rect.colliderect(player_rect):
            self.collected = True
            player.diamonds += 5  # SuperDiamonds are worth more
            player.activate_power(self.power_type)
            sound_manager.play_sound('superdiamond_collect')
    
    def draw(self, screen, camera_x):
        if self.collected:
            return
            
        screen_x = self.x - camera_x
        if screen_x < -30 or screen_x > SCREEN_WIDTH + 30:
            return
            
        # Animated superdiamond with glow effect
        offset_y = math.sin(self.animation) * 4
        color = self.colors[self.power_type]
        
        # Glow effect
        for i in range(3):
            glow_size = 8 + i * 4
            glow_alpha = 100 - i * 30
            glow_points = [
                (screen_x + 12, self.y + offset_y - glow_size//2),
                (screen_x + 12 - glow_size//2, self.y + 6 + offset_y),
                (screen_x + 12, self.y + 12 + offset_y + glow_size//2),
                (screen_x + 12 + glow_size//2, self.y + 6 + offset_y)
            ]
            # Create a surface for the glow effect
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2))
            glow_surf.set_alpha(glow_alpha)
            glow_surf.fill(color)
            screen.blit(glow_surf, (screen_x + 12 - glow_size, self.y + offset_y + 6 - glow_size))
        
        # Main diamond
        points = [
            (screen_x + 12, self.y + offset_y),
            (screen_x + 6, self.y + 8 + offset_y),
            (screen_x + 12, self.y + 16 + offset_y),
            (screen_x + 18, self.y + 8 + offset_y)
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, WHITE, points, 3)
        
        # Sparkle effects
        for i in range(4):
            angle = (self.animation * 2 + i * 90) * math.pi / 180
            sparkle_x = screen_x + 12 + math.cos(angle) * 15
            sparkle_y = self.y + 8 + offset_y + math.sin(angle) * 15
            pygame.draw.circle(screen, WHITE, (int(sparkle_x), int(sparkle_y)), 2)

class Robot:
    def __init__(self, x, y, robot_type="normal"):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 40
        self.vel_x = random.choice([-2, 2])
        self.vel_y = 0
        self.health = 30 if robot_type == "normal" else 80  # Tougher robots have much more health
        self.max_health = self.health
        self.alive = True
        self.attack_timer = 0
        self.patrol_distance = 100
        self.start_x = x
        self.type = robot_type
        self.speed = 1.5 if robot_type == "normal" else 3.0  # Tougher robots are faster
        self.attack_damage = 5 if robot_type == "normal" else 8  # Tougher robots deal more damage
        
    def update(self, platforms, player):
        if not self.alive:
            return
            
        # Simple AI - patrol and chase player if close
        distance_to_player = abs(self.x - player.x)
        
        if distance_to_player < 200:
            # Chase player
            if player.x > self.x:
                self.vel_x = self.speed
            else:
                self.vel_x = -self.speed
        else:
            # Patrol
            if abs(self.x - self.start_x) > self.patrol_distance:
                self.vel_x *= -1
                
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        robot_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        on_ground = False
        
        for platform in platforms:
            if robot_rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.y < platform.rect.top:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    on_ground = True
                    
        # Turn around at edges
        if not on_ground and self.vel_y >= 0:
            self.vel_x *= -1
            
        # Attack player if close and player is not invulnerable
        if (distance_to_player < 40 and abs(self.y - player.y) < 50 and 
            player.invulnerable == 0 and not (player.punching or player.kicking)):
            self.attack_timer += 1
            if self.attack_timer > 60:  # Attack every second
                player.lose_diamonds(self.attack_damage)
                player.invulnerable = 60  # 1 second invulnerability
                self.attack_timer = 0
        
        # Check if hit by player (with proper range and height checking)
        vertical_distance = abs(self.y - player.y)
        if (distance_to_player < PUNCH_RANGE and 
            vertical_distance < 60 and  # Must be within reasonable height
            player.punching):
            damage = 25 if player.powers["strength"] > 0 else 15
            self.health -= damage
            self.vel_x = 5 if player.facing_right else -5
            sound_manager.play_sound('robot_hit')
            
        if (distance_to_player < KICK_RANGE and 
            vertical_distance < 60 and  # Must be within reasonable height
            player.kicking):
            damage = 40 if player.powers["strength"] > 0 else 25
            self.health -= damage
            self.vel_x = 8 if player.facing_right else -8
            self.vel_y = -5
            sound_manager.play_sound('robot_hit')
            
        # Check if jumped on
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        robot_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Check if player is above the robot and moving downward
        if (player_rect.colliderect(robot_rect) and 
            player_rect.bottom < robot_rect.centery and 
            player.vel_y > 0 and 
            player.jump_cooldown == 0):
            self.health -= 20
            player.vel_y = -12  # Bounce player up more
            sound_manager.play_sound('robot_hit')
            # Add cooldown to prevent infinite bouncing
            player.jump_cooldown = 10
            # Push the player up slightly to prevent getting stuck
            player.y = self.y - player.height - 1
            
        if self.health <= 0:
            self.alive = False
    
    def draw(self, screen, camera_x):
        if not self.alive:
            return
            
        screen_x = self.x - camera_x
        if screen_x < -50 or screen_x > SCREEN_WIDTH + 50:
            return
            
        # Robot body
        color = GRAY if self.type == "normal" else (150, 50, 50)
        pygame.draw.rect(screen, color, (screen_x, self.y, self.width, self.height))
        
        # Robot head
        pygame.draw.rect(screen, (150, 150, 150), 
                        (screen_x + 4, self.y - 8, self.width - 8, 12))
        
        # Evil red eyes
        pygame.draw.circle(screen, RED, (int(screen_x + 8), int(self.y - 2)), 3)
        pygame.draw.circle(screen, RED, (int(screen_x + self.width - 8), int(self.y - 2)), 3)
        
        # Health bar
        if self.health < self.max_health:
            bar_width = int((self.health / self.max_health) * self.width)
            pygame.draw.rect(screen, RED, (screen_x, self.y - 15, self.width, 4))
            pygame.draw.rect(screen, GREEN, (screen_x, self.y - 15, bar_width, 4))

class Boss:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 80
        self.vel_x = 0
        self.vel_y = 0
        self.health = 100 + (level * 75)  # Much more health scaling
        self.max_health = self.health
        self.alive = True
        self.attack_timer = 0
        self.level = level
        self.phase = 0
        self.attack_pattern = 0
        self.animation = 0
        self.move_timer = 0
        self.jump_timer = 0
        self.charge_timer = 0
        self.is_charging = False
        self.base_damage = 8 + (level * 2)  # Damage scales with level
        
    def update(self, platforms, player):
        if not self.alive:
            return
            
        self.animation += 0.1
        distance_to_player = abs(self.x - player.x)
        
        # Update timers
        self.attack_timer += 1
        self.move_timer += 1
        self.jump_timer += 1
        
        # Boss AI based on level and health percentage
        health_percentage = self.health / self.max_health
        
        if self.level <= 2:
            # Simple aggressive boss
            if self.attack_timer > 60:  # Attack every second
                if distance_to_player < 80:
                    # Close range attack
                    if player.invulnerable == 0 and not (player.punching or player.kicking):
                        player.lose_diamonds(self.base_damage)
                        player.invulnerable = 60
                        sound_manager.play_sound('robot_hit')
                    self.attack_timer = 0
                elif distance_to_player < 150:
                    # Charge at player
                    self.is_charging = True
                    self.charge_timer = 30
                    if player.x > self.x:
                        self.vel_x = 4
                    else:
                        self.vel_x = -4
                    self.attack_timer = 0
            
            # Normal movement when not attacking
            if not self.is_charging and self.move_timer > 120:
                if player.x > self.x:
                    self.vel_x = 2
                else:
                    self.vel_x = -2
                self.move_timer = 0
                
        else:
            # Advanced boss with multiple attack patterns
            if self.attack_timer > 90:
                self.attack_pattern = (self.attack_pattern + 1) % 4
                self.attack_timer = 0
                
            if self.attack_pattern == 0:  # Aggressive chase
                if player.x > self.x:
                    self.vel_x = 3 + self.level * 0.5
                else:
                    self.vel_x = -(3 + self.level * 0.5)
                    
                # Close combat
                if distance_to_player < 70 and player.invulnerable == 0:
                    if not (player.punching or player.kicking):
                        player.lose_diamonds(self.base_damage + 2)
                        player.invulnerable = 45
                        sound_manager.play_sound('robot_hit')
                        
            elif self.attack_pattern == 1:  # Jump attack
                if self.jump_timer > 60 and distance_to_player < 200:
                    self.vel_y = -15
                    self.jump_timer = 0
                    # Damage player if boss lands on them
                    if (distance_to_player < 50 and 
                        abs(self.y - player.y) < 30 and 
                        player.invulnerable == 0):
                        player.lose_diamonds(self.base_damage + 5)
                        player.invulnerable = 90
                        sound_manager.play_sound('robot_hit')
                        
            elif self.attack_pattern == 2:  # Charge attack
                self.is_charging = True
                self.charge_timer = 45
                charge_speed = 5 + self.level
                if player.x > self.x:
                    self.vel_x = charge_speed
                else:
                    self.vel_x = -charge_speed
                    
                # Damage during charge
                if (distance_to_player < 60 and 
                    player.invulnerable == 0 and 
                    not (player.punching or player.kicking)):
                    player.lose_diamonds(self.base_damage + 3)
                    player.invulnerable = 60
                    sound_manager.play_sound('robot_hit')
                    
            else:  # Defensive pattern with occasional strikes
                self.vel_x *= 0.8  # Slow down
                if distance_to_player < 100 and self.move_timer > 30:
                    # Quick strike
                    if player.invulnerable == 0:
                        player.lose_diamonds(self.base_damage)
                        player.invulnerable = 75
                        sound_manager.play_sound('robot_hit')
                    self.move_timer = 0
        
        # Handle charging state
        if self.is_charging:
            self.charge_timer -= 1
            if self.charge_timer <= 0:
                self.is_charging = False
                self.vel_x *= 0.5  # Slow down after charge
        
        # Enraged mode when health is low
        if health_percentage < 0.3:
            self.vel_x *= 1.5  # Move faster when low health
            if self.attack_timer > 45:  # Attack more frequently
                if (distance_to_player < 90 and 
                    player.invulnerable == 0 and 
                    not (player.punching or player.kicking)):
                    player.lose_diamonds(self.base_damage - 2)  # Slightly less damage but more frequent
                    player.invulnerable = 30
                    sound_manager.play_sound('robot_hit')
                    self.attack_timer = 0
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        boss_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            if boss_rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.y < platform.rect.top:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
        
        # Keep boss in boss area (don't let it wander too far)
        if self.x < WORLD_WIDTH - 600:
            self.x = WORLD_WIDTH - 600
            self.vel_x = abs(self.vel_x)  # Turn around
        elif self.x > WORLD_WIDTH - 100:
            self.x = WORLD_WIDTH - 100
            self.vel_x = -abs(self.vel_x)  # Turn around
                    
        # Check if hit by player (with proper range and height checking)
        vertical_distance = abs(self.y - player.y)
        if (distance_to_player < PUNCH_RANGE and 
            vertical_distance < 80 and  # Bosses are taller, so slightly more range
            player.punching):
            damage = 20 if player.powers["strength"] > 0 else 10
            self.health -= damage
            self.vel_x = 3 if player.facing_right else -3
            sound_manager.play_sound('boss_hit')
            
        if (distance_to_player < KICK_RANGE and 
            vertical_distance < 80 and  # Bosses are taller, so slightly more range
            player.kicking):
            damage = 35 if player.powers["strength"] > 0 else 20
            self.health -= damage
            self.vel_x = 5 if player.facing_right else -5
            self.vel_y = -3
            sound_manager.play_sound('boss_hit')
            
        # Check if jumped on (with cooldown to prevent infinite bouncing)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        boss_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if (player_rect.colliderect(boss_rect) and 
            player_rect.bottom < boss_rect.centery and 
            player.vel_y > 0 and 
            player.jump_cooldown == 0):
            self.health -= 15
            player.vel_y = -12  # Bounce player up
            player.jump_cooldown = 15  # Prevent immediate re-bounce
            # Push the player up slightly to prevent getting stuck
            player.y = self.y - player.height - 2
            sound_manager.play_sound('boss_hit')
            
        if self.health <= 0:
            self.alive = False
    
    def draw(self, screen, camera_x):
        if not self.alive:
            return
            
        screen_x = self.x - camera_x
        if screen_x < -100 or screen_x > SCREEN_WIDTH + 100:
            return
            
        # Boss body (larger and more menacing)
        colors = [(100, 0, 100), (150, 0, 0), (0, 100, 100), (100, 100, 0), (150, 50, 150)]
        boss_color = colors[min(self.level - 1, 4)]
        
        # Charging effect - make boss glow red
        if self.is_charging:
            boss_color = (255, 50, 50)
        
        # Enraged effect when health is low
        health_percentage = self.health / self.max_health
        if health_percentage < 0.3:
            # Pulsing red effect when low health
            pulse_intensity = int(abs(math.sin(self.animation * 3)) * 100)
            boss_color = (min(255, boss_color[0] + pulse_intensity), 
                         boss_color[1], boss_color[2])
        
        # Pulsing effect
        pulse = int(math.sin(self.animation) * 3)
        pygame.draw.rect(screen, boss_color, 
                        (screen_x - pulse, self.y - pulse, 
                         self.width + pulse*2, self.height + pulse*2))
        
        # Boss head
        head_color = (200, 200, 200)
        if self.is_charging:
            head_color = (255, 200, 200)
        pygame.draw.rect(screen, head_color, 
                        (screen_x + 10, self.y - 15, self.width - 20, 20))
        
        # Glowing eyes - more intense when attacking
        if self.attack_pattern == 0 or self.is_charging:  # Aggressive mode
            eye_color = (255, 0, 0)
            eye_size = 6
        elif health_percentage < 0.3:  # Enraged mode
            eye_color = (255, 100, 0) if self.animation % 1 < 0.5 else (255, 0, 0)
            eye_size = 7
        else:
            eye_color = (255, 0, 0) if self.animation % 1 < 0.5 else (255, 100, 100)
            eye_size = 5
            
        pygame.draw.circle(screen, eye_color, (int(screen_x + 20), int(self.y - 5)), eye_size)
        pygame.draw.circle(screen, eye_color, (int(screen_x + self.width - 20), int(self.y - 5)), eye_size)
        
        # Attack pattern indicator
        if self.attack_pattern == 1:  # Jump attack mode
            # Show jump preparation
            for i in range(3):
                pygame.draw.circle(screen, (255, 255, 0), 
                                 (int(screen_x + self.width//2), int(self.y + self.height + 5 + i*3)), 
                                 2)
        elif self.attack_pattern == 2 or self.is_charging:  # Charge mode
            # Show charge lines
            for i in range(5):
                line_x = screen_x - 10 - i*5
                pygame.draw.line(screen, (255, 100, 0), 
                               (line_x, self.y + 20), (line_x, self.y + 60), 2)
        
        # Health bar
        bar_width = int((self.health / self.max_health) * self.width)
        bar_color = GREEN
        if health_percentage < 0.5:
            bar_color = YELLOW
        if health_percentage < 0.3:
            bar_color = RED
            
        pygame.draw.rect(screen, RED, (screen_x, self.y - 25, self.width, 6))
        pygame.draw.rect(screen, bar_color, (screen_x, self.y - 25, bar_width, 6))
        
        # Boss level indicator
        font = pygame.font.Font(None, 24)
        level_text = font.render(f"BOSS LV.{self.level}", True, WHITE)
        screen.blit(level_text, (screen_x, self.y - 45))
        
        # Attack mode indicator
        if self.level > 2:
            mode_text = ""
            if self.attack_pattern == 0:
                mode_text = "AGGRESSIVE"
            elif self.attack_pattern == 1:
                mode_text = "JUMP ATTACK"
            elif self.attack_pattern == 2:
                mode_text = "CHARGING"
            else:
                mode_text = "DEFENSIVE"
                
            if health_percentage < 0.3:
                mode_text = "ENRAGED!"
                
            mode_font = pygame.font.Font(None, 18)
            mode_surface = mode_font.render(mode_text, True, YELLOW)
            screen.blit(mode_surface, (screen_x, self.y - 65))

def create_level(level_num):
    platforms = []
    robots = []
    diamonds = []
    superdiamonds = []
    boss = None
    
    # Base ground platforms - connected with no gaps
    for i in range(0, WORLD_WIDTH, 200):
        platforms.append(Platform(i, SCREEN_HEIGHT - 40, 200, 40))  # Changed from 180 to 200 to eliminate gaps
    
    # Boss platform at the very end
    boss_platform_x = WORLD_WIDTH - 300
    platforms.append(Platform(boss_platform_x, SCREEN_HEIGHT - 100, 250, 60))
    
    if level_num == 1:
        # Level 1 - Simple layout
        platforms.extend([
            Platform(300, SCREEN_HEIGHT - 150, 120, 30),
            Platform(600, SCREEN_HEIGHT - 200, 150, 30),
            Platform(1000, SCREEN_HEIGHT - 180, 100, 30),
            Platform(1300, SCREEN_HEIGHT - 280, 120, 30),
            Platform(1600, SCREEN_HEIGHT - 320, 140, 30),
            Platform(2000, SCREEN_HEIGHT - 250, 100, 30),
            Platform(2300, SCREEN_HEIGHT - 400, 120, 30),
        ])
        
        # Robots (not near boss area)
        robots.extend([
            Robot(350, SCREEN_HEIGHT - 80),
            Robot(650, SCREEN_HEIGHT - 80),
            Robot(1050, SCREEN_HEIGHT - 210),
            Robot(1350, SCREEN_HEIGHT - 310),
            Robot(1650, SCREEN_HEIGHT - 350),
            Robot(2050, SCREEN_HEIGHT - 280),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 1)
        
    elif level_num == 2:
        # Level 2 - More complex
        platforms.extend([
            Platform(200, SCREEN_HEIGHT - 120, 100, 30),
            Platform(400, SCREEN_HEIGHT - 200, 120, 30),
            Platform(600, SCREEN_HEIGHT - 160, 80, 30),
            Platform(800, SCREEN_HEIGHT - 280, 100, 30),
            Platform(1000, SCREEN_HEIGHT - 220, 120, 30),
            Platform(1200, SCREEN_HEIGHT - 350, 100, 30),
            Platform(1400, SCREEN_HEIGHT - 180, 140, 30),
            Platform(1600, SCREEN_HEIGHT - 400, 120, 30),
            Platform(1800, SCREEN_HEIGHT - 300, 100, 30),
            Platform(2000, SCREEN_HEIGHT - 450, 120, 30),
            Platform(2200, SCREEN_HEIGHT - 250, 100, 30),
        ])
        
        robots.extend([
            Robot(250, SCREEN_HEIGHT - 80),
            Robot(450, SCREEN_HEIGHT - 230),
            Robot(650, SCREEN_HEIGHT - 190),
            Robot(850, SCREEN_HEIGHT - 310),
            Robot(1050, SCREEN_HEIGHT - 250),
            Robot(1250, SCREEN_HEIGHT - 380),
            Robot(1450, SCREEN_HEIGHT - 210),
            Robot(1850, SCREEN_HEIGHT - 330),
            Robot(2050, SCREEN_HEIGHT - 480),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 2)
        
    elif level_num == 3:
        # Level 3 - Vertical challenges
        platforms.extend([
            Platform(150, SCREEN_HEIGHT - 100, 80, 30),
            Platform(300, SCREEN_HEIGHT - 180, 100, 30),
            Platform(500, SCREEN_HEIGHT - 260, 80, 30),
            Platform(700, SCREEN_HEIGHT - 340, 100, 30),
            Platform(900, SCREEN_HEIGHT - 420, 80, 30),
            Platform(1100, SCREEN_HEIGHT - 500, 100, 30),
            Platform(1300, SCREEN_HEIGHT - 380, 120, 30),
            Platform(1500, SCREEN_HEIGHT - 280, 100, 30),
            Platform(1700, SCREEN_HEIGHT - 200, 80, 30),
            Platform(1900, SCREEN_HEIGHT - 320, 100, 30),
            Platform(2100, SCREEN_HEIGHT - 450, 120, 30),
            Platform(2300, SCREEN_HEIGHT - 350, 100, 30),
        ])
        
        robots.extend([
            Robot(200, SCREEN_HEIGHT - 130),
            Robot(350, SCREEN_HEIGHT - 210),
            Robot(550, SCREEN_HEIGHT - 290),
            Robot(750, SCREEN_HEIGHT - 370),
            Robot(950, SCREEN_HEIGHT - 450),
            Robot(1150, SCREEN_HEIGHT - 530),
            Robot(1350, SCREEN_HEIGHT - 410),
            Robot(1550, SCREEN_HEIGHT - 310),
            Robot(1950, SCREEN_HEIGHT - 350),
            Robot(2150, SCREEN_HEIGHT - 480),
            Robot(2350, SCREEN_HEIGHT - 380),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 3)
        
    elif level_num == 4:
        # Level 4 - Mixed challenges with tougher robots
        platforms.extend([
            Platform(100, SCREEN_HEIGHT - 120, 100, 30),
            Platform(250, SCREEN_HEIGHT - 200, 80, 30),
            Platform(400, SCREEN_HEIGHT - 150, 120, 30),
            Platform(600, SCREEN_HEIGHT - 280, 100, 30),
            Platform(800, SCREEN_HEIGHT - 200, 80, 30),
            Platform(1000, SCREEN_HEIGHT - 350, 120, 30),
            Platform(1200, SCREEN_HEIGHT - 250, 100, 30),
            Platform(1400, SCREEN_HEIGHT - 400, 80, 30),
            Platform(1600, SCREEN_HEIGHT - 180, 120, 30),
            Platform(1800, SCREEN_HEIGHT - 320, 100, 30),
            Platform(2000, SCREEN_HEIGHT - 450, 120, 30),
            Platform(2200, SCREEN_HEIGHT - 280, 100, 30),
            Platform(2400, SCREEN_HEIGHT - 380, 80, 30),
        ])
        
        robots.extend([
            Robot(150, SCREEN_HEIGHT - 80, "tough"),
            Robot(300, SCREEN_HEIGHT - 230, "normal"),
            Robot(450, SCREEN_HEIGHT - 180, "tough"),
            Robot(650, SCREEN_HEIGHT - 310, "normal"),
            Robot(850, SCREEN_HEIGHT - 230, "tough"),
            Robot(1050, SCREEN_HEIGHT - 380, "normal"),
            Robot(1250, SCREEN_HEIGHT - 280, "tough"),
            Robot(1450, SCREEN_HEIGHT - 430, "normal"),
            Robot(1650, SCREEN_HEIGHT - 210, "tough"),
            Robot(1850, SCREEN_HEIGHT - 350, "normal"),
            Robot(2050, SCREEN_HEIGHT - 480, "tough"),
            Robot(2250, SCREEN_HEIGHT - 310, "normal"),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 4)
        
    elif level_num == 5:  # Level 5 - Ultimate challenge
        # Level 5 - Ultimate challenge
        platforms.extend([
            Platform(80, SCREEN_HEIGHT - 100, 80, 30),
            Platform(200, SCREEN_HEIGHT - 180, 60, 30),
            Platform(320, SCREEN_HEIGHT - 260, 80, 30),
            Platform(480, SCREEN_HEIGHT - 340, 60, 30),
            Platform(600, SCREEN_HEIGHT - 420, 80, 30),
            Platform(750, SCREEN_HEIGHT - 500, 60, 30),
            Platform(900, SCREEN_HEIGHT - 380, 80, 30),
            Platform(1050, SCREEN_HEIGHT - 280, 60, 30),
            Platform(1200, SCREEN_HEIGHT - 200, 80, 30),
            Platform(1350, SCREEN_HEIGHT - 320, 60, 30),
            Platform(1500, SCREEN_HEIGHT - 450, 80, 30),
            Platform(1650, SCREEN_HEIGHT - 350, 60, 30),
            Platform(1800, SCREEN_HEIGHT - 250, 80, 30),
            Platform(1950, SCREEN_HEIGHT - 400, 60, 30),
            Platform(2100, SCREEN_HEIGHT - 300, 80, 30),
            Platform(2250, SCREEN_HEIGHT - 480, 60, 30),
            Platform(2400, SCREEN_HEIGHT - 380, 80, 30),
        ])
        
        robots.extend([
            Robot(130, SCREEN_HEIGHT - 80, "tough"),
            Robot(250, SCREEN_HEIGHT - 210, "tough"),
            Robot(370, SCREEN_HEIGHT - 290, "tough"),
            Robot(530, SCREEN_HEIGHT - 370, "tough"),
            Robot(650, SCREEN_HEIGHT - 450, "tough"),
            Robot(800, SCREEN_HEIGHT - 530, "tough"),
            Robot(950, SCREEN_HEIGHT - 410, "tough"),
            Robot(1100, SCREEN_HEIGHT - 310, "tough"),
            Robot(1250, SCREEN_HEIGHT - 230, "tough"),
            Robot(1400, SCREEN_HEIGHT - 350, "tough"),
            Robot(1550, SCREEN_HEIGHT - 480, "tough"),
            Robot(1700, SCREEN_HEIGHT - 380, "tough"),
            Robot(1850, SCREEN_HEIGHT - 280, "tough"),
            Robot(2000, SCREEN_HEIGHT - 430, "tough"),
            Robot(2150, SCREEN_HEIGHT - 330, "tough"),
            Robot(2300, SCREEN_HEIGHT - 510, "tough"),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 5)
        
    elif level_num == 6:
        # Level 6 - Narrow platforms challenge
        platforms.extend([
            Platform(120, SCREEN_HEIGHT - 100, 60, 30),
            Platform(220, SCREEN_HEIGHT - 180, 60, 30),
            Platform(350, SCREEN_HEIGHT - 260, 60, 30),
            Platform(480, SCREEN_HEIGHT - 340, 60, 30),
            Platform(610, SCREEN_HEIGHT - 420, 60, 30),
            Platform(740, SCREEN_HEIGHT - 500, 60, 30),
            Platform(870, SCREEN_HEIGHT - 420, 60, 30),
            Platform(1000, SCREEN_HEIGHT - 340, 60, 30),
            Platform(1130, SCREEN_HEIGHT - 260, 60, 30),
            Platform(1260, SCREEN_HEIGHT - 180, 60, 30),
            Platform(1390, SCREEN_HEIGHT - 100, 60, 30),
            Platform(1520, SCREEN_HEIGHT - 200, 80, 30),
            Platform(1650, SCREEN_HEIGHT - 350, 60, 30),
            Platform(1780, SCREEN_HEIGHT - 450, 60, 30),
            Platform(1910, SCREEN_HEIGHT - 350, 60, 30),
            Platform(2040, SCREEN_HEIGHT - 250, 80, 30),
            Platform(2170, SCREEN_HEIGHT - 400, 60, 30),
            Platform(2300, SCREEN_HEIGHT - 300, 60, 30),
            Platform(2430, SCREEN_HEIGHT - 200, 80, 30),
        ])
        
        robots.extend([
            Robot(150, SCREEN_HEIGHT - 80, "tough"),
            Robot(250, SCREEN_HEIGHT - 210, "tough"),
            Robot(380, SCREEN_HEIGHT - 290, "tough"),
            Robot(510, SCREEN_HEIGHT - 370, "tough"),
            Robot(640, SCREEN_HEIGHT - 450, "tough"),
            Robot(770, SCREEN_HEIGHT - 530, "tough"),
            Robot(900, SCREEN_HEIGHT - 450, "tough"),
            Robot(1030, SCREEN_HEIGHT - 370, "tough"),
            Robot(1160, SCREEN_HEIGHT - 290, "tough"),
            Robot(1290, SCREEN_HEIGHT - 210, "tough"),
            Robot(1420, SCREEN_HEIGHT - 130, "tough"),
            Robot(1550, SCREEN_HEIGHT - 230, "tough"),
            Robot(1680, SCREEN_HEIGHT - 380, "tough"),
            Robot(1810, SCREEN_HEIGHT - 480, "tough"),
            Robot(1940, SCREEN_HEIGHT - 380, "tough"),
            Robot(2070, SCREEN_HEIGHT - 280, "tough"),
            Robot(2200, SCREEN_HEIGHT - 430, "tough"),
            Robot(2330, SCREEN_HEIGHT - 330, "tough"),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 6)
        
    elif level_num == 7:
        # Level 7 - Speed and agility test
        platforms.extend([
            Platform(100, SCREEN_HEIGHT - 120, 80, 30),
            Platform(250, SCREEN_HEIGHT - 200, 70, 30),
            Platform(380, SCREEN_HEIGHT - 280, 60, 30),
            Platform(500, SCREEN_HEIGHT - 360, 70, 30),
            Platform(650, SCREEN_HEIGHT - 440, 60, 30),
            Platform(780, SCREEN_HEIGHT - 520, 70, 30),
            Platform(920, SCREEN_HEIGHT - 440, 60, 30),
            Platform(1050, SCREEN_HEIGHT - 360, 70, 30),
            Platform(1200, SCREEN_HEIGHT - 280, 60, 30),
            Platform(1330, SCREEN_HEIGHT - 200, 70, 30),
            Platform(1480, SCREEN_HEIGHT - 120, 80, 30),
            Platform(1630, SCREEN_HEIGHT - 240, 60, 30),
            Platform(1750, SCREEN_HEIGHT - 360, 70, 30),
            Platform(1900, SCREEN_HEIGHT - 480, 60, 30),
            Platform(2030, SCREEN_HEIGHT - 360, 70, 30),
            Platform(2180, SCREEN_HEIGHT - 240, 60, 30),
            Platform(2310, SCREEN_HEIGHT - 120, 80, 30),
            Platform(2460, SCREEN_HEIGHT - 280, 60, 30),
        ])
        
        # More robots with faster movement
        robots.extend([
            Robot(130, SCREEN_HEIGHT - 80, "tough"),
            Robot(280, SCREEN_HEIGHT - 230, "tough"),
            Robot(410, SCREEN_HEIGHT - 310, "tough"),
            Robot(530, SCREEN_HEIGHT - 390, "tough"),
            Robot(680, SCREEN_HEIGHT - 470, "tough"),
            Robot(810, SCREEN_HEIGHT - 550, "tough"),
            Robot(950, SCREEN_HEIGHT - 470, "tough"),
            Robot(1080, SCREEN_HEIGHT - 390, "tough"),
            Robot(1230, SCREEN_HEIGHT - 310, "tough"),
            Robot(1360, SCREEN_HEIGHT - 230, "tough"),
            Robot(1510, SCREEN_HEIGHT - 150, "tough"),
            Robot(1660, SCREEN_HEIGHT - 270, "tough"),
            Robot(1780, SCREEN_HEIGHT - 390, "tough"),
            Robot(1930, SCREEN_HEIGHT - 510, "tough"),
            Robot(2060, SCREEN_HEIGHT - 390, "tough"),
            Robot(2210, SCREEN_HEIGHT - 270, "tough"),
            Robot(2340, SCREEN_HEIGHT - 150, "tough"),
            Robot(2490, SCREEN_HEIGHT - 310, "tough"),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 7)
        
    elif level_num == 8:
        # Level 8 - Extreme vertical challenge
        platforms.extend([
            Platform(80, SCREEN_HEIGHT - 80, 60, 30),
            Platform(180, SCREEN_HEIGHT - 140, 50, 30),
            Platform(270, SCREEN_HEIGHT - 220, 50, 30),
            Platform(360, SCREEN_HEIGHT - 300, 50, 30),
            Platform(450, SCREEN_HEIGHT - 380, 50, 30),
            Platform(540, SCREEN_HEIGHT - 460, 50, 30),
            Platform(630, SCREEN_HEIGHT - 540, 50, 30),
            Platform(720, SCREEN_HEIGHT - 460, 50, 30),
            Platform(810, SCREEN_HEIGHT - 380, 50, 30),
            Platform(900, SCREEN_HEIGHT - 300, 50, 30),
            Platform(990, SCREEN_HEIGHT - 220, 50, 30),
            Platform(1080, SCREEN_HEIGHT - 140, 50, 30),
            Platform(1170, SCREEN_HEIGHT - 80, 60, 30),
            Platform(1280, SCREEN_HEIGHT - 180, 50, 30),
            Platform(1370, SCREEN_HEIGHT - 280, 50, 30),
            Platform(1460, SCREEN_HEIGHT - 380, 50, 30),
            Platform(1550, SCREEN_HEIGHT - 480, 50, 30),
            Platform(1640, SCREEN_HEIGHT - 380, 50, 30),
            Platform(1730, SCREEN_HEIGHT - 280, 50, 30),
            Platform(1820, SCREEN_HEIGHT - 180, 50, 30),
            Platform(1910, SCREEN_HEIGHT - 80, 60, 30),
            Platform(2020, SCREEN_HEIGHT - 200, 50, 30),
            Platform(2110, SCREEN_HEIGHT - 320, 50, 30),
            Platform(2200, SCREEN_HEIGHT - 440, 50, 30),
            Platform(2290, SCREEN_HEIGHT - 320, 50, 30),
            Platform(2380, SCREEN_HEIGHT - 200, 50, 30),
            Platform(2470, SCREEN_HEIGHT - 80, 60, 30),
        ])
        
        # Maximum robot density
        robots.extend([
            Robot(110, SCREEN_HEIGHT - 80, "tough"),
            Robot(210, SCREEN_HEIGHT - 170, "tough"),
            Robot(300, SCREEN_HEIGHT - 250, "tough"),
            Robot(390, SCREEN_HEIGHT - 330, "tough"),
            Robot(480, SCREEN_HEIGHT - 410, "tough"),
            Robot(570, SCREEN_HEIGHT - 490, "tough"),
            Robot(660, SCREEN_HEIGHT - 570, "tough"),
            Robot(750, SCREEN_HEIGHT - 490, "tough"),
            Robot(840, SCREEN_HEIGHT - 410, "tough"),
            Robot(930, SCREEN_HEIGHT - 330, "tough"),
            Robot(1020, SCREEN_HEIGHT - 250, "tough"),
            Robot(1110, SCREEN_HEIGHT - 170, "tough"),
            Robot(1200, SCREEN_HEIGHT - 110, "tough"),
            Robot(1310, SCREEN_HEIGHT - 210, "tough"),
            Robot(1400, SCREEN_HEIGHT - 310, "tough"),
            Robot(1490, SCREEN_HEIGHT - 410, "tough"),
            Robot(1580, SCREEN_HEIGHT - 510, "tough"),
            Robot(1670, SCREEN_HEIGHT - 410, "tough"),
            Robot(1760, SCREEN_HEIGHT - 310, "tough"),
            Robot(1850, SCREEN_HEIGHT - 210, "tough"),
            Robot(1940, SCREEN_HEIGHT - 110, "tough"),
            Robot(2050, SCREEN_HEIGHT - 230, "tough"),
            Robot(2140, SCREEN_HEIGHT - 350, "tough"),
            Robot(2230, SCREEN_HEIGHT - 470, "tough"),
            Robot(2320, SCREEN_HEIGHT - 350, "tough"),
            Robot(2410, SCREEN_HEIGHT - 230, "tough"),
            Robot(2500, SCREEN_HEIGHT - 110, "tough"),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 8)
        
    elif level_num == 9:
        # Level 9 - Gauntlet of death
        platforms.extend([
            Platform(60, SCREEN_HEIGHT - 100, 50, 30),
            Platform(140, SCREEN_HEIGHT - 160, 40, 30),
            Platform(210, SCREEN_HEIGHT - 240, 40, 30),
            Platform(280, SCREEN_HEIGHT - 320, 40, 30),
            Platform(350, SCREEN_HEIGHT - 400, 40, 30),
            Platform(420, SCREEN_HEIGHT - 480, 40, 30),
            Platform(490, SCREEN_HEIGHT - 560, 40, 30),
            Platform(560, SCREEN_HEIGHT - 480, 40, 30),
            Platform(630, SCREEN_HEIGHT - 400, 40, 30),
            Platform(700, SCREEN_HEIGHT - 320, 40, 30),
            Platform(770, SCREEN_HEIGHT - 240, 40, 30),
            Platform(840, SCREEN_HEIGHT - 160, 40, 30),
            Platform(910, SCREEN_HEIGHT - 100, 50, 30),
            Platform(990, SCREEN_HEIGHT - 180, 40, 30),
            Platform(1060, SCREEN_HEIGHT - 260, 40, 30),
            Platform(1130, SCREEN_HEIGHT - 340, 40, 30),
            Platform(1200, SCREEN_HEIGHT - 420, 40, 30),
            Platform(1270, SCREEN_HEIGHT - 500, 40, 30),
            Platform(1340, SCREEN_HEIGHT - 420, 40, 30),
            Platform(1410, SCREEN_HEIGHT - 340, 40, 30),
            Platform(1480, SCREEN_HEIGHT - 260, 40, 30),
            Platform(1550, SCREEN_HEIGHT - 180, 40, 30),
            Platform(1620, SCREEN_HEIGHT - 100, 50, 30),
            Platform(1700, SCREEN_HEIGHT - 200, 40, 30),
            Platform(1770, SCREEN_HEIGHT - 300, 40, 30),
            Platform(1840, SCREEN_HEIGHT - 400, 40, 30),
            Platform(1910, SCREEN_HEIGHT - 500, 40, 30),
            Platform(1980, SCREEN_HEIGHT - 400, 40, 30),
            Platform(2050, SCREEN_HEIGHT - 300, 40, 30),
            Platform(2120, SCREEN_HEIGHT - 200, 40, 30),
            Platform(2190, SCREEN_HEIGHT - 100, 50, 30),
            Platform(2270, SCREEN_HEIGHT - 220, 40, 30),
            Platform(2340, SCREEN_HEIGHT - 340, 40, 30),
            Platform(2410, SCREEN_HEIGHT - 460, 40, 30),
            Platform(2480, SCREEN_HEIGHT - 340, 40, 30),
            Platform(2550, SCREEN_HEIGHT - 220, 40, 30),
        ])
        
        # Overwhelming robot army
        robots.extend([
            Robot(90, SCREEN_HEIGHT - 80, "tough"),
            Robot(170, SCREEN_HEIGHT - 190, "tough"),
            Robot(240, SCREEN_HEIGHT - 270, "tough"),
            Robot(310, SCREEN_HEIGHT - 350, "tough"),
            Robot(380, SCREEN_HEIGHT - 430, "tough"),
            Robot(450, SCREEN_HEIGHT - 510, "tough"),
            Robot(520, SCREEN_HEIGHT - 590, "tough"),
            Robot(590, SCREEN_HEIGHT - 510, "tough"),
            Robot(660, SCREEN_HEIGHT - 430, "tough"),
            Robot(730, SCREEN_HEIGHT - 350, "tough"),
            Robot(800, SCREEN_HEIGHT - 270, "tough"),
            Robot(870, SCREEN_HEIGHT - 190, "tough"),
            Robot(940, SCREEN_HEIGHT - 130, "tough"),
            Robot(1020, SCREEN_HEIGHT - 210, "tough"),
            Robot(1090, SCREEN_HEIGHT - 290, "tough"),
            Robot(1160, SCREEN_HEIGHT - 370, "tough"),
            Robot(1230, SCREEN_HEIGHT - 450, "tough"),
            Robot(1300, SCREEN_HEIGHT - 530, "tough"),
            Robot(1370, SCREEN_HEIGHT - 450, "tough"),
            Robot(1440, SCREEN_HEIGHT - 370, "tough"),
            Robot(1510, SCREEN_HEIGHT - 290, "tough"),
            Robot(1580, SCREEN_HEIGHT - 210, "tough"),
            Robot(1650, SCREEN_HEIGHT - 130, "tough"),
            Robot(1730, SCREEN_HEIGHT - 230, "tough"),
            Robot(1800, SCREEN_HEIGHT - 330, "tough"),
            Robot(1870, SCREEN_HEIGHT - 430, "tough"),
            Robot(1940, SCREEN_HEIGHT - 530, "tough"),
            Robot(2010, SCREEN_HEIGHT - 430, "tough"),
            Robot(2080, SCREEN_HEIGHT - 330, "tough"),
            Robot(2150, SCREEN_HEIGHT - 230, "tough"),
            Robot(2220, SCREEN_HEIGHT - 130, "tough"),
            Robot(2300, SCREEN_HEIGHT - 250, "tough"),
            Robot(2370, SCREEN_HEIGHT - 370, "tough"),
            Robot(2440, SCREEN_HEIGHT - 490, "tough"),
            Robot(2510, SCREEN_HEIGHT - 370, "tough"),
            Robot(2580, SCREEN_HEIGHT - 250, "tough"),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 9)
        
    else:  # Level 10 - Final ultimate challenge
        # Level 10 - The ultimate test
        platforms.extend([
            Platform(50, SCREEN_HEIGHT - 80, 40, 30),
            Platform(120, SCREEN_HEIGHT - 140, 35, 30),
            Platform(180, SCREEN_HEIGHT - 200, 35, 30),
            Platform(240, SCREEN_HEIGHT - 260, 35, 30),
            Platform(300, SCREEN_HEIGHT - 320, 35, 30),
            Platform(360, SCREEN_HEIGHT - 380, 35, 30),
            Platform(420, SCREEN_HEIGHT - 440, 35, 30),
            Platform(480, SCREEN_HEIGHT - 500, 35, 30),
            Platform(540, SCREEN_HEIGHT - 560, 35, 30),
            Platform(600, SCREEN_HEIGHT - 500, 35, 30),
            Platform(660, SCREEN_HEIGHT - 440, 35, 30),
            Platform(720, SCREEN_HEIGHT - 380, 35, 30),
            Platform(780, SCREEN_HEIGHT - 320, 35, 30),
            Platform(840, SCREEN_HEIGHT - 260, 35, 30),
            Platform(900, SCREEN_HEIGHT - 200, 35, 30),
            Platform(960, SCREEN_HEIGHT - 140, 35, 30),
            Platform(1020, SCREEN_HEIGHT - 80, 40, 30),
            Platform(1090, SCREEN_HEIGHT - 160, 35, 30),
            Platform(1150, SCREEN_HEIGHT - 240, 35, 30),
            Platform(1210, SCREEN_HEIGHT - 320, 35, 30),
            Platform(1270, SCREEN_HEIGHT - 400, 35, 30),
            Platform(1330, SCREEN_HEIGHT - 480, 35, 30),
            Platform(1390, SCREEN_HEIGHT - 560, 35, 30),
            Platform(1450, SCREEN_HEIGHT - 480, 35, 30),
            Platform(1510, SCREEN_HEIGHT - 400, 35, 30),
            Platform(1570, SCREEN_HEIGHT - 320, 35, 30),
            Platform(1630, SCREEN_HEIGHT - 240, 35, 30),
            Platform(1690, SCREEN_HEIGHT - 160, 35, 30),
            Platform(1750, SCREEN_HEIGHT - 80, 40, 30),
            Platform(1820, SCREEN_HEIGHT - 180, 35, 30),
            Platform(1880, SCREEN_HEIGHT - 280, 35, 30),
            Platform(1940, SCREEN_HEIGHT - 380, 35, 30),
            Platform(2000, SCREEN_HEIGHT - 480, 35, 30),
            Platform(2060, SCREEN_HEIGHT - 580, 35, 30),
            Platform(2120, SCREEN_HEIGHT - 480, 35, 30),
            Platform(2180, SCREEN_HEIGHT - 380, 35, 30),
            Platform(2240, SCREEN_HEIGHT - 280, 35, 30),
            Platform(2300, SCREEN_HEIGHT - 180, 35, 30),
            Platform(2360, SCREEN_HEIGHT - 80, 40, 30),
            Platform(2430, SCREEN_HEIGHT - 200, 35, 30),
            Platform(2490, SCREEN_HEIGHT - 320, 35, 30),
            Platform(2550, SCREEN_HEIGHT - 440, 35, 30),
            Platform(2610, SCREEN_HEIGHT - 320, 35, 30),
            Platform(2670, SCREEN_HEIGHT - 200, 35, 30),
        ])
        
        # Maximum difficulty - robot army
        robots.extend([
            Robot(80, SCREEN_HEIGHT - 80, "tough"),
            Robot(150, SCREEN_HEIGHT - 170, "tough"),
            Robot(210, SCREEN_HEIGHT - 230, "tough"),
            Robot(270, SCREEN_HEIGHT - 290, "tough"),
            Robot(330, SCREEN_HEIGHT - 350, "tough"),
            Robot(390, SCREEN_HEIGHT - 410, "tough"),
            Robot(450, SCREEN_HEIGHT - 470, "tough"),
            Robot(510, SCREEN_HEIGHT - 530, "tough"),
            Robot(570, SCREEN_HEIGHT - 590, "tough"),
            Robot(630, SCREEN_HEIGHT - 530, "tough"),
            Robot(690, SCREEN_HEIGHT - 470, "tough"),
            Robot(750, SCREEN_HEIGHT - 410, "tough"),
            Robot(810, SCREEN_HEIGHT - 350, "tough"),
            Robot(870, SCREEN_HEIGHT - 290, "tough"),
            Robot(930, SCREEN_HEIGHT - 230, "tough"),
            Robot(990, SCREEN_HEIGHT - 170, "tough"),
            Robot(1050, SCREEN_HEIGHT - 110, "tough"),
            Robot(1120, SCREEN_HEIGHT - 190, "tough"),
            Robot(1180, SCREEN_HEIGHT - 270, "tough"),
            Robot(1240, SCREEN_HEIGHT - 350, "tough"),
            Robot(1300, SCREEN_HEIGHT - 430, "tough"),
            Robot(1360, SCREEN_HEIGHT - 510, "tough"),
            Robot(1420, SCREEN_HEIGHT - 590, "tough"),
            Robot(1480, SCREEN_HEIGHT - 510, "tough"),
            Robot(1540, SCREEN_HEIGHT - 430, "tough"),
            Robot(1600, SCREEN_HEIGHT - 350, "tough"),
            Robot(1660, SCREEN_HEIGHT - 270, "tough"),
            Robot(1720, SCREEN_HEIGHT - 190, "tough"),
            Robot(1780, SCREEN_HEIGHT - 110, "tough"),
            Robot(1850, SCREEN_HEIGHT - 210, "tough"),
            Robot(1910, SCREEN_HEIGHT - 310, "tough"),
            Robot(1970, SCREEN_HEIGHT - 410, "tough"),
            Robot(2030, SCREEN_HEIGHT - 510, "tough"),
            Robot(2090, SCREEN_HEIGHT - 610, "tough"),
            Robot(2150, SCREEN_HEIGHT - 510, "tough"),
            Robot(2210, SCREEN_HEIGHT - 410, "tough"),
            Robot(2270, SCREEN_HEIGHT - 310, "tough"),
            Robot(2330, SCREEN_HEIGHT - 210, "tough"),
            Robot(2390, SCREEN_HEIGHT - 110, "tough"),
            Robot(2460, SCREEN_HEIGHT - 230, "tough"),
            Robot(2520, SCREEN_HEIGHT - 350, "tough"),
            Robot(2580, SCREEN_HEIGHT - 470, "tough"),
            Robot(2640, SCREEN_HEIGHT - 350, "tough"),
            Robot(2700, SCREEN_HEIGHT - 230, "tough"),
        ])
        
        boss = Boss(boss_platform_x + 50, SCREEN_HEIGHT - 160, 10)
    
    # Add diamonds throughout the level (but not in boss area)
    diamond_positions = []
    for platform in platforms[1:-1]:  # Skip ground platforms and boss platform
        if platform.rect.x < WORLD_WIDTH - 500:  # Don't place diamonds near boss
            # Add diamonds on platforms
            for i in range(2):
                diamond_x = platform.rect.x + random.randint(10, platform.rect.width - 20)
                diamond_y = platform.rect.y - 20
                diamond_positions.append((diamond_x, diamond_y))
    
    # Add some floating diamonds (not near boss area)
    for i in range(level_num * 5):
        x = random.randint(100, WORLD_WIDTH - 600)  # Keep away from boss area
        y = random.randint(200, SCREEN_HEIGHT - 200)
        diamond_positions.append((x, y))
    
    for pos in diamond_positions:
        diamonds.append(Diamond(pos[0], pos[1]))
    
    # Add SuperDiamonds (fewer, more strategic placement)
    power_types = ["speed", "jump", "invincible", "strength"]
    superdiamond_count = min(level_num + 1, 4)  # More superdiamonds in later levels
    
    for i in range(superdiamond_count):
        # Place superdiamonds on higher platforms or in challenging locations
        suitable_platforms = [p for p in platforms[1:-1] 
                            if p.rect.y < SCREEN_HEIGHT - 200 and p.rect.x < WORLD_WIDTH - 600]
        if suitable_platforms:
            platform = random.choice(suitable_platforms)
            power_type = power_types[i % len(power_types)]
            superdiamond_x = platform.rect.x + platform.rect.width // 2
            superdiamond_y = platform.rect.y - 30
            superdiamonds.append(SuperDiamond(superdiamond_x, superdiamond_y, power_type))
    
    return platforms, robots, diamonds, superdiamonds, boss

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Retro Platform Fighter - Diamond Quest")
    clock = pygame.time.Clock()
    
    # Game state
    current_level = 1
    score = 0
    camera_x = 0
    game_state = "playing"  # "playing", "level_complete", "game_over", "victory"
    transition_timer = 0
    
    # Create game objects
    player = Player(100, SCREEN_HEIGHT - 200)
    platforms, robots, diamonds, superdiamonds, boss = create_level(current_level)
    
    # Fonts
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and (game_state == "game_over" or game_state == "victory"):
                    # Restart game
                    current_level = 1
                    score = 0
                    player = Player(100, SCREEN_HEIGHT - 200)
                    platforms, robots, diamonds, superdiamonds, boss = create_level(current_level)
                    game_state = "playing"
                    camera_x = 0
                elif event.key == pygame.K_RETURN and game_state == "level_complete":
                    # Next level
                    current_level += 1
                    if current_level > 10:  # Changed from 5 to 10
                        game_state = "victory"
                    else:
                        player = Player(100, SCREEN_HEIGHT - 200)
                        platforms, robots, diamonds, superdiamonds, boss = create_level(current_level)
                        game_state = "playing"
                        camera_x = 0
        
        if game_state == "playing":
            # Update camera to follow player
            target_camera_x = player.x - SCREEN_WIDTH // 2
            target_camera_x = max(0, min(target_camera_x, WORLD_WIDTH - SCREEN_WIDTH))
            camera_x += (target_camera_x - camera_x) * 0.1
            
            # Update game objects
            if player.lives > 0:
                player.update(platforms, camera_x)
                
                # Update diamonds
                for diamond in diamonds[:]:
                    diamond.update(player)
                    if diamond.collected:
                        diamonds.remove(diamond)
                        score += 10
                
                # Update superdiamonds
                for superdiamond in superdiamonds[:]:
                    superdiamond.update(player)
                    if superdiamond.collected:
                        superdiamonds.remove(superdiamond)
                        score += 50  # SuperDiamonds are worth more points
                
                # Update robots
                for robot in robots[:]:
                    robot.update(platforms, player)
                    if not robot.alive:
                        robots.remove(robot)
                        score += 100
                
                # Update boss
                if boss and boss.alive:
                    boss.update(platforms, player)
                    if not boss.alive:
                        score += 500
                        # Don't immediately complete level - check if all enemies are dead
                
                # Check level completion: both all robots AND boss must be defeated
                robots_alive = len([r for r in robots if r.alive])
                boss_alive = boss and boss.alive
                
                if robots_alive == 0 and not boss_alive:
                    sound_manager.play_sound('level_complete')
                    game_state = "level_complete"
                    transition_timer = 180  # 3 seconds
                
                # Check if player reached boss area without defeating all robots
                if player.x > WORLD_WIDTH - 500 and robots_alive > 0:
                    # Push player back
                    player.x = WORLD_WIDTH - 500
                    
            else:
                game_state = "game_over"
        
        elif game_state == "level_complete":
            transition_timer -= 1
            if transition_timer <= 0:
                # Auto-advance after showing completion message
                current_level += 1
                if current_level > 10:  # Changed from 5 to 10
                    game_state = "victory"
                else:
                    player = Player(100, SCREEN_HEIGHT - 200)
                    platforms, robots, diamonds, superdiamonds, boss = create_level(current_level)
                    game_state = "playing"
                    camera_x = 0
        
        # Draw everything
        screen.fill(BLUE)  # Sky background
        
        if game_state == "playing" or game_state == "level_complete":
            # Draw platforms
            for platform in platforms:
                platform.draw(screen, camera_x)
            
            # Draw diamonds
            for diamond in diamonds:
                diamond.draw(screen, camera_x)
            
            # Draw superdiamonds
            for superdiamond in superdiamonds:
                superdiamond.draw(screen, camera_x)
            
            # Draw robots
            for robot in robots:
                robot.draw(screen, camera_x)
            
            # Draw boss
            if boss:
                boss.draw(screen, camera_x)
            
            # Draw player
            if player.lives > 0:
                player.draw(screen, camera_x)
            
            # Draw UI
            diamonds_text = font.render(f"Diamonds: {player.diamonds}", True, WHITE)
            screen.blit(diamonds_text, (10, 10))
            
            lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
            screen.blit(lives_text, (10, 50))
            
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 90))
            
            level_text = font.render(f"Level: {current_level}", True, WHITE)
            screen.blit(level_text, (10, 130))
            
            robots_left = len([r for r in robots if r.alive])
            boss_alive = boss and boss.alive
            
            # Show robots left
            robots_text = font.render(f"Robots Left: {robots_left}", True, WHITE)
            screen.blit(robots_text, (10, 170))
            
            # Show boss status
            if boss:
                boss_status = "Boss: Alive" if boss_alive else "Boss: Defeated"
                boss_color = RED if boss_alive else GREEN
                boss_text = font.render(boss_status, True, boss_color)
                screen.blit(boss_text, (10, 195))
            
            # Show level completion requirement
            if robots_left == 0 and boss_alive:
                requirement_text = font.render("Defeat the Boss to complete level!", True, YELLOW)
                screen.blit(requirement_text, (10, 220))
            elif robots_left > 0 and not boss_alive:
                requirement_text = font.render("Defeat all robots to complete level!", True, YELLOW)
                screen.blit(requirement_text, (10, 220))
            elif robots_left > 0 and boss_alive:
                requirement_text = font.render("Defeat all enemies to complete level!", True, YELLOW)
                screen.blit(requirement_text, (10, 220))
            
            # Power-up status display
            power_y = 250  # Moved down to accommodate new UI elements
            active_powers = [power for power, timer in player.powers.items() if timer > 0]
            if active_powers:
                powers_text = pygame.font.Font(None, 24).render("Active Powers:", True, YELLOW)
                screen.blit(powers_text, (10, power_y))
                power_y += 25
                
                power_colors = {
                    "speed": (255, 255, 0),
                    "jump": (0, 255, 0),
                    "invincible": (255, 0, 255),
                    "strength": (255, 100, 0)
                }
                
                for power in active_powers:
                    time_left = player.powers[power] // 60  # Convert to seconds
                    color = power_colors.get(power, WHITE)
                    power_text = pygame.font.Font(None, 20).render(
                        f"{power.upper()}: {time_left}s", True, color)
                    screen.blit(power_text, (10, power_y))
                    power_y += 22
            
            # Instructions
            instructions = [
                "Arrow Keys/WASD: Move & Jump",
                "X: Punch, Z: Kick",
                "Collect diamonds & superdiamonds!",
                "SuperDiamonds give special powers:",
                "Yellow=Speed, Green=Jump, Pink=Invincible, Orange=Strength",
                "Defeat ALL robots AND boss to complete level!",
                "ESC: Quit"
            ]
            
            for i, instruction in enumerate(instructions):
                text = pygame.font.Font(None, 20).render(instruction, True, WHITE)
                screen.blit(text, (SCREEN_WIDTH - 280, 10 + i * 22))
            
            # Level complete message
            if game_state == "level_complete":
                complete_text = big_font.render("LEVEL COMPLETE!", True, YELLOW)
                screen.blit(complete_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 50))
                
                if current_level < 10:  # Changed from 5 to 10
                    next_text = font.render("Press ENTER for next level", True, WHITE)
                    screen.blit(next_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 20))
                else:
                    final_text = font.render("Final level completed!", True, WHITE)
                    screen.blit(final_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 20))
        
        elif game_state == "game_over":
            game_over_text = big_font.render("GAME OVER!", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
            
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(final_score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
            
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 60))
            
        elif game_state == "victory":
            victory_text = big_font.render("VICTORY!", True, YELLOW)
            screen.blit(victory_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 100))
            
            congrats_text = font.render("You defeated all 10 levels!", True, WHITE)
            screen.blit(congrats_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 30))
            
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(final_score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 10))
            
            restart_text = font.render("Press R to play again", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 50))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
