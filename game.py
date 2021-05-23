import arcade
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 708
SCREEN_TITLE = "Game"

WALL_SCALING = 1
PLAYER_SCALING = 0.5
BALL_SCALING = 0.15

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
        self.player_list = None

        self.player_sprite = None
        
        self.physics_engine = None

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.block_list_1 = arcade.SpriteList()

        player_image = "images/player_wall.jpg"

        self.player_sprite = arcade.Sprite(player_image, PLAYER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 0
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

        brick_image = "images/brick.jpg"

        for x in range(150, 800, 57):
            brick = arcade.Sprite(brick_image, 0.23)
            brick.center_x = x
            brick.center_y = 500
            self.block_list_1.append(brick)

        ball_image = "images/ball.png"
                                  
        ball = arcade.Sprite(ball_image, BALL_SCALING)
        ball.center_x = SCREEN_WIDTH/2
        ball.center_y = 200
        ball.change_y = 8
        ball.change_x = 0
        
        self.coin_list.append(ball)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

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
            hit_blocks = arcade.check_for_collision_with_list(ball, self.block_list_1)
            x_hits = hit_walls + hit_blocks

            for wall in x_hits:
                if ball.change_x > 0:
                    ball.right = wall.left
                elif ball.change_x < 0:
                    ball.left = wall.right
            if len(x_hits) > 0:
                ball.change_x *= -1

            ball.center_y += ball.change_y
            
            hit_walls = arcade.check_for_collision_with_list(ball, self.wall_list)
            hit_blocks = arcade.check_for_collision_with_list(ball, self.block_list_1)
            player_wall = arcade.check_for_collision_with_list(ball, self.player_list)
            y_hits = hit_walls + hit_blocks + player_wall
            for wall in y_hits:
                if ball.change_y > 0:
                    ball.top = wall.bottom
                elif ball.change_y < 0:
                    ball.bottom = wall.top        
            if len(y_hits) > 0:
                ball.change_y *= -1

            for block in hit_blocks:
                block.remove_from_sprite_lists()

            
            if ball.bottom <= 15:
                for player in self.player_list:
                    if ball.right < player.right and ball.left > player.left:
                        ball.change_y *= -1
                        ball.change_x = (ball.center_x - player.center_x)*0.03

                
        self.physics_engine.update()
        
        
    def on_draw(self):
        
        arcade.start_render()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.block_list_1.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
