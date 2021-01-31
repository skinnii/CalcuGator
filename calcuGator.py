import pygame, os, time, random

class Equation:
	def __init__(self, text_white, text_green, text_red, x_pos, y_pos, answer, velocity, onScreen, g_counter, r_counter):
		self.text_white = text_white 
		self.text_green = text_green 
		self.text_red = text_red 
		self.x_pos = x_pos 
		self.y_pos = y_pos
		self.onScreen = onScreen
		self.answer = answer
		self.velocity = velocity
		self.green_counter = g_counter
		self.red_counter = r_counter




pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_caption("CalcuGator")
icon = pygame.image.load("crocodile.png")
pygame.display.set_icon(icon)

WIDTH, HEIGHT = 700, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
FPS = 60

user_font = pygame.font.SysFont("notomono", 20)
main_font = pygame.font.SysFont("notomono", 25)
menu_font = pygame.font.SysFont("notomono", 20)
end_font = pygame.font.SysFont("notomono", 30)
arcade_font = pygame.font.Font("ARCADE.TTF", 25)


BACKGROUND = pygame.image.load("background-black.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

gator = pygame.image.load("gator.png")
logo = pygame.image.load("gator_logo.png")

progress_bar_states = [pygame.image.load("bar_" + str(i) + ".jpg") for i in range(1, 6)]
animation = [pygame.image.load("frame_" + str(i) + "_delay-0.1s.jpg") for i in range(8)]
for i in range(len(animation)): animation[i] = pygame.transform.scale(animation[i], (60, 60))
for i in range(len(progress_bar_states)): progress_bar_states[i] = pygame.transform.scale(progress_bar_states[i], (25, 400))
logo = pygame.transform.scale(logo, (300, 200))
gator = pygame.transform.scale(gator, (55, 35))

level_up = pygame.mixer.Sound("chime_up.wav")
lost_life = pygame.mixer.Sound("wrong_answer.wav")
lost_game = pygame.mixer.Sound("Sad_Trombone.wav")
winning_sound = pygame.mixer.Sound("winning_sound.wav")
chomp_sound = pygame.mixer.Sound("croc_chomp_x.wav")

music = pygame.mixer.music.load("retro_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)



def generate(lvl, diff):
	def op(sign, a, b):
		if sign == "+": 
			return a + b
		if sign == "-": 
			return a - b
		if sign == "/": 
			return a / b
		if sign == "*":
			return a * b

	eq = []
	operations = ["+", "-", "*", "/"]
	# x_range = [True for i in range(WIDTH - 100)]
	y_range = [True for i in range(-1000 - (lvl * 100), 0)]


	for i in range(lvl * 5):

		sign = random.choice(operations)
		if diff == 10:
			if sign == operations[0] or sign == operations[1]: v = 2
			if sign == operations[2] or sign == operations[3]: v = 1
		else: 
			v = 1


		a = random.randint(1, 5*lvl+diff)
		b = random.randint(1, 5*lvl+diff)

		if sign == "/": 
			while a % b != 0 or a == b or a == 1 or b == 1 :
				a = random.randint(1, 5*lvl+diff)
				b = random.randint(1, 5*lvl+diff)

		answer = int(op(sign, a, b))
		text_white = arcade_font.render(str(a)+ " " + sign + " " + str(b), 1, WHITE)
		text_green = arcade_font.render(str(a)+ " " + sign + " " + str(b), 1, GREEN)
		text_red = arcade_font.render(str(a)+ " " + sign + " " + str(b), 1, RED)

		green_counter = 0
		red_counter = -1


		x_pos = random.randint(100, WIDTH - text_white.get_width() - 100)
		y_pos = random.randint(-1000 - (lvl * 100), 0 - text_white.get_height())

		while y_range[y_pos] == False or y_range[y_pos + text_white.get_height()] == False:
			y_pos = random.randint(-1000 - (lvl * 100), 0 - text_white.get_height())
			
		for y in range(y_pos, y_pos + text_white.get_height() + 1):
			y_range[y] = False
		
		e = Equation(text_white, text_green, text_red, x_pos, y_pos, answer, v, True, green_counter, red_counter)
		
		eq.append(e)

        

	y_range = [True for i in range(-1000 - (lvl * 100), 0)]
	return eq

def check(eq):
	for e in eq:
		if e.onScreen == True:
			return False

	return True


def main_menu():
	run = True
	arcade_text = arcade_font.render("Press any key to start.", 1, GREEN)

	while run:
		WINDOW.blit(BACKGROUND, (0, 0))	
		WINDOW.blit(arcade_text, (int(WIDTH/2 - arcade_text.get_width()/2), int(HEIGHT/2 - arcade_text.get_height()/2)))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				intermediate_screen()
				run = False


		pygame.display.update()


	pygame.quit()


def main_game(diff):
	clock = pygame.time.Clock()
	run = True

	string = ''
	lvl = 1
	eq = generate(lvl, diff)
	lives = 10
	frames = 0

	lives_text = arcade_font.render("Lives: ", 1, YELLOW)
	level_text = arcade_font.render("Level: ", 1, YELLOW)


	while run:
		
		WINDOW.blit(BACKGROUND, (0, 0))
		frames += 0.12
		frames %= 8
		WINDOW.blit(animation[int(frames)], (630, 520))	
		WINDOW.blit(logo, (int(WIDTH/2 - logo.get_width()/2), int(HEIGHT/2 - logo.get_height()/2)))
		WINDOW.blit(progress_bar_states[lvl-1], (650, 100))	
		
		if lvl == 5:

			run = False
			pygame.mixer.music.pause()
			winning_sound.play()

			win_text = arcade_font.render("Congrats. You are a true", 1, GREEN)
			calcu_text = arcade_font.render("Calcu", 1, BLUE)
			gator_text = arcade_font.render("Gator", 1, ORANGE)

			WINDOW.blit(BACKGROUND, (0, 0))
			WINDOW.blit(progress_bar_states[-1], (650, 100))
			WINDOW.blit(win_text, (int(WIDTH/2 - (win_text.get_width() + calcu_text.get_width() + gator_text.get_width())/2  ), int(HEIGHT/2 - win_text.get_height()/2)))
			WINDOW.blit(calcu_text, (int(WIDTH/2 + win_text.get_width()/2 - calcu_text.get_width() + 12), int(HEIGHT/2 - win_text.get_height()/2)))
			WINDOW.blit(gator_text, (int(WIDTH/2 + win_text.get_width()/2 + calcu_text.get_width() - gator_text.get_width() + 16), int(HEIGHT/2 - win_text.get_height()/2)))
			
			pygame.display.update()
			pygame.time.wait(4000)
			end_screen()

			break


		if check(eq):
			lvl += 1
			if lvl != 5: level_up.play()
			eq = generate(lvl, diff)

		for i in range(len(eq)):

			if eq[i].y_pos + eq[i].text_white.get_height() > HEIGHT and eq[i].onScreen == True:
				eq[i].onScreen = False
				lives -= 1
				lost_life.play()



			elif eq[i].onScreen == True:


				eq[i].y_pos += eq[i].velocity

				if eq[i].red_counter >= 0 and eq[i].red_counter < FPS/10: #wrong answer
					WINDOW.blit(eq[i].text_red, (eq[i].x_pos, eq[i].y_pos))
					eq[i].red_counter += 1

				else:
					WINDOW.blit(eq[i].text_white, (eq[i].x_pos, eq[i].y_pos))
			
			else: #right answer

				if eq[i].green_counter < FPS/10 and eq[i].y_pos + eq[i].text_white.get_height() < HEIGHT:
					WINDOW.blit(eq[i].text_green, (eq[i].x_pos, eq[i].y_pos))
					eq[i].green_counter += 1



		if lives == 0:

			run = False
			pygame.mixer.music.pause()
			lost_game.play()

			loser_text = arcade_font.render("Better luck next time Gator...", 1, RED)

			WINDOW.blit(BACKGROUND, (0, 0))
			WINDOW.blit(loser_text, (int(WIDTH/2 - loser_text.get_width()/2), int(HEIGHT/2 - loser_text.get_height()/2)))
			
			pygame.display.update()
			pygame.time.wait(5000)
			
			end_screen()
			break



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				string += event.unicode



					
				if event.key == pygame.K_BACKSPACE:
					string = string[:-2]

				if event.key == pygame.K_RETURN:
					correct = False
					for i in range(len(eq)):
						if eq[i].onScreen == False:
							continue
						if string[:-1] == str(eq[i].answer):
							eq[i].onScreen = False
							correct = True
							WINDOW.blit(eq[i].text_green, (eq[i].x_pos, eq[i].y_pos))

					if correct == False:
						for i in range(len(eq)):
							eq[i].red_counter = 0


					string = ''


		input_text = arcade_font.render(string, 1, GREEN)
		lives_counter = arcade_font.render(str(lives), 1, WHITE)
		level_counter = arcade_font.render(str(lvl), 1, WHITE)

		WINDOW.blit(input_text, (int(WIDTH / 2 - input_text.get_width() / 2), 500))
		WINDOW.blit(lives_text, (15, 15))
		WINDOW.blit(level_text, (int(WIDTH - 25 - level_text.get_width()), 15))

		WINDOW.blit(lives_counter, (17 + lives_text.get_width() , 15))
		WINDOW.blit(level_counter, (WIDTH - 23, 15))





		pygame.display.update()
		clock.tick(FPS)


def end_screen():
	clock = pygame.time.Clock()
	run = True
	margin = 30
	separation = 30
	rect_width = 400
	rect_height = 100

	end_text = arcade_font.render("Restart", 1, WHITE)
	exit_text = arcade_font.render("Exit", 1, WHITE)

	restart_rec = pygame.Rect(int(WIDTH / 2 - rect_width / 2), int(HEIGHT / 2 - rect_height - separation), rect_width, rect_height) 
	exit_rec = pygame.Rect(restart_rec.topleft[0], restart_rec.bottomleft[1] + separation * 2, rect_width, rect_height)


	pygame.mixer.music.unpause()

	while run:
		WINDOW.blit(BACKGROUND, (0, 0))
		WINDOW.blit(end_text, (int(WIDTH / 2 - end_text.get_width() / 2), int(restart_rec.topleft[1] + (rect_height - end_text.get_height()) / 2  )))
		WINDOW.blit(exit_text, (int(WIDTH / 2 - exit_text.get_width() / 2), int(exit_rec.topleft[1] + (rect_height - exit_text.get_height()) / 2  )))
		pygame.draw.rect(WINDOW, GREEN, restart_rec, 4)
		pygame.draw.rect(WINDOW, RED, exit_rec, 4)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				click_restart = restart_rec.collidepoint(pygame.mouse.get_pos())
				click_exit = exit_rec.collidepoint(pygame.mouse.get_pos())

				if click_restart == 1:
					run = False
					chomp_sound.play()
					intermediate_screen()


				elif click_exit == 1:
					run = False



		pygame.display.update()
		clock.tick(FPS)


def intermediate_screen():
	clock = pygame.time.Clock()
	run = True
	margin_left = 50
	margin_top = 125
	separation = 20
	rect_width =  150
	rect_height = 425

	prompt_text = arcade_font.render("Choose the difficulty :", 1, WHITE)
	easy_text = arcade_font.render("Easy", 1, GREEN)
	medium_text = arcade_font.render("Medium", 1, YELLOW)
	hard_text = arcade_font.render("Hard", 1, RED)

	medium_rect = pygame.Rect(int(WIDTH/2 - rect_width/2), margin_top, rect_width, rect_height)
	easy_rect = pygame.Rect(medium_rect.topleft[0] - (separation * 2) - rect_width , margin_top, rect_width, rect_height) 
	hard_rect = pygame.Rect(medium_rect.topright[0] + (separation * 2), medium_rect.topright[1], rect_width, rect_height)


	while run:
		WINDOW.blit(BACKGROUND, (0, 0))
		# WINDOW.blit(end_text, (int(WIDTH / 2 - end_text.get_width() / 2), int(restart_rec.topleft[1] + (rect_height - end_text.get_height()) / 2  )))
		WINDOW.blit(prompt_text, (int(WIDTH / 2 - prompt_text.get_width()/2), 30))
		WINDOW.blit(easy_text, (int(easy_rect.topleft[0] + ((rect_width - easy_text.get_width())/2)), int(easy_rect.topleft[1] + ((rect_height - easy_text.get_height())/2))))
		WINDOW.blit(medium_text, (int(medium_rect.topleft[0] + ((rect_width - medium_text.get_width())/2)), int(medium_rect.topleft[1] + ((rect_height - medium_text.get_height())/2))))
		WINDOW.blit(hard_text, (int(hard_rect.topleft[0] + ((rect_width - hard_text.get_width())/2)), int(hard_rect.topleft[1] + ((rect_height - hard_text.get_height())/2))))
		# WINDOW.blit(medium_text, (int(WIDTH / 2 - prompt_text.get_width()/2), 20))
		# WINDOW.blit(hard_text, (int(WIDTH / 2 - prompt_text.get_width()/2), 20))
		pygame.draw.rect(WINDOW, GREEN, easy_rect, 10)
		pygame.draw.rect(WINDOW, YELLOW, medium_rect, 10)
		pygame.draw.rect(WINDOW, RED, hard_rect, 10)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				click_easy = easy_rect.collidepoint(pygame.mouse.get_pos())
				click_medium = medium_rect.collidepoint(pygame.mouse.get_pos())
				click_hard = hard_rect.collidepoint(pygame.mouse.get_pos())

				if click_easy == 1:
					run = False
					chomp_sound.play()
					main_game(5)


				elif click_medium == 1:
					run = False
					chomp_sound.play()
					main_game(7)

				elif click_hard == 1:
					run = False
					chomp_sound.play()
					main_game(10)



		pygame.display.update()
		clock.tick(FPS)
			


def main():

	main_menu()


main()



