import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

#resimleri oku
def read_images(image_name1,image_name2):
    image_folder = 'images/'
    image1_path = os.path.join(image_folder, image_name1)
    image2_path = os.path.join(image_folder, image_name2)
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path)
    image1_size = image1.shape[:2]
    image2_resized = cv2.resize(image2, (image1_size[1], image1_size[0]))
    # cv2.imshow('Resized Image2', image2_resized)
    # cv2.imshow('image1', image1)
    return image1,image2_resized


#en degersiz 2 biti 0 yap
def LSB_2_bit_to_0(image):
    temp=cv2.bitwise_and(image, np.array([0xFC, 0xFC, 0xFC], dtype=np.uint8))
    # cv2.imshow('temp', temp)
    return temp

#gray scale image'in en degerli 6 bitini al
def encode_image(message_image,encoding_image):
    MSB_head_mask=0xC0
    MSB_middle_mask=0x30
    MSB_tail_mask=0xC
    
    and1=cv2.bitwise_and(message_image,MSB_head_mask)
    filter1=and1 >> 6
    # print_binary_image(and1,filter1)

    and2=cv2.bitwise_and(message_image,MSB_middle_mask)
    filter2= and2 >> 4

    and3=cv2.bitwise_and(message_image,MSB_tail_mask)
    filter3= and3>>2

    r_channel = encoding_image[:, :, 2]
    g_channel = encoding_image[:, :, 1]  
    b_channel = encoding_image[:, :, 0]  

    r_cipher=cv2.bitwise_or(r_channel,filter1)
    g_cipher=cv2.bitwise_or(g_channel,filter2)
    b_cipher=cv2.bitwise_or(b_channel,filter3)

    cipher=cv2.merge((b_cipher, g_cipher, r_cipher))
    save_image(cipher,"cipherImage")
    return cipher

def decode_image(cipher_image):
    r_channel = cipher_image[:, :, 2]
    g_channel = cipher_image[:, :, 1]  
    b_channel = cipher_image[:, :, 0]  

    lsb_2_mask=0x3
    msb_head=cv2.bitwise_and(r_channel,lsb_2_mask)
    msb_middle=cv2.bitwise_and(g_channel,lsb_2_mask)
    msb_tail=cv2.bitwise_and(b_channel,lsb_2_mask)

    msb_head=msb_head<<6
    msb_middle=msb_middle<<4
    msb_tail=msb_tail<<2

    message_image=msb_head+msb_middle+msb_tail

    # cv2.imshow("message",message_image)

    save_image(message_image,"message")

    return message_image




def save_image(image,name):
    output_path = name+".jpg"
    cv2.imwrite(output_path, image)

def print_binary_image(temp,shifted):
    height, width= temp.shape   #ekstra bir return degeri daha olabilir renk kanali sayiisna gore
    # Her bir pikselin değerini bit olarak göster
    for i in range(height):
        for j in range(width):
            pixel_value1 = temp[i, j]
            pixel_value2=shifted[i,j]
            binary_value1 = np.binary_repr(pixel_value1,width=8)
            binary_value2 = np.binary_repr(pixel_value2,width=8) # Piksel değerini 8 bitlik binary formata dönüştür
            print(binary_value1)
            print(binary_value2)
            pass
    


def see_histogram(image1,image2):
    histogram1 = cv2.calcHist([image1], [0], None, [256], [0, 256])
    histogram2 = cv2.calcHist([image2], [0], None, [256], [0, 256])



    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    # Birinci grafik paneline histogramı çiz
    axes[0].plot(histogram1, color='black')
    axes[0].set_title('Image1')
    axes[0].set_xlabel('Piksel Değeri')
    axes[0].set_ylabel('Piksel Sayısı')

    # İkinci grafik paneline kümülatif histogramı çiz
    axes[1].plot(histogram2, color='black')
    axes[1].set_title('Image2')
    axes[1].set_xlabel('Piksel Değeri')
    axes[1].set_ylabel('Piksel Sayısı')

    # Grafikleri göster
    plt.tight_layout()
    plt.show()