from PIL import Image, ImageDraw, ImageFont
from word_search_data_generator import Crossword


class DrawGrid:
    def __init__(self, letter_grid, words, cell_size=50, font_size=40, sidebar_width=200,
                            font_path="DejaVuSans.ttf"):
        """

        :param letter_grid: The 2D array for the word search grid
        :param words: The words in the word search
        :param cell_size: The size of each cell in the word search
        :param font_size:
        :param sidebar_width:
        :param font_path: The directory for the font used in the word search relative to this script
        """

        self.letter_grid = letter_grid
        self.words = words
        self.cell_size = cell_size
        self.font_size = font_size
        self.sidebar_width = sidebar_width
        self.font_path = font_path
        self.get_image = self.main()

    def main(self):
        self.setup_grid()
        self.create_canvas()
        self.fill_grid()
        self.sidebar()
        # print('yes')
        return self.image


    def setup_grid(self):
        """Calculate the size of the grid"""
        self.rows = len(self.letter_grid)
        self.cols = len(self.letter_grid[0]) if self.rows > 0 else 0
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size

    def create_canvas(self):
        """ Create a new blank image with a sidebar"""
        total_width = self.width + self.sidebar_width
        self.image = Image.new('RGBA', (total_width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.image)

        # Load the font
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            self.font = ImageFont.load_default()

    def fill_grid(self):
        """Fill the grid with letters"""
        for row in range(self.rows):
            for col in range(self.cols):
                letter = self.letter_grid[row][col]
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                text_bbox = self.draw.textbbox((0, 0), letter, font=self.font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = x - text_width // 2
                text_y = y - text_height // 2
                self.draw.text((text_x, text_y), letter, fill='black', font=self.font)

    def sidebar(self):
        # Draw the sidebar with words
        sidebar_x = self.width + 20  # Start drawing the sidebar 20 pixels from the grid
        sidebar_y = 20  # Start 20 pixels from the top
        sidebar_font_size = 20  # Adjust font size for sidebar
        try:
            sidebar_font = ImageFont.truetype(self.font_path, sidebar_font_size)
        except IOError:
            sidebar_font = ImageFont.load_default()

        for word in self.words:
            self.draw.text((sidebar_x, sidebar_y), word, fill='black', font=sidebar_font)
            sidebar_y += sidebar_font_size + 10  # Adjust spacing between words


if __name__ == '__main__':
    # Load list of words
    words = ['PHP', 'JAVA', 'JAVASCRIPT', 'HTML', 'SWIFT', 'RUBY', 'FORTRAN', 'SQL', 'BASIC', 'RUST']

    #Create word-search object to hold data
    crossword = Crossword(13, words=words, allow_reverse=True)

    # Build the data for the word search. Return and save the data.
    word_data = crossword.build_grid()

    # Directory for the font
    font_path ='fonts/MouldyCheeseRegular-WyMWG.ttf'

    # Create object to display thr word search
    word_search_grid = DrawGrid(word_data, words, font_path=font_path)

    # Call object attribute that allows saving the word-search to a file
    word_search_grid.get_image.save('word_search_grid_with_sidebar2.png')

