
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import random
import math

import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('data/background.png')
mixer.music.load('data/background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('data/ufo.png')
pygame.display.set_icon(icon)

scoreX = 10
scoreY = 10
levelX = 650
levelY = 10

# Score
score_value = 0
level_value = 1
font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

#Player
playerImg = pygame.image.load('data/player.png')
playerX = 370
playerY = 480
playerX_change =0


#Bullet
# Ready - Cannot see bullet but is ready in ship
# Fired - Bullet is currently moving
bulletImg = pygame.image.load('data/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"


#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15
current_enemies = num_of_enemies
enemy_speed = 1


x_value = 188
y_value = 64
for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('data/enemy.png'))
	enemyX.append(x_value)
	enemyY.append(y_value)
	if (i+1)% (num_of_enemies/3) == 0:
		y_value += 70
		x_value = 188
	else:
		x_value += 90
	enemyX_change.append(enemy_speed)
	enemyY_change.append(10)

def spawn_enemies():
	x_value = 188
	y_value = 64
	
	for i in range(num_of_enemies):

		#enemyImg[i] = pygame.image.load('data/enemy.png')

		enemyX[i] = (x_value)
		enemyY[i] = (y_value)
		if (i+1)% (num_of_enemies/3) == 0:
			y_value += 70
			x_value = 188
		else:
			x_value += 90
		enemyX_change[i] = (enemy_speed)
		enemyY_change[i] = (40)
def show_score(x, y):
	score = font.render("Score: " + str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))
def show_level(x, y):
	level = font.render("Level: " + str(level_value), True, (255, 255, 255))
	screen.blit(level, (x, y))
def next_level():
	next_level_text = game_over_font.render("Next Level: " + str(level_value), True, (255, 255, 255))
	screen.blit(next_level_text, (200, 250))
def game_over():
	game_over_text = game_over_font.render("GAME OVER...", True, (255, 255, 255))
	screen.blit(game_over_text, (200, 250))
def player(x, y):
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt( (math.pow(enemyX - bulletX,2)) + (math.pow(enemyY-bulletY, 2)))
	if distance <27:
		return True
	else:
		return False


#game loop
running = True
while running:

	if current_enemies == 0:
		level_value += 1
		next_level()
		
		#fire_bullet(bulletX, bulletY)
		#bulletY = 480
		#bulletX = playerX
		pygame.display.update()
		pygame.time.wait(5000)
		enemy_speed += 1
		spawn_enemies()
		current_enemies += num_of_enemies  # add the maximum capacity of enemies
		



	# RGB - Red, Green, Blue
	screen.fill((0,255,0))

	#background image
	screen.blit(background, (0, 0))

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change= -5

			elif event.key == pygame.K_RIGHT:
				playerX_change= 5

			elif event.key == pygame.K_SPACE:
				if bullet_state == "ready":
					bullet_sound = mixer.Sound('data/laser.wav')
					bullet_sound.play()
					bullet_state = "fire" 					

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change= 0

	#checking to make sure player stays in bo  u  nds
	playerX+= playerX_change

	if(playerX <0):
		playerX=0
	elif playerX >736:	#800 - 64 = 736
		playerX = 736




	if bulletY <= 0:
		bullet_state = "ready"
		bulletY = 480
	# Bullet Movement
	if bullet_state == "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change
	else:
		bulletX = playerX





	for i in range(num_of_enemies):
		
		# Game Over code
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over()
			break # break out of outer loop
		
		enemyX[i]+= enemyX_change[i]
		if(enemyX[i] <=0 or enemyX[i] >=736):
			for j in range(num_of_enemies):
				if j > i:						# move all the enemies in list that haven't been moved yet
					enemyX[j]+= enemyX_change[j]
				enemyX_change[j]*= -1
				enemyY[j]+=enemyY_change[j]
				enemy(enemyX[j], enemyY[j], j)
			break
		
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			bulletY = 480
			bullet_state = "ready"
			score_value += 100
			
			enemyY[i] = -200
			enemyX_change[i] = 0
			enemyY_change[i] = 0
			current_enemies -= 1


			explosion_sound = mixer.Sound('data/explosion.wav')
			explosion_sound.play()

		enemy(enemyX[i], enemyY[i], i)



	
	#pygame.time.delay(200)

	# Collision
	player(playerX, playerY)
	show_score(scoreX, scoreY)
	show_level(levelX, levelY)

	'''
	if current_enemies == 0:
		bullet_state = "ready"
		bulletY = 440
		bulletX = playerX
	'''
	pygame.display.update()