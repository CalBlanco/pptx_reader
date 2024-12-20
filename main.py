import os
from pptx_reading import get_text_from_pptx
from pdf_reading import get_text_from_pdf
from db import init_db, add_to_db, search_db, DEFAULT_DB_NAME
import argparse
import curses
from tqdm import tqdm
import sys
import time



QUERY_COLOR = curses.COLOR_CYAN 
QUERY_HIGHLIGHT = curses.COLOR_WHITE #make this another color to enable highlighting

path = lambda x: os.path.join(os.path.dirname(__file__), x) #lambda path bc its fun 

def show_result(stdscr, results, search_string, db, i):
    
    stdscr.clear()
    stdscr.refresh()
    
    # Set up colors in curses
    curses.start_color()
    curses.init_pair(1, QUERY_COLOR, QUERY_HIGHLIGHT)  # Red on black
    highlight = curses.color_pair(1)

    # Hide cursor
    curses.curs_set(0)

    height, width = stdscr.getmaxyx()

    while True:

        file_name, page, text = results[i]

        stdscr.addstr(1, 0, f'File: {file_name}\tPage: {page}\t From {db}')
        #stdscr.addstr(2, 0, f"DEBUG: current_result={i}", curses.A_BOLD)

        # Wrap text manually to fit screen width
        lines = [text[i:i+width-1] for i in range(0, len(text), width-1)]
        for i, line in enumerate(lines[:height-4]):  # Leave space for header and navigation
                line = line.replace('\x00', '')  # Remove null bytes
                if line.lower().find(search_string) !=-1:
                    stdscr.addstr(i+3, 0, line, highlight)  # 3 is where text starts
                    
                    continue
                stdscr.addstr(i+3, 0, line)

                stdscr.refresh()
        
        # Navigation info
        stdscr.addstr(height - 2, 0, "press 'q' to return to listing", curses.A_BOLD)
        stdscr.refresh()


        # Key handling
        key = stdscr.getch()
        if key == ord('q'):
            return list_results(stdscr, results, search_string, db, i)
        else:
            pass
            


def list_results(stdscr, results, search_string, db, j):
    stdscr.clear()

    curses.start_color()
    curses.init_pair(1, QUERY_COLOR, QUERY_HIGHLIGHT)  # Define colors
    highlight = curses.color_pair(1)

    curses.curs_set(0)

    height, width = stdscr.getmaxyx()

    current_result = j
    num_results = len(results)
    page = 0
    page_size = max(10, height - 5)  # Dynamically adjust page size
    
    #flush_input_with_delay(stdscr)
    while True:
        stdscr.clear()

        # Get range for the current page
        bot = page * page_size
        top = min(bot + page_size, num_results)
        subset = results[bot:top]

        # Debugging info
        #stdscr.addstr(height - 1, 0, f"DEBUG: current_result={current_result}, page={page}, page_range=({bot},{top})", curses.A_BOLD)

        stdscr.addstr(0, 10,f'Results for "{search_string}" in {db}     Page: {page+1}/{round(num_results/page_size)}', curses.A_BOLD)
        # Display results
        for i, res in enumerate(subset):
            file_name, page_num, _ = res
            if bot + i == current_result:  # Highlight selected result
                stdscr.addstr(2+i, 0, f"> {bot + i +1}. {file_name} -- Page: {page_num}", highlight)
            else:
                stdscr.addstr(2+i, 0, f"{bot + i +1}. {file_name} -- Page: {page_num}")

        # Navigation info
        stdscr.addstr(height - 2, 0, "Use 's' to go down one, 'w' to go up one. 'j' to go down a page, and 'k' to go up a page. 'e' to view.", curses.A_BOLD)
        stdscr.addstr(height - 1, 0, "'q' to quit.", curses.A_BOLD)
        stdscr.refresh()

        # Key handling
        key = stdscr.getch()
        if key == ord('s'):
            # Move down
            stdscr.refresh()
            current_result += 1
        elif key == ord('w'):
            # Move up
            stdscr.refresh()
            current_result -= 1
        elif key == ord('q'):
            return
        elif key == ord('e'):
            curses.curs_set(1)
            return show_result(stdscr, results, search_string, db, current_result)
        elif key == ord('j'):
            current_result += page_size
        elif key == ord('k'):
            current_result -= page_size
        else:
            continue

        if current_result < 0:  # Wrap to the last result
            current_result = num_results - 1
            page = current_result // page_size
        elif current_result < page * page_size:  # Previous page
            page -= 1

        if current_result >= num_results:  # Wrap to the first result
            current_result = 0
            page = 0
        elif current_result >= (page + 1) * page_size:  # Next page
            page += 1


def main(args):

    db_path = path(f'dbs/{args.database}')
    
    
    if args.dir: #add new files to a db
        

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

        if results is None or len(results) == 0 :
        #paginate_results(stdscr, results, args.search)
            print(f"No results for {args.search} in {db_path}.db")
        else:
            curses.wrapper(list_results, results, args.search, args.database, 0)

if __name__ == '__main__':

    try:
        os.mkdir(path('dbs'))
        print('Created db folder')
    except:
        pass

    parser = argparse.ArgumentParser(description='Utility for quickly searching across pptx files')
    parser.add_argument('-r', '--dir', help='Directory to find pptx files from [ONLY USE FOR ADDING NEW ITEMS]')
    parser.add_argument('-s', '--search', help='Search pattern in loaded files')
    parser.add_argument('-db', '--database', help='Database do not include .db(if new will create new database)', default=DEFAULT_DB_NAME)
    args = parser.parse_args()

    
    main(args)
