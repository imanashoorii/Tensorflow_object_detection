import os
import uuid
import cv2
import time

### Define Image Labels
labels = ['thumbsup', 'thumbsdown', 'thankyou', 'livelong']
images_cnt = 5

### Setup Folders
IMAGES_PATH = os.path.join('Tensorflow', 'workspace', 'images', 'collectedImages')
if not os.path.exists(IMAGES_PATH):
    if os.name == 'posix':
        os.system(f'mkdir -p {IMAGES_PATH}')
    if os.name == 'nt':
        os.system(f'mkdir {IMAGES_PATH}')
for label in labels:
    path = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(path):
        os.system(f'mkdir {path}')

for label in labels:
    cap = cv2.VideoCapture(0)
    print('Collecting images for {}'.format(label))
    for num in range(images_cnt):
        print('Collecting image {}'.format(num))
        ret, frame = cap.read()
        filename = os.path.join(IMAGES_PATH, label, label+'.'+'{}.jpg'.format(str(uuid.uuid4())))
        cv2.imwrite(filename, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

LABELLING_PATH = os.path.join('Tensorflow', 'labeling')
if not os.path.exists(LABELLING_PATH):
    os.system(f'mkdir {LABELLING_PATH}')
    os.system(f'git clone https://github.com/tzutalin/labelImg {LABELLING_PATH}')
if os.name == 'posix':
    os.system(f'cd {LABELLING_PATH} && make qt5py3')
if os.name == 'nt':
    os.system(f'cd {LABELLING_PATH} && pyrcc5 -o libs/resources.py resources.qrc')

os.system(f'cd {LABELLING_PATH} && python labelImg.py')
