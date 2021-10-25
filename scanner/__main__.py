from .adafruit import Input, Display
from .scanimg import Scanner
from common.config import Config
import scanner.fonts as fonts

import os

global current_year
global is_scanning

upload_dir = Config.DIR_SCANNED_PHOTOS

def get_ip():
    import socket
    hostname = socket.gethostname()   
    return socket.gethostbyname(hostname+'.local')

def get_num_files_processing():
    return len([name for name in os.listdir(upload_dir) if os.path.isfile('%s/%s'%(upload_dir,name))])

def check_input(draw):
    global is_scanning
    global current_year

    if is_scanning:
        return

    if(controller.button_top()):
        is_scanning = True
        return

    if(controller.up()):
        current_year += 1
    if(controller.down()):
        current_year -= 1

def event_loop(draw):
    global current_year
    global is_scanning

    #### Actions ####
    if is_scanning:
        from datetime import date
        d = date(current_year, 1, 2)
        scanner.scan_image(d)
        is_scanning = False
        return

    #### Drawing ####
    check_input(draw)
    photos_to_process = get_num_files_processing()

    # Draw Current IP
    ip_text = 'IP: %s'%(get_ip())
    (ip_font, ip_font_size) = fonts.xsmall()
    ip_xy = (0, display.height-ip_font_size)
    draw.text(ip_xy, ip_text, font=ip_font, fill = "white")

    # Draw Year
    year_text = 'Year: %s'%(current_year)
    (year_font, year_font_size) = fonts.large()
    year_xy = (0, 0)
    draw.text(year_xy, year_text, font=year_font, fill = "white")

    # Draw Photos to Upload
    ptp_text = 'Photos to Upload: %s '%(photos_to_process)
    (ptp_font, ptp_font_size) = fonts.small()
    ptp_xy = (0, ip_xy[1]-ptp_font_size)
    draw.text(ptp_xy, ptp_text, font=ptp_font, fill = "white")

    if is_scanning:
        text = 'Scanning... '
        (font, size) = fonts.small()
        xy = (0, display.height/2-size/2)
        draw.text(xy, text, font=font, fill="white")


if __name__ == '__main__':
    print('Photos to Upload are stored in "%s"'%(upload_dir))

    scanner = Scanner(upload_dir)
    controller = Input()
    display = Display()
    current_year = 2000
    is_scanning = False

    print('Running Event Loop')
    display.run(event_loop)