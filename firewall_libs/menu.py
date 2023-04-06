import curses
import time


class Menu:
    def __init__(self, functionalities_Dic, header_msg, log_file) -> None:
        self.menu_options = functionalities_Dic
        self.header_msg = header_msg
        self.log_file = log_file
        self.menu_position = len(header_msg)+4
        self.status_area_position = len(
            functionalities_Dic) + len(header_msg) + 9
        self.min_col_required = 110
        self.current_row = 0
        self.option = 0
        self.screen = 0
        self.max_row = 0
        self.max_col = 0

    def _start_screen(self):
        self.screen.keypad(True)

        self._draw_header()

        curses.curs_set(0)  # esconde o cursor
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN,
                         curses.COLOR_BLACK)  # Cor verde
        curses.init_pair(2, curses.COLOR_YELLOW,
                         curses.COLOR_BLACK)  # cor Amarela
        curses.init_pair(3, curses.COLOR_RED,
                         curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA,
                         curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN,
                         curses.COLOR_BLACK)

    def _stop_screen(self):
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def _draw_header(self):
        self.screen.clear()
        self.screen.border(0)
        line = 2
        for msg in self.header_msg:
            print(msg)
            self.screen.addstr(line, 10, msg, 2)
            line += 1

        line = line + len(self.menu_options) + 3

        self.screen.addstr(line, 2, 'Status Area:', 2)
        line += 1
        self.screen.hline(line, 2, '_', 100)
        self.status_area_position = line+2
        self.screen.refresh()

    def _change_items_colors(self):
        for index, item in enumerate(self.menu_options.keys()):
            if index == self.current_row:
                self.screen.addstr(self.menu_position + index,
                                   4, item, curses.color_pair(1))
            else:
                self.screen.addstr(self.menu_position + index,
                                   4, item, curses.color_pair(2))
        self.screen.refresh()

    def _run(self, stdscr):
        try:
            self.screen = stdscr
            self.max_row, self.max_col = self.screen.getmaxyx()
            if self.status_area_position > self.max_row:
                print(
                    "A janela do terminal é muito pequena, tente com uma janela maior.")
                time.sleep(2)
                return

            self._start_screen()

            while True:
                self._change_items_colors()
                key = self.screen.getch()

                if key == curses.KEY_UP and self.current_row > 0:
                    self.current_row -= 1
                elif key == curses.KEY_DOWN and self.current_row < len(self.menu_options) - 1:
                    self.current_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    option = list(self.menu_options.keys())[self.current_row]
                    if option == "Exit":
                      #  self._stop_screen()
                        print("Até logo!")
                        break
                    else:

                        self.menu_options[option]()
                        self._draw_status_area()
        except Exception as e:

            print("Ocorreu um erro:", e)
            time.sleep(3)
        return

    def _draw_status_area(self):
        status_are_line = self.status_area_position

        with open(self.log_file, 'r+') as file:
            for line in file:
                status_are_line = status_are_line + 1
                self.max_row, self.max_col = self.screen.getmaxyx()
                if status_are_line < self.max_row:
                    parts = line.strip().split(':')
                    if len(parts) >= 3:
                        level = parts[0]
                        message = ':'.join(parts[2:])

                        if level == 'ERROR':
                            self.screen.addstr(
                                status_are_line, 10, message, curses.color_pair(3))
                        if level == 'INFO':
                            self.screen.addstr(
                                status_are_line, 10, message, curses.color_pair(1))
                        if level == 'DEBUG':
                            self.screen.addstr(
                                status_are_line, 10, message, curses.color_pair(5))
                else:
                    msg = f"O tamanho maximo do terminal atigindo ({self.max_row} X {self.max_col})! - Amplie a janela para ver mais "
                  #  self.screen.addstr(10, 50,
                    #  msg, curses.color_pair(4))

                    break
           # file.truncate(0)

    def show(self):
        curses.wrapper(self._run)
        return
