import os

import data

terminalX, terminalY = os.get_terminal_size()
ramSplit = .14 # Sum must add up to .97 for the scaling to work correctly
ipSplit = .44
cmdSplit = .39

ipsPerLine = (data.terminalX * ipSplit - 2) // 15 # 15 being the max length of ip addresses

logoMain = f"""
{"\033[91m██████╗░██╗░░░██╗████████╗███████╗\033[96m██████╗░██████╗░███████╗░█████╗░░█████╗░██╗░░██╗\033[97m": ^{terminalX + 12}}
{"\033[91m██╔══██╗╚██╗░██╔╝╚══██╔══╝██╔════╝\033[96m██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██║░░██║\033[97m": ^{terminalX + 12}}
{"\033[91m██████╦╝░╚████╔╝░░░░██║░░░█████╗░░\033[96m██████╦╝██████╔╝█████╗░░███████║██║░░╚═╝███████║\033[97m": ^{terminalX + 12}}
{"\033[91m██╔══██╗░░╚██╔╝░░░░░██║░░░██╔══╝░░\033[96m██╔══██╗██╔══██╗██╔══╝░░██╔══██║██║░░██╗██╔══██║\033[97m": ^{terminalX + 12}}
{"\033[91m██████╦╝░░░██║░░░░░░██║░░░███████╗\033[96m██████╦╝██║░░██║███████╗██║░░██║╚█████╔╝██║░░██║\033[97m": ^{terminalX + 12}}
{"\033[91m╚═════╝░░░░╚═╝░░░░░░╚═╝░░░╚══════╝\033[96m╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝\033[97m": ^{terminalX + 12}}
"""
dontCheat = """

▒█▀▀▄ █▀▀█ █▀▀▄ █ ▀▀█▀▀ 　 ▀▀█▀▀ █▀▀█ █░░█ 　 ▀▀█▀▀ █▀▀█ 　 █▀▀ █░░█ █▀▀ █▀▀█ ▀▀█▀▀ 
▒█░▒█ █░░█ █░░█ ░ ░░█░░ 　 ░░█░░ █▄▄▀ █▄▄█ 　 ░░█░░ █░░█ 　 █░░ █▀▀█ █▀▀ █▄▄█ ░░█░░ 
▒█▄▄▀ ▀▀▀▀ ▀░░▀ ░ ░░▀░░ 　 ░░▀░░ ▀░▀▀ ▄▄▄█ 　 ░░▀░░ ▀▀▀▀ 　 ▀▀▀ ▀░░▀ ▀▀▀ ▀░░▀ ░░▀░░ 

█░░ █▀▀█ █▀▀ █▀▀█ █░░ █▀▀ █▀▀ █▀▀█ ▀█░█▀ █▀▀ █▀▀█ 　 █▀▄▀█ █░░█ █▀▀ ▀▀█▀▀ 　 █▀▀▄ █▀▀ 　 █▀▀█ █░░█ █▀▀▄ █▀▀▄ ░▀░ █▀▀▄ █▀▀▀ 
█░░ █░░█ █░░ █▄▄█ █░░ ▀▀█ █▀▀ █▄▄▀ ░█▄█░ █▀▀ █▄▄▀ 　 █░▀░█ █░░█ ▀▀█ ░░█░░ 　 █▀▀▄ █▀▀ 　 █▄▄▀ █░░█ █░░█ █░░█ ▀█▀ █░░█ █░▀█
▀▀▀ ▀▀▀▀ ▀▀▀ ▀░░▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀░▀▀ ░░▀░░ ▀▀▀ ▀░▀▀ 　 ▀░░░▀ ░▀▀▀ ▀▀▀ ░░▀░░ 　 ▀▀▀░ ▀▀▀ 　 ▀░▀▀ ░▀▀▀ ▀░░▀ ▀░░▀ ▀▀▀ ▀░░▀ ▀▀▀▀
"""

def init():
    try:
        import pytimedinput
    except ImportError:
        import os
        os.system("pip install pytimedinput")

def graduallyRemoveText(text, index):
    for line in text.split("\n"):
        if index > 0:
            index -= 1
            print()
            continue

        print(line)
