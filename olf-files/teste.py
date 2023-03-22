import curses
import subprocess

def exec_shell_command(command):
    output = subprocess.check_output(command, shell=True)
    return output.decode()

def main(stdscr):
    curses.curs_set(0)  # Esconde o cursor
    stdscr.clear()

    # Executa o comando e obtém o resultado
    output = exec_shell_command("ls")

    # Imprime o resultado na tela
    stdscr.addstr(output)

    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)