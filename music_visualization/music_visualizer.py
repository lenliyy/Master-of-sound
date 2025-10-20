import sounddevice as sd
import numpy as np
import pygame
import librosa
from typing import List, Tuple
import colorsys
import math
import time

class MusicVisualizer:
    def __init__(self, width: int = 800, height: int = 600):
        # Initialize pygame
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pulse Music Visualizer")
        
        # Audio settings
        self.sample_rate = 44100
        self.block_size = 2048
        self.channels = 1
        
        # Particle settings
        self.particles = []
        self.max_particles = 150
        self.pulse_radius = 50
        self.pulse_speed = 2
        
        # Audio analysis settings
        self.energy_history = []
        self.max_history = 50
        self.started = False  # Whether the start button has been clicked
        self.recording = False
        self.countdown = 3  # Countdown seconds before recording
        
        # Button settings
        self.button_radius = 40
        self.button_center = (width // 2, height // 2 - 20)  # Moved up to make room for text
        self.button_color = (255, 59, 48)  # Apple red
        self.button_hover_color = (255, 89, 78)  # Lighter red
        self.button_pressed_color = (200, 35, 28)  # Darker red
        
    def create_particle(self, energy):
        """Create a new particle with pulse effect"""
        angle = np.random.random() * 2 * np.pi
        speed = self.pulse_speed * (0.5 + energy * 5)  # Speed affected by audio energy
        
        # Calculate gradient color based on energy
        intensity = min(1.0, energy * 10)
        color1 = np.array([255, 89, 94])  # Coral red
        color2 = np.array([255, 202, 58])  # Warm yellow
        color = tuple(map(int, color1 * (1 - intensity) + color2 * intensity))
        
        return {
            'pos': [self.width/2, self.height/2],
            'velocity': (math.cos(angle) * speed, math.sin(angle) * speed),
            'radius': self.pulse_radius,
            'color': color,
            'alpha': 255,
            'life': 1.0
        }
        
    def audio_callback(self, indata, frames, time, status):
        """Process audio input in real-time"""
        if status:
            print(status)
        
        if not self.recording:
            return
            
        # Convert to mono if necessary
        if self.channels == 2:
            audio_data = np.mean(indata, axis=1)
        else:
            audio_data = indata[:, 0]
            
        # Calculate audio features
        energy = np.sum(np.abs(audio_data)) / len(audio_data)
        
        # Create new particles based on audio energy
        if len(self.particles) < self.max_particles:
            self.particles.append(self.create_particle(energy))
            
        # Store energy history
        self.energy_history.append(energy)
        if len(self.energy_history) > self.max_history:
            self.energy_history.pop(0)
    
    def update_particles(self):
        """Update particle positions and properties"""
        for particle in self.particles[:]:
            # Update position
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]
            
            # Update particle properties
            particle['radius'] += self.pulse_speed
            particle['alpha'] = int(255 * particle['life'])
            particle['life'] -= 0.01
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def is_mouse_over_button(self, mouse_pos):
        """Check if mouse is over the circular button"""
        return math.dist(mouse_pos, self.button_center) <= self.button_radius
    
    def draw_button(self, mouse_pos):
        """Draw the start button"""
        # Determine button color based on mouse position
        color = self.button_hover_color if self.is_mouse_over_button(mouse_pos) else self.button_color
        
        # Draw main circle button
        pygame.draw.circle(self.screen, color, self.button_center, self.button_radius)
        
        # Add highlight effect
        highlight_radius = self.button_radius - 2
        pygame.draw.circle(self.screen, (255, 255, 255, 128), 
                         (self.button_center[0], self.button_center[1] - 2), 
                         highlight_radius, 2)
        
        # Draw "Start" text below the button
        font = pygame.font.Font(None, 36)
        text = font.render("Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.button_center[0], self.button_center[1] + self.button_radius + 20))
        self.screen.blit(text, text_rect)
    
    def draw_countdown(self):
        """Draw countdown before recording starts"""
        font = pygame.font.Font(None, 74)
        text = font.render(str(max(1, int(self.countdown))), True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        self.screen.blit(text, text_rect)
    
    def draw(self):
        """Draw the visualization"""
        # Fill background with dark color
        self.screen.fill((15, 15, 35))
        
        mouse_pos = pygame.mouse.get_pos()
        
        if not self.started:
            self.draw_button(mouse_pos)
        elif not self.recording and self.countdown > 0:
            self.draw_countdown()
        else:
            # Draw particles
            for particle in self.particles:
                s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.circle(s, (*particle['color'], particle['alpha']),
                                (int(particle['pos'][0]), int(particle['pos'][1])),
                                int(particle['radius']), 2)
                self.screen.blit(s, (0,0))
        
        pygame.display.flip()
    
    def run(self):
        """Main loop"""
        try:
            with sd.InputStream(callback=self.audio_callback,
                              channels=self.channels,
                              samplerate=self.sample_rate,
                              blocksize=self.block_size):
                print("等待用户点击开始按钮...")
                
                start_time = None
                running = True
                clock = pygame.time.Clock()
                
                while running:
                    current_time = time.time()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if not self.started and self.is_mouse_over_button(event.pos):
                                self.started = True
                                start_time = current_time
                                print("准备开始录音...")
                                print("3秒倒计时后开始...")
                    
                    if self.started and not self.recording:
                        self.countdown = 3 - (current_time - start_time)
                        if self.countdown <= 0:
                            self.recording = True
                            print("开始录音！请说话或播放音乐...")
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    
                    if self.recording:
                        self.update_particles()
                    self.draw()
                    clock.tick(60)  # Cap at 60 FPS
                    
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            pygame.quit()

if __name__ == "__main__":
    visualizer = MusicVisualizer()
    visualizer.run()