import time
import neopixel
import board
import digitalio


# make a neopixel object for 10 pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
pixels.brightness = 0.5

# declare some inputs for button a and b
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

# declare some color constants
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)
Color_list = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE]

# Define variables for bottons
TimeA = 10
TimeB = 1
cnt1 = 0
cnt2 = 0
flg = 0
B_Befor = button_B.value
B_Current = None
A_Befor = button_A.value
A_Current = None


def Culculator():
    print(TimeA)


while True:
    # time.sleep(0.1)
    # gather input values
    button_a_read = button_A.value
    button_b_read = button_B.value

    # Count nembers pressed
    if button_A.value:
        if TimeA >= 0:
            TimeA -= 0.5
        else:
            TimeA = 10
        time.sleep(0.2)
        print(TimeA)
    if button_B.value:
        if TimeB <= 10:
            TimeB += 0.5
        else:
            TimeB = 0
        time.sleep(0.2)

    # Count nembers pressed
    if A_Befor != button_a_read:
        flg += 1
        A_Befor = button_A.value
        if flg == 2:
            flg = 0
        if flg == 1:
            cnt1 += 1
        print(cnt1)

    if B_Befor != button_b_read:
        flg += 1
        B_Befor = button_B.value
        if flg == 2:
            flg = 0
        if flg == 1:
            cnt2 += 1
            if cnt2 == 7:
                cnt2 = 0
        print(cnt2)

    # turn the light on
    if cnt1 % 2 == 1:
        color = Color_list[2]
        pixels.brightness = 0.1 * TimeA
    elif cnt2 % 7 != 0:
        i = cnt2 % 7
        color = Color_list[i]
        pixels.brightness = 0.1 * TimeB
    else:
        color = OFF
    pixels.fill(color)
    pixels.show()
