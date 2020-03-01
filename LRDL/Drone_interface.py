from drone_gs_functions import *


dst_add = 'GST'
dev_add = 'UAV'
max_packet_len = 200

data = np.array([(2.43, 33.42, 8.23, 34.5645, 23.5345), (89.43, 3.42, 3.23, 34.5645, 23.5345), (9.43, 2.42, 8.23, 34.5645, 23.5345), (9.43, 2.42, 8.23, 34.5645, 23.5345), (9.43, 2.42, 8.23, 34.5645, 23.5345), (9.43, 2.42, 8.23, 34.5645, 23.5345)], dtype=my_dtype)

# with open("drone.jpg", "rb") as img_file:
#     image_enc = base64.b64encode(img_file.read())

TXdata = []

for _ in range(10):
    TXdata.append(data)

# TXdata.append(image_enc)

drone(TXdata, dst_add, dev_add, max_packet_len, d)
