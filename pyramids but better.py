# make pyramids with infinite loop
import time

global x
x = "0"
x_count = 0
l = len(x)
over = False
sleep = 0.05
x_sub = 0
c = False

while True:
        if over == True:
                print(x[0:0-x_sub])
                x_sub += 1
                x_count -= 1
        else:
                print(x)
                x_count += 1
                x += "0"
                x_sub = 0

        if x_count == 20:
                if x_sub == 0:
                        over = True
        if x_count == -1:
                if x_sub == 21:
                        over = False
                        x = "0"

        time.sleep(sleep)

# Works but there's a hole for some reason
