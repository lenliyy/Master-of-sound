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
        pygame.display.set_caption("Multi-style Music Visualizer")
        
        # Audio settings
        self.sample_rate = 44100
        self.block_size = 2048
        self.channels = 1
        
        # Visualization settings
        self.current_style = 1  # Default to pulse style
        self.style_names = {
            1: "Pulse Particles",
            2: "Wave Lines",
            3: "Star Field",
            4: "Geometric Shapes",
            5: "Fluid Ripples"
        }
        
        # Particle settings (Style 1)
        self.particles = []
        self.max_particles = 150
        self.pulse_radius = 50
        self.pulse_speed = 2
        
        # Wave settings (Style 2)
        self.wave_points = []
        self.wave_history = []
        self.max_wave_history = 50
        
        # Star settings (Style 3)
        self.stars = []
        self.max_stars = 200
        
        # Geometric settings (Style 4)
        self.shapes = []
        self.max_shapes = 10
        self.rotation = 0
        
        # Fluid settings (Style 5)
        self.ripples = []
        self.max_ripples = 20
        self.fluid_time = 0
        
        # Audio analysis settings
        self.energy_history = []
        self.max_history = 50
        self.started = False  # Whether the start button has been clicked
        self.recording = False
        self.countdown = 3  # Countdown seconds before recording
        
        # Button settings
        self.start_button_radius = 40
        self.start_button_center = (width // 2, height // 2 - 20)
        self.button_color = (255, 59, 48)  # Apple red
        self.button_hover_color = (255, 89, 78)  # Lighter red
        self.button_pressed_color = (200, 35, 28)  # Darker red
        
        # Style buttons settings
        self.style_buttons = []
        button_width = 100
        button_height = 30
        button_margin = 10
        total_width = (button_width + button_margin) * 5 - button_margin
        start_x = (width - total_width) // 2
        
        colors = [
            (255, 89, 94),   # Red for Pulse
            (45, 149, 150),  # Teal for Wave
            (132, 94, 194),  # Purple for Stars
            (255, 170, 51),  # Orange for Geometric
            (29, 185, 84)    # Green for Fluid
        ]
        
        for i in range(5):
            self.style_buttons.append({
                'rect': pygame.Rect(
                    start_x + i * (button_width + button_margin),
                    height - 50,
                    button_width,
                    button_height
                ),
                'color': colors[i],
                'hover_color': tuple(min(255, c + 30) for c in colors[i]),
                'text': f'Style {i+1}',
                'style_num': i + 1
            })
        
    def create_particle(self, energy):
        """Create a new particle with pulse effect (Style 1)"""
        angle = np.random.random() * 2 * np.pi
        speed = self.pulse_speed * (0.5 + energy * 5)
        
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
    
    def create_star(self, energy):
        """Create a new star (Style 3)"""
        # 根据能量决定星星出现的位置（能量大时更集中在中心）
        spread = max(0.2, 1.0 - energy * 2)  # 能量越大，spread越小
        center_offset_x = (np.random.random() - 0.5) * self.width * spread
        center_offset_y = (np.random.random() - 0.5) * self.height * spread
        
        # 在紫色和白色之间过渡
        # 紫色基础：RGB(147, 112, 219)
        # 白色：RGB(255, 255, 255)
        purple = np.array([147, 112, 219])
        white = np.array([255, 255, 255])
        
        # 根据能量在紫色和白色之间插值
        transition = min(1.0, energy * 3)  # 能量大时更偏向白色
        color = tuple(int(c) for c in purple * (1 - transition) + white * transition)
        
        # 星星大小和速度都受能量影响
        size = max(4, min(15, energy * 60))  # 更大的尺寸范围
        speed = energy * 5  # 移动速度随能量变化
        angle = np.random.random() * 2 * np.pi
        
        return {
            'pos': [self.width/2 + center_offset_x, self.height/2 + center_offset_y],
            'velocity': (math.cos(angle) * speed, math.sin(angle) * speed),
            'size': size,
            'base_size': size,  # 保存原始大小用于脉动效果
            'brightness': min(255, energy * 2000),
            'color': color,
            'pulse_phase': np.random.random() * 2 * np.pi,  # 用于制造脉动效果
            'pulse_speed': 0.1,  # 脉动速度
            'life': 1.0
        }
    
    def create_shape(self, energy):
        """Create a new geometric shape (Style 4)"""
        shape_type = np.random.choice(['triangle', 'square', 'pentagon'])
        # 在屏幕范围内随机位置
        pos_x = self.width/2 + np.random.randint(-200, 200)
        pos_y = self.height/2 + np.random.randint(-150, 150)
        
        # 生成明亮的颜色
        hue = np.random.random()  # 随机色相
        color = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.8, 1.0))
        
        return {
            'pos': [pos_x, pos_y],
            'type': shape_type,
            'size': 40 + energy * 200,  # 增大基础大小和能量影响
            'rotation': np.random.random() * 360,
            'color': color,
            'rotation_speed': np.random.random() * 4 - 2,  # 随机旋转速度
            'life': 1.0
        }
    
    def create_ripple(self, energy):
        """Create a new ripple (Style 5)"""
        return {
            'pos': [self.width/2 + np.random.randint(-100, 100), 
                   self.height/2 + np.random.randint(-100, 100)],
            'radius': 5,
            'max_radius': 100 + energy * 200,
            'color': (0, 150, 255),
            'width': 2,
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
        spectrum = np.abs(np.fft.fft(audio_data))[:len(audio_data)//2]
        spectrum = spectrum / len(spectrum)
        
        # Process based on current style
        if self.current_style == 1:  # Pulse Particles
            if len(self.particles) < self.max_particles:
                self.particles.append(self.create_particle(energy))
        
        elif self.current_style == 2:  # Wave Lines
            self.wave_points = []
            for i, amp in enumerate(spectrum[:100]):
                x = i * (self.width / 100)
                y = self.height/2 + amp * self.height * 2
                self.wave_points.append((int(x), int(y)))  # Convert to integers
            
            if len(self.wave_points) > 1:  # Only add if we have valid points
                self.wave_history.append(self.wave_points)
                if len(self.wave_history) > self.max_wave_history:
                    self.wave_history.pop(0)
                
        elif self.current_style == 3:  # Star Field
            if len(self.stars) < self.max_stars:
                self.stars.append(self.create_star(energy))
                
        elif self.current_style == 4:  # Geometric Shapes
            if len(self.shapes) < self.max_shapes:
                self.shapes.append(self.create_shape(energy))
                
        elif self.current_style == 5:  # Fluid Ripples
            if len(self.ripples) < self.max_ripples:
                self.ripples.append(self.create_ripple(energy))
        
        # Store energy history
        self.energy_history.append(energy)
        if len(self.energy_history) > self.max_history:
            self.energy_history.pop(0)
    
    def update_particles(self):
        """Update all visualization elements"""
        # Update Style 1: Pulse Particles
        for particle in self.particles[:]:
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]
            particle['radius'] += self.pulse_speed
            particle['alpha'] = int(255 * particle['life'])
            particle['life'] -= 0.01
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Update Style 3: Stars
        for star in self.stars[:]:
            star['life'] -= 0.005
            if star['life'] <= 0:
                self.stars.remove(star)
        
        # Update Style 4: Geometric Shapes
        for shape in self.shapes[:]:
            shape['rotation'] += shape['rotation_speed']  # 使用独立的旋转速度
            shape['size'] *= 0.99  # 降低缩小速度
            shape['life'] -= 0.008  # 延长生命周期
            if shape['life'] <= 0 or shape['size'] < 10:
                self.shapes.remove(shape)
        
        # Update Style 5: Fluid Ripples
        for ripple in self.ripples[:]:
            ripple['radius'] = min(ripple['radius'] + 2, ripple['max_radius'])
            ripple['life'] -= 0.01
            if ripple['life'] <= 0:
                self.ripples.remove(ripple)
    
    def is_mouse_over_start_button(self, mouse_pos):
        """Check if mouse is over the circular start button"""
        return math.dist(mouse_pos, self.start_button_center) <= self.start_button_radius
    
    def get_style_button_at_pos(self, mouse_pos):
        """Get the style button at the given position, if any"""
        for button in self.style_buttons:
            if button['rect'].collidepoint(mouse_pos):
                return button
        return None
    
    def draw_start_button(self, mouse_pos):
        """Draw the start button"""
        # Determine button color based on mouse position
        color = self.button_hover_color if self.is_mouse_over_start_button(mouse_pos) else self.button_color
        
        # Draw main circle button
        pygame.draw.circle(self.screen, color, self.start_button_center, self.start_button_radius)
        
        # Add highlight effect
        highlight_radius = self.start_button_radius - 2
        pygame.draw.circle(self.screen, (255, 255, 255, 128), 
                         (self.start_button_center[0], self.start_button_center[1] - 2), 
                         highlight_radius, 2)
        
        # Draw "Start" text below the button
        font = pygame.font.Font(None, 36)
        text = font.render("Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.start_button_center[0], 
                                        self.start_button_center[1] + self.start_button_radius + 20))
        self.screen.blit(text, text_rect)
    
    def draw_wave_lines(self):
        """Draw wave line visualization (Style 2)"""
        for i, points in enumerate(self.wave_history):
            alpha = int(255 * (i / len(self.wave_history)))
            s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            if len(points) > 1:
                pygame.draw.lines(s, (100, 200, 255, alpha), False, points, 2)
            self.screen.blit(s, (0, 0))
    
    def draw_stars(self):
        """Draw star field visualization (Style 3)"""
        for star in self.stars:
            # 更新星星位置
            star['pos'][0] = (star['pos'][0] + star['velocity'][0]) % self.width
            star['pos'][1] = (star['pos'][1] + star['velocity'][1]) % self.height
            
            # 更新脉动相位
            star['pulse_phase'] += star['pulse_speed']
            pulse = math.sin(star['pulse_phase']) * 0.3 + 1.0
            current_size = star['base_size'] * pulse
            
            # 创建发光效果
            for size_mult in [3.0, 2.5, 2.0, 1.5, 1.0]:  # 增加更多光晕层
                alpha = int(star['brightness'] * star['life'] * (0.2 if size_mult > 1 else 1.0))
                color = (*star['color'], alpha)
                
                # 绘制主星体
                s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                size = int(current_size * size_mult)
                pygame.draw.circle(s, color,
                                (int(star['pos'][0]), int(star['pos'][1])),
                                size)
                
                # 在最外层添加十字光芒
                if size_mult == 3.0:
                    ray_length = current_size * 3
                    ray_width = max(1, current_size / 3)
                    ray_color = (*star['color'][:3], alpha // 2)  # 只使用RGB值，忽略Alpha
                    
                    # 绘制四个方向的光芒
                    for angle in [0, 45, 90, 135]:
                        rad = math.radians(angle)
                        dx = math.cos(rad) * ray_length
                        dy = math.sin(rad) * ray_length
                        pygame.draw.line(s,
                                     ray_color,
                                     (int(star['pos'][0] - dx), int(star['pos'][1] - dy)),
                                     (int(star['pos'][0] + dx), int(star['pos'][1] + dy)),
                                     int(ray_width))
                
                self.screen.blit(s, (0, 0))
    
    def draw_shapes(self):
        """Draw geometric shapes visualization (Style 4)"""
        for shape in self.shapes:
            points = []
            sides = {'triangle': 3, 'square': 4, 'pentagon': 5}[shape['type']]
            for i in range(sides):
                angle = math.radians(shape['rotation'] + (360 / sides) * i)
                x = shape['pos'][0] + math.cos(angle) * shape['size']
                y = shape['pos'][1] + math.sin(angle) * shape['size']
                points.append((int(x), int(y)))  # Convert to integers
            s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.polygon(s, (*shape['color'], int(255 * shape['life'])), points)
            self.screen.blit(s, (0, 0))
    
    def draw_ripples(self):
        """Draw fluid ripples visualization (Style 5)"""
        for ripple in self.ripples:
            color = (*ripple['color'], int(255 * ripple['life']))
            s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(s, color,
                            (int(ripple['pos'][0]), int(ripple['pos'][1])),
                            int(ripple['radius']),
                            ripple['width'])
            self.screen.blit(s, (0, 0))
    
    def draw_style_buttons(self, mouse_pos):
        """Draw the style selection buttons"""
        if not self.recording:
            return
            
        for button in self.style_buttons:
            # Determine color based on hover and selection state
            color = button['color']
            if button['rect'].collidepoint(mouse_pos):
                color = button['hover_color']
            if button['style_num'] == self.current_style:
                # Draw selection indicator
                pygame.draw.rect(self.screen, (255, 255, 255),
                               button['rect'].inflate(4, 4), 2, border_radius=5)
            
            # Draw button
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
            
            # Draw text
            font = pygame.font.Font(None, 24)
            text = font.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
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
            self.draw_start_button(mouse_pos)
        elif not self.recording and self.countdown > 0:
            self.draw_countdown()
        else:
            if self.current_style == 1:  # Pulse Particles
                for particle in self.particles:
                    s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    pygame.draw.circle(s, (*particle['color'], particle['alpha']),
                                    (int(particle['pos'][0]), int(particle['pos'][1])),
                                    int(particle['radius']), 2)
                    self.screen.blit(s, (0,0))
            elif self.current_style == 2:  # Wave Lines
                self.draw_wave_lines()
            elif self.current_style == 3:  # Star Field
                self.draw_stars()
            elif self.current_style == 4:  # Geometric Shapes
                self.draw_shapes()
            elif self.current_style == 5:  # Fluid Ripples
                self.draw_ripples()
            
            self.draw_style_buttons(mouse_pos)
        
        pygame.display.flip()
    
    def run(self):
        """Main loop"""
        try:
            with sd.InputStream(callback=self.audio_callback,
                              channels=self.channels,
                              samplerate=self.sample_rate,
                              blocksize=self.block_size):
                print("等待用户点击开始按钮...")
                print("提示：可以点击底部按钮或按1-5键切换不同的视觉效果")
                
                start_time = None
                running = True
                clock = pygame.time.Clock()
                
                while running:
                    current_time = time.time()
                    mouse_pos = pygame.mouse.get_pos()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if not self.started and self.is_mouse_over_start_button(event.pos):
                                self.started = True
                                start_time = current_time
                                print("准备开始录音...")
                                print("3秒倒计时后开始...")
                            elif self.recording:  # Only handle style buttons when recording
                                style_button = self.get_style_button_at_pos(event.pos)
                                if style_button:
                                    self.current_style = style_button['style_num']
                                    print(f"切换到样式 {self.current_style}: {self.style_names[self.current_style]}")
                        elif event.type == pygame.KEYDOWN:
                            # Handle number keys 1-5 for style switching
                            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                                new_style = int(event.unicode)
                                if 1 <= new_style <= 5:
                                    self.current_style = new_style
                                    print(f"切换到样式 {new_style}: {self.style_names[new_style]}")
                    
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