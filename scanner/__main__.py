from .adafruit import Input, Display
from .scanimg import Scanner
from common.config import Config
import scanner.fonts as fonts
import common.access_token as access_token
import time
import os

MONTHS = ["Jan", "Feb", "Mar", "Aprl", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
PADDING_VERT = 5
PADDING_HORIZ = 5
TOKEN_CACHE_INVALIDATE = 10

global current_selection # year=0, month=1
global current_month
global current_year
global is_scanning
global token_cache_time
global token

upload_dir = Config.DIR_SCANNED_PHOTOS
token_cache_time = 0
token = ''

def get_ip():
    import socket
    hostname = socket.gethostname()   
    return socket.gethostbyname(hostname+'.local')

def get_num_files_processing():
    return len([name for name in os.listdir(upload_dir) if os.path.isfile('%s/%s'%(upload_dir,name))])


def check_input(draw):
    global is_scanning
    global current_year
    global current_month
    global current_selection

    if is_scanning:
        return

    if(controller.button_top()):
        is_scanning = True
        return

    modifier = 0
    if(controller.up()):
        modifier = 1
    elif(controller.down()):
        modifier = -1

    if current_selection == 0:
        current_year += modifier
    elif current_selection == 1:
        month = current_month + modifier
        if(0 <= month and month <= 12):
            current_month = month

    if(controller.left() and current_selection == 1):
        current_selection = 0
    elif(controller.right() and current_selection == 0):
        current_selection = 1

def event_loop(draw):    
    global current_year
    global current_month
    global is_scanning
    global current_selection
    global token_cache_time
    global token

    #### Actions ####
    if is_scanning:
        from datetime import date
        d = date(current_year, current_month+1, 2)
        scanner.batch_scan(d)
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
    year_fill = "black" if current_selection == 0 else "white"
    year_text = 'Y: %s'%(current_year)
    (year_font, year_font_size) = fonts.large()
    year_xy = (PADDING_HORIZ, 0)
    if current_selection == 0:
        rect_xy = (
            (0, 0), 
            (display.width/2, year_font_size+PADDING_VERT)
        )
        draw.rectangle(rect_xy, fill="white")
    draw.text(year_xy, year_text, font=year_font, fill = year_fill)

    # Draw Month
    month_fill = "black" if current_selection == 1 else "white"
    month_text = 'M: %s'%(MONTHS[current_month])
    (month_font, month_font_size) = fonts.large()
    month_xy = (display.width/2+PADDING_HORIZ, 0)
    if current_selection == 1:
        rect_xy = (
            (display.width/2, 0), 
            (display.width, month_font_size+PADDING_VERT)
        )
        draw.rectangle(rect_xy, fill="white")
    draw.text(month_xy, month_text, font=month_font, fill = month_fill)

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
    
    if time.time()-token_cache_time > TOKEN_CACHE_INVALIDATE:
        token = access_token.get_token()
        token_cache_time = time.time()

    if token == None or token == '':
        text = 'Login at ' + get_ip()
        (font, size) = fonts.small()
        xy = (0, display.height/2-size/2)
        draw.text(xy, text, font=font, fill="white")

if __name__ == '__main__':
    print('Photos to Upload are stored in "%s"'%(upload_dir))

    scanner = Scanner(upload_dir)
    controller = Input()
    display = Display()
    current_year = 2000
    current_month = 0
    is_scanning = False
    current_selection = 0

    print('Running Event Loop')
    display.run(event_loop)