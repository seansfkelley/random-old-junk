from globals import g_game_clock

import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = pygame.Rect(0, 0, 1, 1)
    
    def change_image(self, image, num_frames, fps):
        self.image = image
        self.num_frames = num_frames
        self.ms_per_frame = 1000 / fps
        
        self.current_frame = 0
        self.ms_since_flip = 0
        
        self.draw_source_rect = image.get_rect()
        self.draw_source_rect.width = self.draw_source_rect.width / num_frames
        
        self.rect.width, self.rect.height = self.draw_source_rect.width, self.draw_source_rect.height
    
    def update(self):
        if self.num_frames == 1:
            return
        
        self.ms_since_flip += g_game_clock.get_time()
        while (self.ms_since_flip > self.ms_per_frame):
            self.ms_since_flip -= self.ms_per_frame
            self.current_frame = (self.current_frame + 1) % self.num_frames
        self.draw_source_rect.left = self.current_frame * self.draw_source_rect.width
    
    def draw(self, screen):
        screen.blit(self.image, self.rect, self.draw_source_rect)
    
