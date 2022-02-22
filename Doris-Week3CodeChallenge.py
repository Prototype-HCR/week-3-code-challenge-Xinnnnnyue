import time
import board
from digitalio import DigitalInOut, Pull
import neopixel

# declare the color
RED = 0xff0000
GREEN = 0x00ff00
BLUE = 0x0000ff
YELLOW = 0xffff00
CYAN = 0x00ffff
MAGENTA = 0xff00ff
WHITE = 0xffffff
OFF = 0x000000

# initialize the neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

# declare a digitial input
button_a = DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=Pull.DOWN)
button_b = DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=Pull.DOWN)


# put all the colors in a list
colors = [RED, MAGENTA, BLUE, CYAN, GREEN, YELLOW, WHITE]

# track if the button has been clicked
clicked_a = False
clicked_b = False
click_count = 0
click_time_a = 0
click_time_b = 0
pixels_state = False

# a variable to track how long the button is Pressed
press_duration_a = 0
press_duration_b = 0

# a threshold value to compare to a press_duration
LONG_PRESS_THRESHOLD = 1

# keep track of brightness
brightness_value = 0.5

# a varible to track the previous reading of the button
button_a_pre = button_a.value
button_b_pre = button_b.value

while True:
    # gather input values as an integer
    button_a_read = button_a.value
    button_b_read = button_b.value

    # compare this reading to the previous value
    if button_a_read != button_a_pre:
        # the button value has changed
        # save the read to previous for next iteration of the loop
        button_a_pre = button_a_read
        if button_a_read:
            # the button changed from False to True (click)
            # print("Button A changed Not to Pressed")
            # the button is clicked set the clicked variable to True
            clicked_a = True
            # save the current time of the click
            click_time_a = time.monotonic()
            print("click time is:", click_time_a) # print
        else:
            # the button changed from True to False (release)
            print("Button A changed Pressed to Not")
            # has the button been clicked without being reset?
            if clicked_a:
                print("Short Press Detected for Button A, light state changed")
                # check the pixels are on
                pixels_state = not pixels_state #-----#

    else:
        # The button value is the same as last time is it pressed?
        if button_a_read:
            if clicked_a:
                # calculate how much time has passed since the last click
                press_duration_a = time.monotonic() - click_time_a
                print("Press duration is:", press_duration_a)
                if pixels_state:
                    if press_duration_a >= LONG_PRESS_THRESHOLD:
                        print("Long Press Detected for Button A, brightness decreased")
                        brightness_value -= 0.25
                        clicked_a = False


    if button_b_read != button_b_pre:
        # the button value has changed
        # save the read to previous for next iteration of the loop
        button_b_pre = button_b_read
        if button_b_read:
            # the button changed from False to True (click)
            print("Button B changed Not to Pressed")
            # the button is clicked set the clicked variable to True
            clicked_b = True
            # save the current time of the click
            click_time_b = time.monotonic()
            print("click time is:", click_time_b)
        else:
            # the button changed from True to False (release)
            print("Button B changed Pressed to Not")
            # has the button been clicked without being reset?
            if clicked_b:
                # check the pixels are on
                if pixels_state:
                    print("Short Press Detected for Button B, light color changed")
                    # they are on increment the click count
                    click_count += 1
                    print("click count is", click_count)
                else:
                    click_count -= 1
                    print("Error, light is switched off")
    else:
        # The button value is the same as last time is it pressed?
        if button_b_read:
            # the button is Pressed
            if clicked_b:
                # calculate how much time has passed since the last click
                press_duration_b = time.monotonic() - click_time_b
                print("Press duration is:", press_duration_b)
                # are the pixels on?
                if pixels_state:
                    # the pixels are on
                    if press_duration_b >= LONG_PRESS_THRESHOLD:
                        # the press_duration is longer than the threshold
                        print("Long Press Detected for Button B, brightness increased")
                        # toggle the pixels_state
                        brightness_value += 0.25
                        # reset the clicked variable to prevent repeated
                        clicked_b = False



    # calculate the modulus of the click_count
    # modulus is just the remainder of division by a given divisor
    # the divisor must be the length (len(colors)) of the color list
    click_modulo = click_count % len(colors)
    # use click_modulo to select a color from the colors list
    color = colors[click_modulo]

    # do output based on input and calculated variables
    # if pixels_state is true the pixels should be on
    if pixels_state:
        # fill the pixels with the proper color
        pixels.fill(color)
        #-do the brightness here
        pixels.brightness = brightness_value
    else:
        # pixels should be off, fill them as such
        pixels.fill(OFF)


    # sleep to see changes in the serial monitor
    time.sleep(0.01)
