import os
from pptx_reading import get_text_from_pptx
from pdf_reading import get_text_from_pdf
from db import init_db, add_to_db, search_db, DEFAULT_DB_NAME
import argparse
import curses
from tqdm import tqdm

QUERY_COLOR = curses.COLOR_CYAN 
QUERY_HIGHLIGHT = curses.COLOR_BLACK #make this another color to enable highlighting

path = lambda x: os.path.join(os.path.dirname(__file__), x) #lambda path bc its fun 

    
def paginate_results(stdscr, results, search_string):
    """Paginate through the search results and display highlighted text."""
    # Clear screen
    stdscr.clear()
    
    # Set up colors in curses
    curses.start_color()
    curses.init_pair(1, QUERY_COLOR, QUERY_HIGHLIGHT)  # Red on black
    highlight = curses.color_pair(1)

    # Hide cursor
    curses.curs_set(0)


    # Get screen height and width
    height, width = stdscr.getmaxyx()

    # Initialize line index for navigating through the results
    current_result = 0
    num_results = len(results)

    while True:
        stdscr.clear()
        
        # Display the current result
        if num_results > 0:
            file_name, page, text = results[current_result]

            # Print header
            stdscr.addstr(0, 0, f'-- Result {current_result + 1}/{num_results} --')
            stdscr.addstr(1, 0, f'File: {file_name}\tPage: {page}')
            
           
            # Wrap text manually to fit screen width
            lines = [text[i:i+width-1] for i in range(0, len(text), width-1)]
            
            for i, line in enumerate(lines[:height-4]):  # Leave space for header and navigation
                line = line.replace('\x00', '')  # Remove null bytes
                if line.lower().find(search_string) !=-1:
                    stdscr.addstr(i+5, 0, line, highlight)  # 3 is where text starts
                    stdscr.addstr(i+6, 0, '\n')
                    
                    continue
                stdscr.addstr(i+5, 0, line)
                stdscr.addstr(i+6, 0, ' ')

                stdscr.refresh()

            # Navigation info
            stdscr.addstr(height-2, 0, f"Use 'j' to go down, 'k' to go up, 'q' to quit.", curses.A_BOLD)

        # Refresh the screen to update content
        stdscr.refresh()

        # Handle user input
        key = stdscr.getch()

        if key == ord('j'):
            # Move to the next result, allowing negative indexing
            current_result += 1
            if current_result >= len(results):
                current_result = 0 # Wrap around to the last item
        elif key == ord('k'):
            # Move to the previous result, allowing negative indexing
            current_result -= 1
            if current_result < 0:
                current_result = len(results) -1  # Wrap around to the first item
        elif key == ord('q'):
            break  # Quit the progra

def main(args):

    db_path = path(f'dbs/{args.database}')
    print(db_path)
    
    if args.dir: #add new files to a db
        print(args.dir, db_path)

        init_db(db_path)

        data_path = path(args.dir)
        for item in tqdm(os.listdir(data_path), desc='Reading text from files'):
            file_path = f'{data_path}/{item}'
            if item.find('.pdf') != -1:
                text = get_text_from_pdf(file_path)
                add_to_db(text, db_path)
            elif item.find('.pptx') != -1:
                text = get_text_from_pptx(file_path)
                add_to_db(text, db_path)
            else:
                print('unable to parse file type')
                continue

            

    if args.search:
        assert os.path.exists(f'{db_path}.db'), f"Database does not exist [{db_path}], try calling -r with a directory to build it first"

        results = search_db(args.search, db_path)

        #paginate_results(stdscr, results, args.search)
        curses.wrapper(paginate_results, results, args.search)

if __name__ == '__main__':

    try:
        os.mkdir(path('dbs'))
        print('Created db folder')
    except:
        print('Database folder exists')

    parser = argparse.ArgumentParser(description='Utility for quickly searching across pptx files')
    parser.add_argument('-r', '--dir', help='Directory to find pptx files from [ONLY USE FOR ADDING NEW ITEMS]')
    parser.add_argument('-s', '--search', help='Search pattern in loaded files')
    parser.add_argument('-db', '--database', help='Database do not include .db(if new will create new database)', default=DEFAULT_DB_NAME)
    args = parser.parse_args()

    #print(args)
    main(args)






    

