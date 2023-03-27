import curses
import time
class Menu:
    def __init__(self,menu_itens, menu_funcitons, header_msg) -> None:
        self.menu_itens=menu_itens
        self.menu_functions=menu_funcitons
        self.header_msg=header_msg
        self.menu_position=len(header_msg)+4
        self.status_area_position=0
        self.current_row = 0
        self.option = 0
        self.screen=curses.initscr()
        
   
    

        

    def check_parametre(self):
        if len(self.menu_itens) != len(self.menu_functions):
            raise Exception("Parâmetros de tamanhos diferentes")
    
        
            

    
    def start_screen(self):
        self.screen.keypad(True)
        self.draw_header()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Cor verde
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # cor Amarela
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
           
    def stop_screen(self):
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


    def draw_header(self):
        self.screen.clear()
        self.screen.border(0)
        line=3          
        for msg in self.header_msg:
            print(msg)
            self.screen.addstr(line,10,msg,2)
            line +=1
        
        line = line + len(self.menu_itens) +3
        self.screen.addstr(line, 2,'Status Area:',2)
        line +=1
        self.screen.hline(line, 2, '_',100)
        self.status_are_position=line+2
        self.screen.refresh()
        
    def change_items_colors(self):
        for index, item in enumerate(self.menu_itens):
            if index == self.current_row:
                    self.screen.addstr(self.menu_position + index, 4, item, curses.color_pair(1))
            else:
                    self.screen.addstr(self.menu_position + index, 4, item, curses.color_pair(2))
        self.screen.refresh()
            


    def show(self):

        try:
            self.check_parametre()
        
            self.start_screen()
            while True:    
                
                #self.draw_header()
                self.change_items_colors()           
                key = self.screen.getch()
                if key == curses.KEY_UP and self.current_row > 0:
                    self.current_row -= 1
                elif key == curses.KEY_DOWN and self.current_row < len(self.menu_itens) - 1:
                    self.current_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    option = self.current_row
                    if self.menu_itens[option]=="sair":
                        self.stop_screen()   
                        print("Até logo!") 
                        break
                    else:
                        self.menu_functions[option]()
                    #drawMsgStatusArea(functionsList[option](),screen)
        except Exception as e:
            pass
            # Código a ser executado em caso de exceção
            self.stop_screen()
            print("Ocorreu um erro:",e)



        return
                