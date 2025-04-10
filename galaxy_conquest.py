import pygame
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum, auto
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WORLD_WIDTH = 4096
WORLD_HEIGHT = 3072
FPS = 60
CAMERA_SPEED = 10
PLANET_RADIUS = 40  # Restored to original size
ZOOMED_PLANET_RADIUS = 300
ZOOMED_STATION_SIZE = 60
STAR_COUNT = 1000
COMMAND_BAR_HEIGHT = 150
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 30
ICON_SIZE = 40
SPACE_STATION_COST = 500
FIGHTER_COST = 100
LORE_BUTTON_WIDTH = 100
LORE_BUTTON_HEIGHT = 30
LORE_SCREEN_PADDING = 50
ZOOM_SPEED = 0.2
MAX_ZOOM = 1.0
MIN_ZOOM = 0.0
FLEET_SPEED = 100
FLEET_RADIUS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
PURPLE = (100, 0, 150)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_BLUE = (100, 200, 255)
PLAYER_GREEN = (40, 200, 40)  # Softer green for player ownership

# Planet appearance data - Colors based on Star Wars planet characteristics
PLANET_APPEARANCES = {
    "Coruscant": {
        "colors": [(100, 100, 120), (255, 240, 150), (60, 60, 80)],  # Darker base, bright lights, shadows
        "pattern": "grid"  # City grid pattern
    },
    "Bastion": {
        "colors": [(100, 90, 90), (80, 70, 70), (60, 50, 50)],  # Dark industrial
        "pattern": "fortress"
    },
    "Corellia": {
        "colors": [(60, 100, 160), (50, 120, 50), (180, 180, 160)],  # Blue oceans, green land
        "pattern": "continents"
    },
    "Alderaan": {
        "colors": [(100, 150, 255), (50, 120, 50), (200, 200, 200)],  # Blue waters, green mountains
        "pattern": "mountains"
    },
    "Kuat": {
        "colors": [(70, 70, 90), (90, 90, 110), (110, 110, 130)],  # Industrial shipyards
        "pattern": "rings"
    },
    "Naboo": {
        "colors": [(60, 180, 60), (40, 120, 200), (200, 200, 150)],  # Green plains, blue waters
        "pattern": "swirls"
    },
    "Kashyyyk": {
        "colors": [(0, 100, 0), (20, 80, 0), (40, 120, 20)],  # Dense forests
        "pattern": "forest"
    },
    "Mon Calamari": {
        "colors": [(0, 100, 200), (0, 80, 180), (0, 60, 160)],  # Ocean world
        "pattern": "waves"
    },
    "Mandalore": {
        "colors": [(180, 180, 160), (160, 160, 140), (140, 140, 120)],  # Desert/rocky
        "pattern": "cracked"
    },
    "Bothawui": {
        "colors": [(140, 120, 100), (120, 100, 80), (100, 80, 60)],  # Urban/industrial
        "pattern": "urban"
    },
    "Fondor": {
        "colors": [(80, 80, 100), (60, 60, 80), (40, 40, 60)],  # Industrial
        "pattern": "industrial"
    },
    "Bilbringi": {
        "colors": [(100, 100, 120), (80, 80, 100), (60, 60, 80)],  # Shipyards
        "pattern": "docks"
    },
    "Ord Mantell": {
        "colors": [(180, 140, 100), (160, 120, 80), (140, 100, 60)],  # Rocky/junkyard
        "pattern": "scattered"
    },
    "Bestine": {
        "colors": [(160, 140, 120), (140, 120, 100), (120, 100, 80)],  # Mining world
        "pattern": "mining"
    },
    "Anaxes": {
        "colors": [(100, 120, 140), (80, 100, 120), (60, 80, 100)],  # Fortress world
        "pattern": "fortress"
    },
    "Rhinnal": {
        "colors": [(180, 180, 200), (160, 160, 180), (140, 140, 160)],  # Medical world
        "pattern": "medical"
    },
    "Hoth": {
        "colors": [(220, 220, 255), (200, 200, 235), (180, 180, 215)],  # Ice world
        "pattern": "ice"
    },
    "Tatooine": {
        "colors": [(245, 215, 145), (230, 190, 120), (200, 160, 100)],  # Lighter sand colors
        "pattern": "desert"
    },
    "Endor": {
        "colors": [(40, 120, 40), (30, 100, 30), (20, 80, 20)],  # Forest moon
        "pattern": "forest"
    },
    "Mustafar": {
        "colors": [(200, 60, 0), (180, 40, 0), (160, 20, 0)],  # Lava world
        "pattern": "lava"
    }
}

# Planet lore data
PLANET_LORE = {
    "Coruscant": [
        "The capital of the Galactic Republic and later the Empire",
        "A city-covered planet and the heart of galactic civilization",
        "Home to the Jedi Temple and Senate building",
        "Population of over 1 trillion beings",
        "Officially designated Imperial Center during Imperial rule"
    ],
    "Bastion": [
        "Fortress world of the Imperial Remnant",
        "Heavily fortified with multiple Star Destroyer shipyards",
        "Served as the capital of the Imperial Remnant",
        "Known for its military academies and training facilities",
        "Protected by a network of defensive platforms"
    ],
    "Corellia": [
        "Famous for its shipyards and skilled pilots",
        "Birthplace of Han Solo and many other famous smugglers",
        "Known for producing YT-series freighters",
        "Home to the prestigious Corellian Engineering Corporation",
        "Strong tradition of independence and self-reliance"
    ],
    "Alderaan": [
        "Peaceful world known for art, culture, and education",
        "Home planet of Princess Leia Organa",
        "Destroyed by the first Death Star",
        "Known for its pristine environment and architecture",
        "Center of galactic politics and diplomacy"
    ],
    "Kuat": [
        "Home to Kuat Drive Yards, builder of Star Destroyers",
        "Massive orbital ring houses shipbuilding facilities",
        "Primary supplier of Imperial warships",
        "Heavily defended strategic military asset",
        "Ancient noble houses control the economy"
    ],
    "Naboo": [
        "Peaceful world known for its art and culture",
        "Home planet of Padmé Amidala and Emperor Palpatine",
        "Features vast plains, swamps, and beautiful cities",
        "Known for its plasma energy exports",
        "Capital city of Theed is renowned for its architecture"
    ],
    "Kashyyyk": [
        "Homeworld of the Wookiees",
        "Covered in massive wroshyr trees",
        "Site of a major battle during the Clone Wars",
        "Known for its dangerous wildlife and ecosystem",
        "Features advanced technology integrated with nature"
    ],
    "Mon Calamari": [
        "Ocean world home to Mon Calamari and Quarren",
        "Famous for building Alliance cruisers",
        "Underwater cities feature unique architecture",
        "Resisted Imperial occupation successfully",
        "Major supplier of capital ships to the Rebellion"
    ],
    "Mandalore": [
        "Home of the legendary Mandalorian warriors",
        "Capital city of Sundari built in massive biodomes",
        "Rich in beskar iron deposits",
        "Site of multiple civil wars and conflicts",
        "Known for its warrior culture and ancient traditions"
    ],
    "Bothawui": [
        "Homeworld of the Bothan species",
        "Center of the Bothan Spynet",
        "Key intelligence provider to the Rebellion",
        "Advanced technology and information economy",
        "Neutral stance in most galactic conflicts"
    ],
    "Fondor": [
        "Major shipbuilding world",
        "Rival to Kuat Drive Yards",
        "Specialized in custom starship designs",
        "Protected by powerful planetary shields",
        "Strategic Imperial manufacturing center"
    ],
    "Bilbringi": [
        "Key shipyard system and trade hub",
        "Site of major battle against Grand Admiral Thrawn",
        "Protected by extensive defense grid",
        "Specialized in starship maintenance and repair",
        "Important New Republic military facility"
    ],
    "Ord Mantell": [
        "Former military outpost turned criminal haven",
        "Major black market trading center",
        "Base for many bounty hunter operations",
        "Mix of urban areas and dangerous wilderness",
        "Frequent site of conflict between rival gangs"
    ],
    "Bestine": [
        "Early Imperial colonial world",
        "Rich in mineral resources",
        "Strategic location in trade routes",
        "Moderate climate and Earth-like conditions",
        "Growing industrial and manufacturing base"
    ],
    "Anaxes": [
        "Known as the Defender of the Core",
        "Home to the Republic/Imperial military academy",
        "Ancient fortress world with strategic value",
        "Protected by extensive planetary defenses",
        "Training ground for naval officers"
    ],
    "Rhinnal": [
        "Famous for medical facilities and research",
        "Home to prestigious medical academies",
        "Center for advanced biological research",
        "Neutral stance in most conflicts",
        "Provider of medical aid throughout the sector"
    ],
    "Hoth": [
        "Ice planet and site of Echo Base",
        "Famous Rebel Alliance hideout",
        "Extremely cold climate year-round",
        "Home to wampas and tauntauns",
        "Site of major Imperial victory"
    ],
    "Tatooine": [
        "Desert world with twin suns",
        "Home planet of Anakin and Luke Skywalker",
        "Controlled by the Hutt crime syndicate",
        "Famous for podracing and moisture farming",
        "Haven for smugglers and outlaws"
    ],
    "Endor": [
        "Forest moon home to Ewoks",
        "Site of second Death Star's destruction",
        "Dense forests and rich biodiversity",
        "Sacred home to primitive tribal societies",
        "Location of critical Imperial shield bunker"
    ],
    "Mustafar": [
        "Volcanic mining world",
        "Site of Obi-Wan and Anakin's legendary duel",
        "Rich in unique mineral resources",
        "Home to advanced Techno Union facilities",
        "Later became Darth Vader's personal fortress"
    ]
}

# Planet Data - Fixed positions for 20 planets with Star Wars names
PLANET_DATA = [
    # Core worlds (Player start) - Highest resource generation
    ("Coruscant", (800, 1536), "player", 50),    # Player's capital - major industrial center
    ("Bastion", (3296, 1536), "ai", 50),         # AI's capital - major industrial center
    
    # Inner Ring - High resource generation
    ("Corellia", (1248, 800), "neutral", 30),    # Major shipyard world
    ("Alderaan", (2048, 600), "neutral", 35),    # Wealthy core world
    ("Kuat", (2848, 800), "neutral", 40),        # Major shipyard world
    ("Naboo", (1248, 2272), "neutral", 25),      # Rich in plasma energy
    ("Kashyyyk", (2048, 2472), "neutral", 30),   # Rich in natural resources
    ("Mon Calamari", (2848, 2272), "neutral", 35), # Major shipyard world
    
    # Middle Ring - Medium resource generation
    ("Mandalore", (1000, 1200), "neutral", 20),  # Mining world
    ("Bothawui", (1600, 1000), "neutral", 15),   # Trade hub
    ("Fondor", (2496, 1000), "neutral", 25),     # Industrial world
    ("Bilbringi", (3096, 1200), "neutral", 20),  # Shipyard world
    ("Ord Mantell", (1000, 1872), "neutral", 15), # Trade hub
    ("Bestine", (1600, 2072), "neutral", 20),    # Mining colony
    ("Anaxes", (2496, 2072), "neutral", 25),     # Fortress world
    ("Rhinnal", (3096, 1872), "neutral", 15),    # Medical world
    
    # Outer Systems - Lower resource generation
    ("Hoth", (2048, 200), "neutral", 10),        # Ice world
    ("Tatooine", (400, 1536), "neutral", 5),     # Desert world
    ("Endor", (3696, 1536), "neutral", 10),      # Forest moon
    ("Mustafar", (2048, 2872), "neutral", 15),   # Mining world
]

class GameMode(Enum):
    GALACTIC_OVERVIEW = auto()
    PLANET_VIEW = auto()
    PLANET_LORE = auto()

@dataclass
class Star:
    x: float
    y: float
    brightness: int
    size: float

@dataclass
class Fleet:
    owner: str
    size: int
    position: tuple[int, int]
    destination: tuple[int, int] = None
    fighters: int = 0  # Number of fighters in the fleet

    def move(self, dt):
        if self.destination:
            dx = self.destination[0] - self.position[0]
            dy = self.destination[1] - self.position[1]
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < FLEET_SPEED * dt:
                self.position = self.destination
                self.destination = None
            else:
                move_x = (dx / distance) * FLEET_SPEED * dt
                move_y = (dy / distance) * FLEET_SPEED * dt
                self.position = (self.position[0] + move_x, self.position[1] + move_y)

    def draw(self, screen, camera_pos, zoom):
        # Calculate screen position
        screen_x = (self.position[0] - camera_pos[0]) * zoom + SCREEN_WIDTH // 2
        screen_y = (self.position[1] - camera_pos[1]) * zoom + SCREEN_HEIGHT // 2
        
        # Draw fleet circle
        color = PLAYER_GREEN if self.owner == "player" else RED
        pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), int(FLEET_RADIUS * zoom))
        
        # Draw fighter count if there are fighters
        if self.fighters > 0:
            fighter_text = pygame.font.SysFont(None, 20).render(str(self.fighters), True, WHITE)
            text_x = screen_x - fighter_text.get_width() // 2
            text_y = screen_y - fighter_text.get_height() // 2
            screen.blit(fighter_text, (text_x, text_y))

@dataclass
class Planet:
    name: str
    position: tuple[int, int]
    owner: str  # "player" or "ai"
    resources: int
    fleet_size: int
    resource_rate: int  # Resources generated per day
    has_space_station: bool = False
    building_station: bool = False
    station_build_start: float = 0
    station_level: int = 0  # Current station level (0-5)
    fleet: Fleet = None  # Reference to the planet's fleet
    building_fighter: bool = False
    fighter_build_start: float = 0
    
    def update_station_construction(self, current_time):
        """Update space station construction progress"""
        if self.building_station:
            time_elapsed = current_time - self.station_build_start
            if time_elapsed >= 20:  # 20 seconds build time
                self.building_station = False
                self.has_space_station = True
                self.station_level += 1  # Increment station level
    
    def update_fighter_construction(self, current_time):
        """Update fighter construction progress"""
        if self.building_fighter:
            time_elapsed = current_time - self.fighter_build_start
            if time_elapsed >= 10:  # 10 seconds build time
                self.building_fighter = False
                if not self.fleet:
                    # Create new fleet only when ship is complete
                    self.fleet = Fleet(owner=self.owner, size=0, position=self.position, fighters=1)
                else:
                    self.fleet.fighters += 1
    
    def add_fighter(self, current_time):
        """Start fighter construction"""
        self.building_fighter = True
        self.fighter_build_start = current_time

    def draw(self, screen, pos):
        """Draw the planet with its unique appearance and ownership ring"""
        appearance = PLANET_APPEARANCES[self.name]
        colors = appearance["colors"]
        pattern = appearance["pattern"]
        
        # Draw base planet
        pygame.draw.circle(screen, colors[0], pos, PLANET_RADIUS)
        
        # Draw pattern based on planet type
        if pattern == "grid":  # Coruscant-style city grid
            # Draw darker base with lights
            for y in range(-PLANET_RADIUS, PLANET_RADIUS + 1, 4):
                for x in range(-PLANET_RADIUS, PLANET_RADIUS + 1, 4):
                    # Check if point is within planet circle
                    if x*x + y*y <= PLANET_RADIUS * PLANET_RADIUS:
                        point_x = pos[0] + x
                        point_y = pos[1] + y
                        # Randomly place lights
                        if random.random() < 0.3:  # 30% chance of a light
                            pygame.draw.circle(screen, colors[1], (point_x, point_y), 1)
            
            # Draw main sectors - divide into 6 sections
            for i in range(6):
                angle = i * math.pi / 3
                end_x = pos[0] + math.cos(angle) * PLANET_RADIUS
                end_y = pos[1] + math.sin(angle) * PLANET_RADIUS
                pygame.draw.line(screen, colors[2], pos, (end_x, end_y), 2)
        
        elif pattern == "desert":  # Tatooine-style sand dunes
            # Draw three layers of dunes
            for i in range(3):
                y_offset = -PLANET_RADIUS//2 + i * PLANET_RADIUS//3
                rect = pygame.Rect(
                    pos[0] - PLANET_RADIUS, 
                    pos[1] + y_offset,
                    PLANET_RADIUS * 2,
                    PLANET_RADIUS//2
                )
                pygame.draw.arc(screen, colors[1], rect, 0, math.pi, 3)
            
            # Draw two simple circles for the binary suns
            sun_color = (255, 220, 120)  # Bright yellow-orange
            pygame.draw.circle(screen, sun_color, 
                            (pos[0] - PLANET_RADIUS//3, pos[1] - PLANET_RADIUS//3), 4)
            pygame.draw.circle(screen, sun_color, 
                            (pos[0] - PLANET_RADIUS//4, pos[1] - PLANET_RADIUS//3), 3)

        elif pattern == "lava": # Mustafar-style lava flows
            for i in range(4):
                angle = i * math.pi/2
                pygame.draw.arc(screen, colors[1],
                              (pos[0] - PLANET_RADIUS/2, pos[1] - PLANET_RADIUS/2,
                               PLANET_RADIUS, PLANET_RADIUS),
                               angle, angle + math.pi/4, 3)
        
        elif pattern == "ice":  # Hoth-style ice caps
            pygame.draw.circle(screen, colors[1], 
                             (pos[0], pos[1] - PLANET_RADIUS/2), PLANET_RADIUS/3)
            pygame.draw.circle(screen, colors[1],
                             (pos[0], pos[1] + PLANET_RADIUS/2), PLANET_RADIUS/3)
        
        elif pattern == "forest":  # Endor/Kashyyyk-style forests
            for i in range(8):
                angle = i * math.pi/4
                x = pos[0] + math.cos(angle) * PLANET_RADIUS * 0.7
                y = pos[1] + math.sin(angle) * PLANET_RADIUS * 0.7
                pygame.draw.circle(screen, colors[1], (int(x), int(y)), PLANET_RADIUS//4)
        
        elif pattern == "waves":  # Mon Calamari-style oceans
            for i in range(3):
                offset = i * 6 - 6
                pygame.draw.arc(screen, colors[1],
                              (pos[0] - PLANET_RADIUS, pos[1] - PLANET_RADIUS/2 + offset,
                               PLANET_RADIUS * 2, PLANET_RADIUS),
                               0, math.pi, 2)
        
        # Draw ownership ring if planet is owned
        if self.owner != "neutral":
            ring_color = PLAYER_GREEN if self.owner == "player" else RED
            pygame.draw.circle(screen, ring_color, pos, PLANET_RADIUS + 4, 2)
            
        # Draw space station if present
        if self.has_space_station:
            station_radius = PLANET_RADIUS + 8
            pygame.draw.circle(screen, WHITE, pos, station_radius, 1)
        
        # Draw fleet above planet if it exists and has ships
        if self.fleet and self.fleet.fighters > 0:
            fleet_y_offset = -PLANET_RADIUS - 20  # Position above planet
            fleet_pos = (pos[0], pos[1] + fleet_y_offset)
            
            # Draw fleet circle
            fleet_color = PLAYER_GREEN if self.owner == "player" else RED
            fleet_radius = 12
            pygame.draw.circle(screen, fleet_color, fleet_pos, fleet_radius, 2)
            
            # Draw ship count
            count_text = str(self.fleet.fighters)
            text_surface = pygame.font.SysFont(None, 20).render(count_text, True, WHITE)
            text_rect = text_surface.get_rect(center=fleet_pos)
            screen.blit(text_surface, text_rect)

class Camera:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.speed = CAMERA_SPEED

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WORLD_WIDTH - SCREEN_WIDTH:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < WORLD_HEIGHT - SCREEN_HEIGHT:
            self.y += self.speed

    def world_to_screen(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        return (pos[0] - self.x, pos[1] - self.y)

    def screen_to_world(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Convert screen coordinates to world coordinates"""
        return (pos[0] + self.x, pos[1] + self.y)

class GalaxyConquest:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Galaxy Conquest")
        self.clock = pygame.time.Clock()
        self.current_mode = GameMode.GALACTIC_OVERVIEW
        
        # Initialize camera at the center of the player's capital
        start_x = PLANET_DATA[0][1][0] - SCREEN_WIDTH // 2
        start_y = PLANET_DATA[0][1][1] - SCREEN_HEIGHT // 2
        self.camera = Camera(start_x, start_y)
        
        # Game state
        self.planets: Dict[str, Planet] = {}
        self.fleets: List[Fleet] = []
        self.player_resources = 100_000
        self.ai_resources = 100_000
        self.selected_planet = None
        self.current_zoom = 0.0  # 0.0 = galaxy view, 1.0 = planet view
        self.target_zoom = 0.0   # For smooth zoom transitions
        self.current_day = 1
        self.day_timer = 0
        self.seconds_per_day = 30
        self.mouse_pos = (0, 0)  # Track mouse position
        self.hovering_station_icon = False
        self.hovering_fighter_icon = False
        self.last_time = time.time()
        self.current_time = time.time()
        
        # Fleet movement
        self.dragging_fleet = None
        self.dragging_from_planet = None
        self.fleet_drag_start = None
        
        # Initialize fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Initialize background stars
        self.stars = self.generate_stars()
        
        self.initialize_game()
        
    def generate_stars(self) -> List[Star]:
        stars = []
        for _ in range(STAR_COUNT):
            x = random.uniform(0, WORLD_WIDTH)
            y = random.uniform(0, WORLD_HEIGHT)
            brightness = random.randint(50, 255)
            size = random.uniform(0.5, 2)
            stars.append(Star(x, y, brightness, size))
        return stars

    def initialize_game(self):
        """Initialize the game state with planets"""
        # Create planets from the planet data
        for name, position, owner, resource_rate in PLANET_DATA:
            # Set initial resources based on owner
            self.planets[name] = Planet(
                name=name,
                position=position,
                owner=owner,
                resources=0,  # Planets don't store resources
                fleet_size=0,
                resource_rate=resource_rate  # Each planet gives 500 per day
            )

    def calculate_daily_resource_income(self):
        """Calculate total daily resource income from all owned planets"""
        total_income = 0
        for planet in self.planets.values():
            if planet.owner == "player":
                total_income += planet.resource_rate
        return total_income

    def calculate_ai_daily_income(self):
        """Calculate total daily resource income for AI from all owned planets"""
        total_income = 0
        for planet in self.planets.values():
            if planet.owner == "ai":
                total_income += planet.resource_rate
        return total_income

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    self.handle_mouse_release(event.pos)
                    
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                
        return True
        
    def handle_mouse_click(self, pos):
        """Handle mouse clicks in the game"""
        if self.current_mode == GameMode.GALACTIC_OVERVIEW:
            # Check for clicks on planets
            for planet_name, planet in self.planets.items():
                screen_pos = self.camera.world_to_screen(planet.position)
                distance = math.sqrt((pos[0] - screen_pos[0])**2 + 
                                  (pos[1] - screen_pos[1])**2)
                
                # Check if clicking on fleet
                if planet.fleet and planet.fleet.fighters > 0:
                    fleet_pos = (screen_pos[0], screen_pos[1] - PLANET_RADIUS - 20)
                    fleet_distance = math.sqrt((pos[0] - fleet_pos[0])**2 + 
                                            (pos[1] - fleet_pos[1])**2)
                    if fleet_distance <= 12:  # Fleet circle radius
                        self.dragging_fleet = planet.fleet
                        self.dragging_from_planet = planet
                        self.fleet_drag_start = pos
                        return True
                
                if distance <= PLANET_RADIUS:
                    if self.current_mode == GameMode.GALACTIC_OVERVIEW:
                        self.selected_planet = planet_name
                        self.target_zoom = 1.0
                        return True
                        
        return False
        
    def handle_mouse_release(self, pos):
        """Handle mouse button release"""
        if self.dragging_fleet:
            # Check if released over a planet
            for planet_name, planet in self.planets.items():
                screen_pos = self.camera.world_to_screen(planet.position)
                distance = math.sqrt((pos[0] - screen_pos[0])**2 + 
                                  (pos[1] - screen_pos[1])**2)
                
                if distance <= PLANET_RADIUS:
                    # Move fleet to this planet
                    if planet != self.dragging_from_planet:
                        # If target is neutral, conquer it
                        if planet.owner == "neutral":
                            planet.owner = self.dragging_fleet.owner
                        
                        # Transfer fleet to new planet
                        self.dragging_from_planet.fleet = None
                        planet.fleet = self.dragging_fleet
                        planet.fleet.position = planet.position
                    break
            
            self.dragging_fleet = None
            self.dragging_from_planet = None
            self.fleet_drag_start = None
            return True
            
        return False
        
    def update(self, dt):
        self.current_time += dt
        self.day_timer += dt
        
        # Update planets
        for planet in self.planets.values():
            # Update space station construction
            planet.update_station_construction(self.current_time)
            
            # Update fighter construction
            planet.update_fighter_construction(self.current_time)
        
        # Update zoom level with smooth transition
        if abs(self.current_zoom - self.target_zoom) > 0.01:
            self.current_zoom += (self.target_zoom - self.current_zoom) * 0.1
            if self.current_zoom > 0.5:
                self.current_mode = GameMode.PLANET_VIEW
            else:
                self.current_mode = GameMode.GALACTIC_OVERVIEW

        # Update camera position based on keyboard input
        if self.current_mode == GameMode.GALACTIC_OVERVIEW:
            keys = pygame.key.get_pressed()
            self.camera.move(keys)
        
        # Update day timer
        if self.day_timer >= self.seconds_per_day:
            self.day_timer = 0
            self.current_day += 1
            
            # Add resources once per day
            for planet in self.planets.values():
                if planet.owner == "player":
                    self.player_resources += planet.resource_rate
                elif planet.owner == "ai":
                    self.ai_resources += planet.resource_rate

    def draw(self):
        """Draw the game state"""
        self.screen.fill(BLACK)
        
        # Draw stars in the background
        for star in self.stars:
            color = (star.brightness,) * 3
            pygame.draw.circle(self.screen, color, 
                             (int(star.x), int(star.y)), 
                             int(star.size))
        
        if self.current_mode == GameMode.GALACTIC_OVERVIEW:
            # Draw planets
            self.draw_planets()
            
            # Draw dragging fleet if any
            if self.dragging_fleet:
                # Draw line from start to current mouse position
                start_pos = self.camera.world_to_screen(self.dragging_from_planet.position)
                start_pos = (start_pos[0], start_pos[1] - PLANET_RADIUS - 20)
                fleet_color = PLAYER_GREEN if self.dragging_fleet.owner == "player" else RED
                pygame.draw.line(self.screen, fleet_color, start_pos, self.mouse_pos, 2)
                
                # Draw fleet circle at mouse position
                pygame.draw.circle(self.screen, fleet_color, self.mouse_pos, 12, 2)
                
                # Draw ship count
                count_text = str(self.dragging_fleet.fighters)
                text_surface = pygame.font.SysFont(None, 20).render(count_text, True, WHITE)
                text_rect = text_surface.get_rect(center=self.mouse_pos)
                self.screen.blit(text_surface, text_rect)
                
        elif self.current_mode == GameMode.PLANET_VIEW and self.selected_planet:
            # Draw zoomed planet view
            planet = self.planets[self.selected_planet]
            appearance = PLANET_APPEARANCES[planet.name]
            colors = appearance["colors"]
            pattern = appearance["pattern"]
            
            # Calculate zoomed planet size based on current zoom level
            zoom_radius = int(PLANET_RADIUS + (ZOOMED_PLANET_RADIUS - PLANET_RADIUS) * self.current_zoom)
            
            # Draw the planet at the center-bottom of the screen
            planet_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - zoom_radius // 2)
            
            # Draw the semicircle planet surface
            pygame.draw.circle(self.screen, colors[0], planet_pos, zoom_radius)
            
            # Draw planet pattern scaled up
            if pattern == "grid":
                # Draw grid pattern scaled with zoom
                grid_spacing = int(4 * (1 + self.current_zoom * 2))
                for y in range(-zoom_radius, zoom_radius + 1, grid_spacing):
                    for x in range(-zoom_radius, zoom_radius + 1, grid_spacing):
                        if x*x + y*y <= zoom_radius * zoom_radius:
                            point_x = planet_pos[0] + x
                            point_y = planet_pos[1] + y
                            if point_y > SCREEN_HEIGHT - zoom_radius:  # Only draw on visible part
                                if random.random() < 0.3:
                                    pygame.draw.circle(self.screen, colors[1], (point_x, point_y), 1 + self.current_zoom)
            
            # Draw the horizon line
            pygame.draw.line(self.screen, colors[0], 
                           (0, SCREEN_HEIGHT - zoom_radius), 
                           (SCREEN_WIDTH, SCREEN_HEIGHT - zoom_radius), 2)
            
            # Draw ownership ring
            ring_color = PLAYER_GREEN if planet.owner == "player" else RED if planet.owner == "ai" else GRAY
            pygame.draw.circle(self.screen, ring_color, planet_pos, zoom_radius + 5, 3)

            # Draw fleet if it exists
            if planet.fleet and planet.fleet.fighters > 0:
                # Position ships to the right of the planet
                ship_x = SCREEN_WIDTH // 2 + zoom_radius + 50  # Right of planet
                ship_y = SCREEN_HEIGHT - zoom_radius * 2  # Same height as station
                
                # Draw detailed fighter icon
                ship_color = PLAYER_GREEN if planet.owner == "player" else RED
                ship_size = 40  # Larger size for zoom view
                
                # Draw fighter shape
                points = [
                    (ship_x, ship_y - ship_size//2),  # Nose
                    (ship_x - ship_size//2, ship_y + ship_size//3),  # Left wing
                    (ship_x - ship_size//4, ship_y),  # Left body
                    (ship_x + ship_size//4, ship_y),  # Right body
                    (ship_x + ship_size//2, ship_y + ship_size//3),  # Right wing
                ]
                pygame.draw.polygon(self.screen, ship_color, points, 0)
                
                # Draw cockpit
                cockpit_pos = (ship_x, ship_y - ship_size//6)
                pygame.draw.circle(self.screen, LIGHT_BLUE, cockpit_pos, ship_size//8)
                
                # Draw engine glow
                engine_pos = (ship_x, ship_y + ship_size//3)
                engine_color = (100, 150, 255) if planet.owner == "player" else (255, 100, 100)
                pygame.draw.circle(self.screen, engine_color, engine_pos, ship_size//6)
                
                # Draw ship count with larger font and background
                count_text = str(planet.fleet.fighters)
                count_font = pygame.font.SysFont(None, 48)
                text_surface = count_font.render(count_text, True, WHITE)
                text_rect = text_surface.get_rect(midleft=(ship_x + ship_size//2 + 20, ship_y))
                
                # Draw background circle for count
                padding = 10
                circle_pos = (text_rect.centerx, text_rect.centery)
                circle_radius = max(text_rect.width, text_rect.height)//2 + padding
                pygame.draw.circle(self.screen, DARK_GRAY, circle_pos, circle_radius)
                pygame.draw.circle(self.screen, ship_color, circle_pos, circle_radius, 2)
                
                # Draw count text
                self.screen.blit(text_surface, text_rect)

            # Draw space station if it exists
            if planet.has_space_station:
                # Position the station up and to the left of the planet
                station_x = SCREEN_WIDTH // 2 - zoom_radius - ZOOMED_STATION_SIZE  # Left of planet
                station_y = SCREEN_HEIGHT - zoom_radius * 2  # Above planet
                
                # Draw the station icon (same as build icon)
                station_color = PLAYER_GREEN if planet.owner == "player" else RED
                # Main circle
                pygame.draw.circle(self.screen, station_color, 
                                 (station_x, station_y), 
                                 ZOOMED_STATION_SIZE // 2)
                # Ring around the circle
                pygame.draw.circle(self.screen, WHITE, 
                                 (station_x, station_y), 
                                 ZOOMED_STATION_SIZE // 2 + 4, 2)

                # Draw pentagon base
                points = []
                radius = ZOOMED_STATION_SIZE // 2
                for i in range(5):
                    angle = math.pi * 2 * i / 5 - math.pi / 2  # Start from top point
                    x = station_x + radius * math.cos(angle)
                    y = station_y + radius * math.sin(angle)
                    points.append((x, y))
                
                # Draw base pentagon
                pygame.draw.polygon(self.screen, LIGHT_BLUE, points)
                pygame.draw.polygon(self.screen, WHITE, points, 2)
                
                # Draw arms for current level
                arm_length = radius * 0.6
                arm_width = 4
                for i in range(planet.station_level):
                    angle = math.pi * 2 * i / 5 - math.pi / 2
                    start_x = station_x + radius * math.cos(angle)
                    start_y = station_y + radius * math.sin(angle)
                    end_x = start_x + arm_length * math.cos(angle)
                    end_y = start_y + arm_length * math.sin(angle)
                    pygame.draw.line(self.screen, WHITE, (start_x, start_y), (end_x, end_y), arm_width)

        # Draw UI elements
        self.draw_command_bar()
        self.draw_status_bar()
        self.draw_minimap()
        
        pygame.display.flip()

    def draw_planets(self):
        """Draw all planets and fleets in galaxy view"""
        # Draw all planets
        for planet in self.planets.values():
            screen_pos = self.camera.world_to_screen(planet.position)
            if (0 <= screen_pos[0] <= SCREEN_WIDTH and 
                0 <= screen_pos[1] <= SCREEN_HEIGHT):
                planet.draw(self.screen, screen_pos)

        # Draw fleets
        for fleet in self.fleets:
            screen_pos = self.camera.world_to_screen(fleet.position)
            if (0 <= screen_pos[0] <= SCREEN_WIDTH and 
                0 <= screen_pos[1] <= SCREEN_HEIGHT):
                fleet.draw(self.screen, self.camera.position, self.current_zoom)

    def draw_command_bar(self):
        """Draw the command bar at the bottom of the screen"""
        if not self.selected_planet:
            return
            
        # Create a surface for the command bar with transparency
        command_bar_surface = pygame.Surface((SCREEN_WIDTH, COMMAND_BAR_HEIGHT), pygame.SRCALPHA)
        command_bar_surface.fill((30, 30, 30, 180))  # DARK_GRAY with alpha
        self.screen.blit(command_bar_surface, (0, SCREEN_HEIGHT - COMMAND_BAR_HEIGHT))
        
        # Draw horizontal separator line at top
        separator_surface = pygame.Surface((SCREEN_WIDTH, 2), pygame.SRCALPHA)
        separator_surface.fill((50, 50, 50, 180))  # GRAY with alpha
        self.screen.blit(separator_surface, (0, SCREEN_HEIGHT - COMMAND_BAR_HEIGHT))
        
        # Draw vertical separator lines to divide into thirds
        section_width = SCREEN_WIDTH // 3
        for x in [section_width, section_width * 2]:
            vertical_separator = pygame.Surface((2, COMMAND_BAR_HEIGHT), pygame.SRCALPHA)
            vertical_separator.fill((50, 50, 50, 180))  # Same color as horizontal separator
            self.screen.blit(vertical_separator, (x, SCREEN_HEIGHT - COMMAND_BAR_HEIGHT))
        
        # Draw section headings
        section2_text = self.font.render("Space Stations", True, WHITE)
        section3_text = self.font.render("Ships", True, WHITE)
        
        # Center the headings in their sections
        section2_x = section_width + (section_width - section2_text.get_width()) // 2
        section3_x = (section_width * 2) + (section_width - section3_text.get_width()) // 2
        heading_y = SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 10
        
        self.screen.blit(section2_text, (section2_x, heading_y))
        self.screen.blit(section3_text, (section3_x, heading_y))
        
        planet = self.planets[self.selected_planet]
        # Draw planet info in first section
        name_text = self.font.render(f"Planet: {planet.name}", True, WHITE)
        owner_text = self.font.render(f"Owner: {planet.owner.capitalize()}", True, WHITE)
        resources_text = self.font.render(f"Resources: {planet.resources}", True, WHITE)
        income_text = self.font.render(f"Daily Income: +{planet.resource_rate}", True, YELLOW)
        
        self.screen.blit(name_text, (20, SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 20))
        self.screen.blit(owner_text, (20, SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 50))
        self.screen.blit(resources_text, (20, SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 80))
        self.screen.blit(income_text, (20, SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 110))
        
        # Draw space station icon if player owned and not at max level
        if planet.owner == "player" and (not planet.has_space_station or planet.station_level < 5):
            self.draw_station_icon(planet)
            
        # Draw fighter production icon if player owned and has at least level 1 station
        if planet.owner == "player" and planet.has_space_station and planet.station_level >= 1:
            self.draw_fighter_icon(planet)
            
    def draw_fighter_icon(self, planet):
        """Draw the fighter production icon in the ships section"""
        section_width = SCREEN_WIDTH // 3
        icon_x = (section_width * 2) + 60
        icon_y = SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 50
        
        if planet.building_fighter:
            # Draw construction timer if fighter is being built
            time_left = 10 - (self.current_time - planet.fighter_build_start)
            timer_text = self.font.render(f"Building: {int(time_left)}s", True, WHITE)
            timer_x = (section_width * 2) + (section_width - timer_text.get_width()) // 2
            timer_y = SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 35
            self.screen.blit(timer_text, (timer_x, timer_y))
            return
        
        # Draw fighter icon (triangle)
        radius = ICON_SIZE // 2
        points = [
            (icon_x, icon_y - radius),  # Top point
            (icon_x - radius, icon_y + radius),  # Bottom left
            (icon_x - radius//2, icon_y),  # Bottom left
            (icon_x + radius//2, icon_y),  # Bottom right
            (icon_x + radius, icon_y + radius)   # Bottom right
        ]
        
        # Determine if player can afford fighter
        can_afford = self.player_resources >= FIGHTER_COST and not planet.building_fighter
        icon_color = LIGHT_BLUE if can_afford else GRAY
        
        pygame.draw.polygon(self.screen, icon_color, points)
        pygame.draw.polygon(self.screen, WHITE, points, 2)
        
        # Draw cost and text
        cost_text = self.small_font.render(f"{FIGHTER_COST}", True, WHITE)
        type_text = self.small_font.render("Fighter", True, WHITE)
        
        cost_x = icon_x - cost_text.get_width() - 10
        cost_y = icon_y - cost_text.get_height() // 2
        type_x = icon_x + radius + 10
        type_y = icon_y - type_text.get_height() // 2
        
        self.screen.blit(cost_text, (cost_x, cost_y))
        self.screen.blit(type_text, (type_x, type_y))
        
        # Draw hover text
        if self.hovering_fighter_icon:
            hover_text = f"Build Fighter ({FIGHTER_COST})"
            text_surface = self.small_font.render(hover_text, True, WHITE)
            text_x = self.mouse_pos[0] + 10
            text_y = self.mouse_pos[1] - 20
            self.screen.blit(text_surface, (text_x, text_y))
            
    def draw_station_icon(self, planet):
        """Draw the space station icon in the space stations section"""
        section_width = SCREEN_WIDTH // 3
        icon_x = section_width + 60
        icon_y = SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 50
        
        if planet.building_station:
            # Draw construction timer if station is being built
            time_left = 20 - (self.current_time - planet.station_build_start)
            timer_text = self.font.render(f"Building: {int(time_left)}s", True, WHITE)
            timer_x = section_width + (section_width - timer_text.get_width()) // 2
            timer_y = SCREEN_HEIGHT - COMMAND_BAR_HEIGHT + 35
            self.screen.blit(timer_text, (timer_x, timer_y))
            return
        
        # Draw pentagon base
        points = []
        radius = ICON_SIZE // 2
        for i in range(5):
            angle = math.pi * 2 * i / 5 - math.pi / 2  # Start from top point
            x = icon_x + radius * math.cos(angle)
            y = icon_y + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw base pentagon
        next_level = planet.station_level + 1
        cost = 500 * next_level  # Each level costs 500 more
        can_afford = self.player_resources >= cost
        icon_color = LIGHT_BLUE if can_afford else GRAY
        pygame.draw.polygon(self.screen, icon_color, points)
        pygame.draw.polygon(self.screen, WHITE, points, 2)
        
        # Draw arms for current level
        if planet.has_space_station:
            arm_length = radius * 0.6
            arm_width = 4
            for i in range(planet.station_level):
                angle = math.pi * 2 * i / 5 - math.pi / 2
                start_x = icon_x + radius * math.cos(angle)
                start_y = icon_y + radius * math.sin(angle)
                end_x = start_x + arm_length * math.cos(angle)
                end_y = start_y + arm_length * math.sin(angle)
                pygame.draw.line(self.screen, WHITE, (start_x, start_y), (end_x, end_y), arm_width)
        
        # Draw cost and level text
        cost_text = self.small_font.render(f"{cost}", True, WHITE)
        level_text = self.small_font.render(f"Lv{next_level}", True, WHITE)
        
        cost_x = icon_x - cost_text.get_width() - 10
        cost_y = icon_y - cost_text.get_height() // 2
        level_x = icon_x + radius + 10
        level_y = icon_y - level_text.get_height() // 2
        
        self.screen.blit(cost_text, (cost_x, cost_y))
        self.screen.blit(level_text, (level_x, level_y))
        
        # Draw hover text
        if self.hovering_station_icon:
            if planet.has_space_station:
                hover_text = f"Upgrade to Level {next_level} Space Station ({cost})"
            else:
                hover_text = f"Build Level 1 Space Station ({cost})"
            text_surface = self.small_font.render(hover_text, True, WHITE)
            text_x = self.mouse_pos[0] + 10
            text_y = self.mouse_pos[1] - 20
            self.screen.blit(text_surface, (text_x, text_y))

    def draw_status_bar(self):
        """Draw the status bar at the top of the screen"""
        # Draw day counter and countdown
        day_text = self.large_font.render(f"Day {self.current_day}", True, LIGHT_BLUE)
        seconds_left = max(0, self.seconds_per_day - self.day_timer)  # Use day_timer instead of get_ticks
        countdown_text = self.font.render(f"Next Day: {int(seconds_left)}s", True, YELLOW)
        
        self.screen.blit(day_text, (20, 20))
        self.screen.blit(countdown_text, 
                        (day_text.get_width() + 20, 
                         20 + 8))  # Align with day text
        
        # Draw player resources and income
        resources_text = self.font.render(f"Player Resources: {int(self.player_resources)}", True, BLUE)
        daily_income = self.calculate_daily_resource_income()
        income_text = self.font.render(f"Daily Income: +{daily_income}", True, YELLOW)
        
        self.screen.blit(resources_text, (20, 65))
        self.screen.blit(income_text, (20, 95))

        # Draw AI resources and income (temporarily)
        ai_resources_text = self.font.render(f"AI Resources: {int(self.ai_resources)}", True, RED)
        ai_income = self.calculate_ai_daily_income()
        ai_income_text = self.font.render(f"Daily Income: +{ai_income}", True, YELLOW)
        
        self.screen.blit(ai_resources_text, (20, 125))
        self.screen.blit(ai_income_text, (20, 155))

    def draw_minimap(self):
        """Draw a small minimap in the top-right corner"""
        minimap_rect = pygame.Rect(SCREEN_WIDTH - 200 - 20, 
                                 20,  
                                 200, 200)
        
        # Draw minimap background with slight transparency
        minimap_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        minimap_surface.fill((30, 30, 30, 180))  # DARK_GRAY with alpha
        self.screen.blit(minimap_surface, minimap_rect)
        
        # Draw planets on minimap
        for planet in self.planets.values():
            mini_x = minimap_rect.x + (planet.position[0] * 200 // WORLD_WIDTH)
            mini_y = minimap_rect.y + (planet.position[1] * 200 // WORLD_HEIGHT)
            color = BLUE if planet.owner == "player" else RED if planet.owner == "ai" else WHITE
            pygame.draw.circle(self.screen, color, (mini_x, mini_y), 2)
        
        # Draw current view rectangle on minimap
        viewport_x = minimap_rect.x + (self.camera.x * 200 // WORLD_WIDTH)
        viewport_y = minimap_rect.y + (self.camera.y * 200 // WORLD_HEIGHT)
        viewport_w = SCREEN_WIDTH * 200 // WORLD_WIDTH
        viewport_h = (SCREEN_HEIGHT - COMMAND_BAR_HEIGHT) * 200 // WORLD_HEIGHT
        pygame.draw.rect(self.screen, WHITE, (viewport_x, viewport_y, viewport_w, viewport_h), 1)

    def draw_battle(self):
        # TODO: Implement battle view
        pass

    def draw_text(self, surface, text, pos, color):
        text_surface = self.font.render(text, True, color)
        surface.blit(text_surface, pos)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update(1 / FPS)
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = GalaxyConquest()
    game.run()
    pygame.quit()
    sys.exit()