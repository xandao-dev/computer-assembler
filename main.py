from Computer import *
from pyfiglet import Figlet


def print_logo(text_logo):
    figlet = Figlet(font='slant')
    print(figlet.renderText(text_logo))


def main():
    print_logo("Computer Assembler")
    
    mouse = AddProduct(product_types['Mouse'],"Deathadder Elite", "Razer", currency_symbols['real'], 259)
    monitor = AddProduct(product_types['Monitor'], "KG241Q", "Acer", currency_symbols['real'], 1299.90, "Widescreen, Full HD, HDMI/Display Port, 144Hz")

    AssembleComputer("Meu PC", currency_symbols['real'], 'Um pc muito bom!')

if __name__ == "__main__":
    main()