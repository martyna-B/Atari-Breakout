import arcade
import random

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

COLOR_SOUND = "sounds/change_color.wav"
BREAK_SOUND = "sounds/break_down.wav"

PLAYER_MOVEMENT_SPEED = 8

class MyGame(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.coin_list = None
        self.wall_list = None
        self.block_list_1 = None
        self.block_list_2 = None
        self.block_list_3 = None
        self.block_list_4 = None

        self.color_sound = arcade.load_sound(COLOR_SOUND)
        self.break_sound = arcade.load_sound(BREAK_SOUND)
        
        self.player_list = None

        self.background = None

        self.player_sprite = None
        
        self.physics_engine = None


    def setup(self):

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.block_list_1 = arcade.SpriteList()
        self.block_list_2 = arcade.SpriteList()
        self.block_list_3 = arcade.SpriteList()
        self.block_list_4 = arcade.SpriteList()

        self.background = arcade.load_texture("images/wall.jpg")

        player_image = "images/player_wall.jpg"

        self.player_sprite = arcade.Sprite(player_image, PLAYER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.bottom = 0
        self.player_list.append(self.player_sprite)

        wally_image = "images/y_wall.jpg"

        for y in [0, 354, 708]:
            for x in [1, 1000]:
                wall = arcade.Sprite(wally_image, WALL_SCALING)
                wall.center_x = x
                wall.center_y = y
                self.wall_list.append(wall)

        wallx_image = "images/x_wall.jpg"

        for x in range(0, 1250, 354):
            wall = arcade.Sprite(wallx_image, WALL_SCALING)
            wall.center_x = x
            wall.center_y = 710
            self.wall_list.append(wall)

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
            
        ball_image = "images/ball.png"
                                  
        ball = arcade.Sprite(ball_image, BALL_SCALING)
        ball.center_x = SCREEN_WIDTH/2
        ball.bottom = 25
        ball.change_y = 0
        ball.change_x = 0
        
        self.coin_list.append(ball)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_key_press(self, key, modifiers):
        for ball in self.coin_list:
            if ball.change_y != 0:
                if key == arcade.key.LEFT or key == arcade.key.A:
                    self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                elif key == arcade.key.RIGHT or key == arcade.key.D:
                    self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            else:
                if key == arcade.key.SPACE:
                    ball.change_y = 8
                    ball.change_x = random.random()
            
    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        for ball in self.coin_list:

            ball.center_x += ball.change_x
            
            hit_walls = arcade.check_for_collision_with_list(ball, self.wall_list)
            hit_blocks1 = arcade.check_for_collision_with_list(ball, self.block_list_1)
            hit_blocks2 = arcade.check_for_collision_with_list(ball, self.block_list_2)
            hit_blocks3 = arcade.check_for_collision_with_list(ball, self.block_list_3)
            hit_blocks4 = arcade.check_for_collision_with_list(ball, self.block_list_4)
            
            hit_blocks = hit_blocks1 + hit_blocks2 + hit_blocks3 + hit_blocks4
            
            #player_wall = arcade.check_for_collision_with_list(ball, self.player_list)
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
                    ball.change_y *= 1.3
                elif block in hit_blocks3:
                    block_new = arcade.Sprite(BRICK_RED, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_2.append(block_new)
                    arcade.play_sound(self.color_sound)
                    ball.change_y *= 1.3
                    ball.change_x *= random.random()
                elif block in hit_blocks2:
                    block_new = arcade.Sprite(BRICK_BROWN, BRICK_SCALING)
                    block_new.center_x = block.center_x
                    block_new.center_y = block.center_y
                    self.block_list_1.append(block_new)
                    arcade.play_sound(self.color_sound)
                    ball.change_y *= 1.25
                else:
                    arcade.play_sound(self.break_sound)
                    ball.change_y *= 0.9
                block.remove_from_sprite_lists()

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
                    arcade.play_sound(self.break_sound)
                block.remove_from_sprite_lists()

            player_wall = arcade.check_for_collision_with_list(ball, self.player_list)
            for wall in player_wall:
                ball.bottom = wall.top
                for player in self.player_list:
                    ball.change_y *= -1
                    ball.change_x = (ball.center_x - player.center_x)*0.05
                
        self.physics_engine.update()
        
        
    def on_draw(self):
        
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.block_list_1.draw()
        self.block_list_2.draw()
        self.block_list_3.draw()
        self.block_list_4.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
