from picamera2 import Picamera2
from datetime import datetime
import time
import os



camera = Picamera2()
camera.configure(camera.create_still_configuration())
camera.start()
time.sleep(2)
camera.autofocus_cycle()
time.sleep(2)

while True:
    camera.autofocus_cycle()
    time.sleep(2)    
    save_dir = f"/home/rleneweaver/Pictures/watermeter/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(save_dir, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    camera.capture_file(os.path.join(save_dir, filename))
    print(f"Saved {filename}")
    time.sleep(1800)
...

    