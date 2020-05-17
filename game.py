import arcade

# constants for the screen size (obviously)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class MapGame(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.AZURE)

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        # things that need to be rendered

    def update(self, delta_time: float):
        # things that happen during the game runs
        pass


def main():
    game = MapGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
