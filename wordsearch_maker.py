from word_search_data_generator import Crossword
from word_search_vizualizer import DrawGrid

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
