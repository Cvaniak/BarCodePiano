from barcode import Code128
from barcode.writer import ImageWriter
try:
    import winsound
except ImportError:
    import os
    def playsound(frequency,duration):
        #apt-get install beep
        os.system(f'play -n synth {duration} tri {frequency}')
else:
    def playsound(frequency,duration):
        winsound.Beep(frequency,duration)


# Frequency generator
for i in range(100, 1200, 100):
    name = f"sound{i}"
    my_code = Code128(f"{name}q", writer=ImageWriter())
    my_code.save(f"{name}")


import sys
from PIL import Image

sound_files = [x for x in os.listdir(".") if x.startswith("sound")]

images = [Image.open(x) for x in sound_files]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = (max(heights)-50)

new_im = Image.new('RGB', ((total_width+700)//2, max_height*2), color=(255,255,255,0))

x_offset = 0
y_offset = 0
for i, im in enumerate(images):
  new_im.paste(im, (x_offset, y_offset))
  x_offset += im.size[0]+10
  if i == 4:
      x_offset = 0
      y_offset += max_height 

new_im.save('test.jpg')

from pynput import keyboard
start = False
tab = []

def on_press(key):
    global start, tab
    try:
        if key.char == "s" and not start:
            print("start")
            start = True
        elif key.char == "q":
            print("end", tab)
            tab = "".join(tab)
            start = False
            if "ound" in tab[:4]:
                print("palyed")
                playsound(int(tab[4:]), 0.200)
            tab = []
        else:
            tab.append(key.char)
        

    except AttributeError:
        ...

def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()