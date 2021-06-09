import arcade, random, csv, os
import arcade.gui
from arcade.gui import UIManager

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 708
SCREEN_TITLE = "Game"

WALL_SCALING = 1
PLAYER_SCALING = 0.5
BALL_SCALING = 0.15
BRICK_SCALING = 0.3

BRICK_BROWN = "images/brick1.jpg"
BRICK_RED = "images/brick2.jpg"
BRICK_FADED = "images/brick3.jpg"
BRICK_GREY = "images/brick4.jpg"

PLAYER_IMAGE = "images/player_wall.jpg"

WALLY_IMAGE = "images/y_wall.jpg"
WALLX_IMAGE = "images/x_wall.jpg"

BALL = "images/ball.png"

COLOR_SOUND = "sounds/change_color.wav"
BREAK_SOUND = "sounds/break_down.wav"
STARTING_SOUND = "sounds/start_game.wav"
GIFT_SOUND = "sounds/pick_a_gift.wav"
BOUNCE_SOUND = "sounds/bounce.wav"

PLAYER_MOVEMENT_SPEED = 12
BALL_SPEED = 11

score = 0
num_of_bounds = 0

def take_data(index):
    """
    Returns a list which contains particular data from file "Scores.csv".

    Paramters
    ---------
    index(int): returned list that contains players' names if index equals 1
                returned list that contains players' scores if index equals 2
    """
    
    if os.path.isfile("Scores.csv"):
        if index == 1 or index == 2:
            with open("Scores.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                lines = []
                for line in csv_reader:
                    if len(line) >= 2:
                        lines.append(line[index-1])
            return lines
        else:
            raise ValueError("Index should equal 1 or 2.")
    else:
        file = open("Scores.csv", "w")
        file.close()

players_name = take_data(1)
players_score = take_data(2)

def organize_data(index):
    """
    Sorts players' scores and names according to height of scores.

    Paramters
    ---------
    index(int): returned list that contains sorted players' names if index equals 1
                returned list that contains sorted players' scores if index equals 2
    """
    
    players_score = take_data(2)
    sorted_score = []
    for score in players_score:
        num_score = eval(score)
        sorted_score.append(num_score)     
    sorted_score.sort()
    sorted_score.reverse()
    if index == 2:
        return sorted_score
    elif index == 1:
        players_name = take_data(1)
        sorted_players = []
        for i in range(0,len(sorted_score)):
            for j in range(0, len(players_score)):
                if sorted_score[i] == eval(players_score[j]):
                    sorted_players.append(players_name[j])
        return sorted_players

def score_show():
    """
    Returns text that will be shown in HIGH SCORES label.
    """
    names = organize_data(1)
    scores = organize_data(2)
    text = ""
    for i in range(0, len(names)):
        if i < 5:
            text += (names[i] + ": " + f'{scores[i]}' + "\n\n")
        else:
            break
    return text

class AtariBreakout(arcade.View):
    """
    Main apliaction class.
    """

    def __init__(self):
        """
        Initlizies game.
        """

        super().__init__()

        self.ball_list = None
        self.player_list = None
        self.player_sprite = None

        #Walls.
        self.wall_list = None
        self.block_list_1 = None
        self.block_list_2 = None
        self.block_list_3 = None
        self.block_list_4 = None

        #Extra balls.       
        self.lifes = None
        self.gift_ball = None

        self.level = 1

        #Sounds and backgrounds.
        self.color_sound = arcade.load_sound(COLOR_SOUND)
        self.break_sound = arcade.load_sound(BREAK_SOUND)
        self.gift_sound = arcade.load_sound(GIFT_SOUND)
        self.start_sound = arcade.load_sound(STARTING_SOUND)
        self.background = arcade.load_texture("images/wall.jpg")
        self.bounce_sound = arcade.load_sound(BOUNCE_SOUND)
         
        self.physics_engine = None


    def setup(self, level):
        """
        Sets up the game.

        Parameters
        ----------
        level(int): according to level's number the game looks different
        """

        global score
        global players_name
        global players_score

        players_name = take_data(1)
        players_score = take_data(2)
        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.block_list_1 = arcade.SpriteList()
        self.block_list_2 = arcade.SpriteList()
        self.block_list_3 = arcade.SpriteList()
        self.block_list_4 = arcade.SpriteList()

        self.gift_ball = arcade.SpriteList()
        self.lifes = arcade.SpriteList()

        #Placing player.
        self.player_sprite = arcade.Sprite(PLAYER_IMAGE, PLAYER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.bottom = 0
        self.player_list.append(self.player_sprite)


        #Placing walls.
        for y in [-708, -354, 0, 354, 708]:
            for x in [1, 1000]:
                wall = arcade.Sprite(WALLY_IMAGE, WALL_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        for x in range(0, 1250, 354):
            wall = arcade.Sprite(WALLX_IMAGE, WALL_SCALING)
            wall.center_x = x
            wall.center_y = 710
            self.wall_list.append(wall)


        #Placing bricks according to level.
        if level == 3:

            brown_bricks = [(8,3), (8,11), (14,7), (15,6), (15,8), (16,5), (16,9), (17,4), (17,10), (18,3), (18,11), (19,2), (19,12), (20,3), (20,11), (21,4), (21,10), (22,5), (22,9), (23,6), (23,8), (24,7)]

            for position in brown_bricks:
                brick = arcade.Sprite(BRICK_BROWN, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_1.append(brick)

            red_bricks = [(7,3), (7,11), (8,2), (8,4), (9,3), (8,10), (8,12), (9,11), (15,7), (16,6), (16,8), (17,5), (17,9), (18,4), (18,10), (19,3),(19,11), (20,4), (20,10), (21,5), (21,9), (22,6), (22,8), (23,7), (26,3), (26,11)]

            for position in red_bricks:
                brick = arcade.Sprite(BRICK_RED, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_2.append(brick)

            pink_bricks = [(11,6), (11,8), (12,5), (12,9), (13,4), (13,10), (14,3), (14,11), (15,2), (15,12), (16,7), (17,6), (17,8), (18,5), (18,7), (18,9), (19,4), (19,6), (19,8), (19,10), (20,5), (20,7), (20,9), (21,6), (21,8), (22,7)]

            for position in pink_bricks:
                brick = arcade.Sprite(BRICK_FADED, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_3.append(brick)

            grey_bricks = [(10,7), (16,1), (16,13), (17,7), (18,6), (18,8), (19,5), (19,7), (19,9), (20,6), (20,8), (21,7), (25,3), (25,11), (26,2), (26,4), (26,10), (26,12)]

            for position in grey_bricks:
                brick = arcade.Sprite(BRICK_GREY, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_4.append(brick)

        elif level == 1:

            score = 0

            brown_bricks = [(14,2), (14,12), (15,3), (15,11), (16, 2), (16, 6), (16, 8), (16, 12), (17,5), (17,9), (18,7), (19,5), (19,9), (20,6), (20,8), (21,1), (21,13)]

            for position in brown_bricks:
                brick = arcade.Sprite(BRICK_BROWN, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_1.append(brick)

            red_bricks = [(14,3), (14,11), (15,2), (15,12), (16, 3), (16, 5), (16, 7), (16, 9), (16, 11), (18, 5), (18, 9), (20,5), (20,7), (20,9)]

            for position in red_bricks:
                brick = arcade.Sprite(BRICK_RED, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_2.append(brick)

            pink_bricks = [(17,6), (17, 8), (19,6), (19,8), (22,2), (22,12), (23,3), (23,5), (23,9), (23,11), (24,4), (24,6), (24,8), (24,10)]

            for position in pink_bricks:
                brick = arcade.Sprite(BRICK_FADED, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_3.append(brick)

            grey_bricks = [(17,7), (18,6), (18,8), (19,7), (25,7)]

            for position in grey_bricks:
                brick = arcade.Sprite(BRICK_GREY, BRICK_SCALING)
                brick.right = 73*position[1] + 25
                brick.bottom = 25*position[0]
                self.block_list_4.append(brick)

        elif level == 2:

                brown_bricks = [(16,7)]
                
                for position in brown_bricks:
                    brick = arcade.Sprite(BRICK_BROWN, BRICK_SCALING)
                    brick.right = 73*position[1] + 25
                    brick.bottom = 25*position[0]
                    self.block_list_1.append(brick)

                red_bricks = [(14,7), (15,6), (15,8), (16,5), (16,9), (17,6), (17,8), (18,7)]

                for i in range(8,24):
                    red_bricks.append((i,2))
                    red_bricks.append((i, 12))

                for position in red_bricks:
                    brick = arcade.Sprite(BRICK_RED, BRICK_SCALING)
                    brick.right = 73*position[1] + 25
                    brick.bottom = 25*position[0]
                    self.block_list_2.append(brick)

                pink_bricks = [(15,7), (16,6), (16,8), (17,7)]

                for i in range(2,13):
                    pink_bricks.append((24,i))

                for position in pink_bricks:
                    brick = arcade.Sprite(BRICK_FADED, BRICK_SCALING)
                    brick.right = 73*position[1] + 25
                    brick.bottom = 25*position[0]
                    self.block_list_3.append(brick)

                grey_bricks = [(20,1), (20,3), (20,11), (20,13), (21,2), (21,3), (21,11), (21,13), (22,4), (22,10), (23,5), (23,6), (23,8), (23,9), (25,6), (25,8), (26,6), (26,8)]

                for position in grey_bricks:
                    brick = arcade.Sprite(BRICK_GREY, BRICK_SCALING)
                    brick.right = 73*position[1] + 25
                    brick.bottom = 25*position[0]
                    self.block_list_4.append(brick)
                
        #Placing a ball.                          
        ball = arcade.Sprite(BALL, BALL_SCALING)
        ball.center_x = SCREEN_WIDTH/2
        ball.bottom = 80
        ball.change_y = 0
        ball.change_x = 0 
        self.ball_list.append(ball)

        #Setting up lifes.
        life = arcade.Sprite(BALL, 0.1)
        life.center_x = len(self.lifes)*20 + 20
        life.top = SCREEN_HEIGHT - 2
        self.lifes.append(life) 

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_key_press(self, key, modifiers):
        
        for ball in self.ball_list:
            if key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.ESCAPE:
                arcade.play_sound(self.start_sound)
                game_view = TitleView()
                self.window.show_view(game_view)
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            if ball.change_y == 0:
                if key == arcade.key.SPACE:
                    ball.change_y = -BALL_SPEED
                    ball.change_x = random.random()
            
    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        
        global score
        global num_of_bounds

        #Checking if number of scores allows to move to another level. If so, sets up it.
        if self.level == 1:
            if score == 50:
                self.level = 2
                self.setup(2)
        elif self.level == 2:
            if score == 124:
                self.level = 3
                self.setup(3)
        elif self.level == 3:
            if score == 216:
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)


        #Moving gift balls and checking if player has cathed them.
        self.gift_ball.on_update(delta_time)

        for player in self.player_list:
            
            hit_gifts = arcade.check_for_collision_with_list(player, self.gift_ball)

            for gift in hit_gifts:
                life = arcade.Sprite(BALL, 0.1)
                life.center_x = len(self.lifes)*20 + 20
                life.top = SCREEN_HEIGHT - 2
                self.lifes.append(life)
                gift.remove_from_sprite_lists()
                arcade.play_sound(self.gift_sound)


        #Ball collisions.        
        for ball in self.ball_list:

            #Collisions on x axis.

            ball.center_x += ball.change_x
            
            hit_walls = arcade.check_for_collision_with_list(ball, self.wall_list)
            hit_blocks1 = arcade.check_for_collision_with_list(ball, self.block_list_1)
            hit_blocks2 = arcade.check_for_collision_with_list(ball, self.block_list_2)
            hit_blocks3 = arcade.check_for_collision_with_list(ball, self.block_list_3)
            hit_blocks4 = arcade.check_for_collision_with_list(ball, self.block_list_4)
            
            hit_blocks = hit_blocks1 + hit_blocks2 + hit_blocks3 + hit_blocks4
            
            x_hits = hit_walls + hit_blocks

            for wall in x_hits:
                if ball.change_x > 0:
                    ball.right = wall.left
                elif ball.change_x < 0:
                    ball.left = wall.right
            if len(x_hits) > 0:
                ball.change_x *= -1

            for block in hit_blocks:
                if block in hit_blocks4:
                    block_new = arcade.Sprite(BRICK_FADED, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_3.append(block_new)
                    arcade.play_sound(self.color_sound)
            
                elif block in hit_blocks3:
                    block_new = arcade.Sprite(BRICK_RED, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_2.append(block_new)
                    arcade.play_sound(self.color_sound)
                    
                elif block in hit_blocks2:
                    block_new = arcade.Sprite(BRICK_BROWN, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_1.append(block_new)
                    arcade.play_sound(self.color_sound)
                    
                else:
                    score += 1
                    arcade.play_sound(self.break_sound)
                    
                block.remove_from_sprite_lists()
                
            #Collisions for y axis
                
            ball.center_y += ball.change_y
            
            hit_walls = arcade.check_for_collision_with_list(ball, self.wall_list)
            hit_blocks1 = arcade.check_for_collision_with_list(ball, self.block_list_1)
            hit_blocks2 = arcade.check_for_collision_with_list(ball, self.block_list_2)
            hit_blocks3 = arcade.check_for_collision_with_list(ball, self.block_list_3)
            hit_blocks4 = arcade.check_for_collision_with_list(ball, self.block_list_4)
            
            hit_blocks = hit_blocks1 + hit_blocks2 + hit_blocks3 + hit_blocks4
            
            y_hits = hit_walls + hit_blocks
            
            for wall in y_hits:
                if ball.change_y > 0:
                    ball.top = wall.bottom
                elif ball.change_y < 0:
                    ball.bottom = wall.top        
            if len(y_hits) > 0:
                ball.change_y *= -1
                
            for block in hit_blocks1:
                if_gift = random.random()
                if if_gift > 0.95:
                    gift = GiftBall(BALL, 0.1)
                    gift.center_x = block.center_x
                    gift.top = block.bottom
                    self.gift_ball.append(gift)
                    
            for block in hit_blocks:
                if block in hit_blocks4:
                    block_new = arcade.Sprite(BRICK_FADED, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_3.append(block_new)
                    arcade.play_sound(self.color_sound)
                   
                elif block in hit_blocks3:
                    block_new = arcade.Sprite(BRICK_RED, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_2.append(block_new)
                    arcade.play_sound(self.color_sound)
                   
                elif block in hit_blocks2:
                    block_new = arcade.Sprite(BRICK_BROWN, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_1.append(block_new)
                    arcade.play_sound(self.color_sound)
                  
                else:
                    score += 1
                    arcade.play_sound(self.break_sound)
                
                block.remove_from_sprite_lists()

                
            #Collisions with player.
            player_wall = arcade.check_for_collision_with_list(ball, self.player_list)
            
            for wall in player_wall:
                ball.bottom = wall.top
                for player in self.player_list:
                    arcade.play_sound(self.bounce_sound)
                    num_of_bounds += 1
                    ball.change_y *= -1
                    ball.change_x = (ball.center_x - player.center_x)*0.1

            if ball.center_y < -100:
                if len(self.lifes) > 0:
                    num_of_life = 1
                    for life in self.lifes:
                        if num_of_life < len(self.lifes):
                            num_of_life += 1
                        else:
                            life.remove_from_sprite_lists()

                    ball.center_x = SCREEN_WIDTH/2
                    ball.bottom = 80
                    ball.change_y = 0
                    ball.change_x = 0
                else:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)
                
        self.physics_engine.update()
        
        
    def on_draw(self):
        
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Score: %d" % score, start_x = 35, start_y = 25, color = (0, 0, 0), font_size = 14)

        self.wall_list.draw()
        self.ball_list.draw()
        self.gift_ball.draw()
        self.lifes.draw()
        self.player_list.draw()
        self.block_list_1.draw()
        self.block_list_2.draw()
        self.block_list_3.draw()
        self.block_list_4.draw()
       
class GameOverView(arcade.View):
    """
    Class that represents window that is shown when the game is over.
    """

    def __init__(self):

        super().__init__()
        self.ui_manager = UIManager()

        #Sound and background.
        self.start_sound = arcade.load_sound(STARTING_SOUND)
        self.title_image = arcade.load_texture("images/menu_wall.jpg")
        
        #Blinking text.
        self.display_timer = 1.0
        self.show_press = False

        #Score.
        self.total_score = score + (1 - (0.5*num_of_bounds)/score)*score

    def on_update(self, delta_time: float):

        self.display_timer -= delta_time
        
        if self.display_timer < 0:
            self.show_press = not self.show_press
            self.display_timer = 1.0

    def on_draw(self):

        global score
        global num_of_bounds

        arcade.start_render()

        #Backgrounds.
        arcade.draw_texture_rectangle(center_x = SCREEN_WIDTH/2, center_y = SCREEN_HEIGHT/2,
                                      width = SCREEN_WIDTH, height = SCREEN_HEIGHT,
                                      texture = self.title_image)

        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = 400, width = SCREEN_WIDTH,
                                     height = 400, color = (255, 255, 255, 100))

        arcade.draw_rectangle_outline(center_x = SCREEN_WIDTH/2, center_y = 400, width = SCREEN_WIDTH,
                                     height = 400, color = (0, 0, 0))

        #Texts.
        arcade.draw_text("Game Over!", 200, 430, arcade.color.BLACK, 100)
        arcade.draw_text("Total score:      %d" % self.total_score, 280, 380, (0, 0, 0), 32)
        arcade.draw_text("Player's name:", 275, 325, (0,0,0), 24)
        if self.show_press:
            arcade.draw_text("Press SPACE to play again", start_x = 350, start_y = 250, 
                                color = arcade.color.BLACK, font_size = 25)

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        self.ui_manager.purge_ui_elements()

        #Input box.
        ui_input_box = arcade.gui.UIInputBox(center_x = 650, center_y = 340, width = 300)
        ui_input_box.text = "Player"
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.ui_manager.add_ui_element(ui_input_box)
        self.input_box = ui_input_box

    def on_key_press(self, key, modifiers):
        """
        When SPACE is pressed, program saves score into the CSV file and changes view to the TitleView.
        When ESCAPE is pressed, program quits.
        """
        
        global players_name
        global players_score
        
        if key == arcade.key.SPACE:
            players_name.append(f'{self.input_box.text}')
            players_score.append(f'{self.total_score}')
            data = []
            for i in range(0, len(players_name)):
                data.append([players_name[i], players_score[i]])
            with open("Scores.csv", "w", newline = '') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(data) 
            arcade.play_sound(self.start_sound)
            view = TitleView()
            self.window.show_view(view)

        elif key == arcade.key.ESCAPE:      
                arcade.close_window()

class GiftBall(arcade.Sprite):
    """
    Class that represents balls, which sometime spawn when the brick has just been broken.
    """

    def __init__(self, image_file, scale):
        super().__init__(image_file, scale)

    def on_update(self, delta_time):
        self.center_y += -4
        
class TitleView(arcade.View):
    """
    Menu window. User sees it when they run this program. 
    """

    def __init__(self):

        super().__init__()

        #Sound and background.
        self.start_sound = arcade.load_sound(STARTING_SOUND)
        self.title_image = arcade.load_texture("images/menu_wall.jpg")

        #Blinking text.
        self.display_timer = 1.0
        self.show_press = False

    def on_update(self, delta_time: float):

        self.display_timer -= delta_time
        
        if self.display_timer < 0:
            self.show_press = not self.show_press
            self.display_timer = 1.0

    def on_draw(self):

        arcade.start_render()

        #Backgrounds.
        arcade.draw_texture_rectangle(center_x = SCREEN_WIDTH/2, center_y = SCREEN_HEIGHT/2,
                                      width = SCREEN_WIDTH, height = SCREEN_HEIGHT,
                                      texture = self.title_image)

        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = 490, width = SCREEN_WIDTH,
                                     height = 250, color = (255, 255, 255, 100))

        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = 70, width = SCREEN_WIDTH,
                                     height = 50, color = (255, 255, 255, 60))

        arcade.draw_rectangle_outline(center_x = SCREEN_WIDTH/2, center_y = 490, width = SCREEN_WIDTH,
                                     height = 250, color = (0, 0, 0))
        
        #Texts.
        arcade.draw_text("Atari Breakout", start_x = 240, start_y = 500, color = arcade.color.BLACK, font_size=70)
        arcade.draw_text("Press M for more information", start_x = 310, start_y = 50, color = arcade.color.BLACK, font_size = 25)

        if self.show_press:
            arcade.draw_text("Press SPACE to start", start_x = 300, start_y = 400, color = arcade.color.BLACK, font_size = 40)
  
       
        
    def on_key_press(self, key, modifiers):
        
        """
        When SPACE is pressed, the game starts.
        When M is pressed, ImformationView is shown.
        When ESCAPE is pressed, program quits.
        """

        if key == arcade.key.SPACE:
            arcade.play_sound(self.start_sound)
            game_view = AtariBreakout()
            game_view.setup(1)
            self.window.show_view(game_view)
        elif key == arcade.key.M:
            game_view = InformationView()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:      
                arcade.close_window()

class InformationView(arcade.View):
    """
    Window with extra information: short instrucion, information about the author and high scores.
    """

    def __init__(self):

        super().__init__()

        #Sound and background.
        self.start_sound = arcade.load_sound(STARTING_SOUND)
        self.title_image = arcade.load_texture("images/menu_wall.jpg")

    def on_draw(self):

        global players_name
        global players_score

        players_name = take_data(1)
        players_score = take_data(2)
        score_text = score_show()
        
        arcade.start_render()

        #Instrucion.
        arcade.draw_texture_rectangle(center_x = SCREEN_WIDTH/2, center_y = SCREEN_HEIGHT/2,
                                      width = SCREEN_WIDTH, height = SCREEN_HEIGHT,
                                      texture = self.title_image)

        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = 595,
                                      width = SCREEN_WIDTH, height = 200, color = (255, 255, 255, 200))

        arcade.draw_text("HOW TO PLAY?", start_x = 25, start_y = 650, color = arcade.color.BLACK, font_size=32)

        arcade.draw_text("Press SPACE to start, then use arrows or WSAD keys to move your platfrom and bounce a ball.\n\nYour goal is to break down all the bricks.\n\nBroken brick may spawn a gift if you're lucky. You get one extra life if you catch it.\n\nDont let the ball fall down!",
                         start_x = 25, start_y = 500, color = arcade.color.BLACK, font_size=18)

        #Information about the author.
        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = 375,
                                      width = SCREEN_WIDTH, height = 150, color = (255, 255, 255, 200))

        arcade.draw_text("ABOUT THE AUTHOR", start_x = 25, start_y = 400, color = arcade.color.BLACK, font_size = 32)

        arcade.draw_text("My name is Martyna and I study Applied Mathematics at Wroclaw University of Science and Technology.\n\nI made this game for my programming classes.", 
                        start_x = 25, start_y = 320, color = (0, 0, 0), font_size = 18) 

        arcade.draw_rectangle_filled(center_x = SCREEN_WIDTH/2, center_y = 150,
                                      width = SCREEN_WIDTH, height = 250, color = (255, 255, 255, 200))

        #High scores.
        arcade.draw_text("HIGH SCORES:", start_x = 25, start_y = 225, color = arcade.color.BLACK, font_size = 32)
        arcade.draw_text(score_text, start_x = 25, start_y = 7, color = arcade.color.BLACK, font_size = 18)
        
    def on_key_press(self, key, modifiers):
        """
        When SPACE is pressed, TitleView is shown.
        When ESCAPE is pressed, program quits.
        """
        
        if key == arcade.key.SPACE:
            arcade.play_sound(self.start_sound)
            game_view = TitleView()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.play_sound(self.start_sound)
            game_view = TitleView()
            self.window.show_view(game_view)
                
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Atari")
    title_view = TitleView()
    window.show_view(title_view)
    arcade.run()

if __name__ == "__main__":
    main()
