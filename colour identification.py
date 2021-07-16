import cv2
import pandas as pd

img_path = 'image 1.jpeg'
csv_path = 'colors.csv'

index = ['colour', 'colour_name', 'number', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

img = cv2.imread(img_path)
img = cv2.resize(img, (640, 480))

clicked = False
r = g = b = xpos = ypos = 0


def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global clicked, r, g, b, xpos, ypos
        clicked = True
        xpos = x
        ypos = y
        # print(x, y)
        b, g, r = img[y, x]
        b = int(b)  # else it is of type numpy int8
        g = int(g)
        r = int(r)


def get_colour_name(R, G, B):
    global color_name
    minimum = 1000
    for i in range(len(df)):
        diff = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))

        if diff <= minimum:
            minimum = diff
            color_name = df.loc[i, 'colour_name']
    return color_name


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        cv2.rectangle(img, (20, 20), (500, 45), (b, g, r), cv2.FILLED)
        text = f'{get_colour_name(r, g, b)} R={r} G={g} B={b}'
        if r + g + b <= 600:
            cv2.putText(img, text, (25, 37), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
        else:
            cv2.putText(img, text, (25, 37), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 0, 0))

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
