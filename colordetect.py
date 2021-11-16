import pandas as pd
import cv2

img_path = 'C:/Users/abk/Desktop/colorpic.jpg'
csv_path = 'C:/Users/abk/Desktop/colors.csv'

# To read the csv file.....
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
dframe = pd.read_csv(csv_path, names=index, header=None)

# To read the image......
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# Now to declare global variables....
clicked = False
r = g = b = xpos = ypos = 0


# The function to calculate the min distance from all colors & get the most matching color
def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(dframe)):
        d = abs(R - int(dframe.loc[i, 'R'])) + abs(G - int(dframe.loc[i, 'G'])) + abs(B - int(dframe.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = dframe.loc[i, 'color_name']
    return cname


# The function to get x , y coordinates of mouse double click.....
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# To create window.....
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        # cv2.rectangle(image,start point, end point, color,thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

        # To create text string to display color name and RGB value
        text = get_color_name(r, g, b) + 'R=' + str(r) + 'G=' + str(g) + 'B=' + str(b)
        # cv2.putText(img,text,start,font(0-7),fontScale, color,thickness,lineType)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors we will display text in black color....
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()