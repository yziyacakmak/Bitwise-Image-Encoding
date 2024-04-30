import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

#Read Images from /images path
def read_images(image_name1,image_name2):
    image_folder = 'images/'
    image1_path = os.path.join(image_folder, image_name1)
    image2_path = os.path.join(image_folder, image_name2)
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path)
    image1_size = image1.shape[:2]
    image2_resized = cv2.resize(image2, (image1_size[1], image1_size[0]))
    return image1,image2_resized


#Set LSB 2 bits to 0 of rgb image
def LSB_2_bit_to_0(image):
    #1100 1111 0xCF 
    # temp=cv2.bitwise_and(image, np.array([0xCF, 0xCF, 0xCF], dtype=np.uint8))
    temp=cv2.bitwise_and(image, np.array([0xFC, 0xFC, 0xFC], dtype=np.uint8))
    return temp

#Take MSB 6 bits of gray scaled image
#Encode image with gray scaled image
def encode_image(message_image,encoding_image):
    MSB_head_mask=0xC0
    MSB_middle_mask=0x30
    MSB_tail_mask=0xC
    
    shift_head= 6 #6   #0xCF ise 2
    shift_middle=4#4  #0xCF ise 0
    shift_tail=2 #2    #0xCF ise 2 ama sola otele

    and1=cv2.bitwise_and(message_image,MSB_head_mask)
    filter1=and1 >> shift_head

    and2=cv2.bitwise_and(message_image,MSB_middle_mask)
    filter2= and2 >> shift_middle

    and3=cv2.bitwise_and(message_image,MSB_tail_mask)
    filter3= and3 >> shift_tail  #and3>>shift_tail   #0xCF ise sola oteleme

    r_channel = encoding_image[:, :, 2]
    g_channel = encoding_image[:, :, 1]  
    b_channel = encoding_image[:, :, 0]  

    r_cipher=cv2.bitwise_or(r_channel,filter1)
    g_cipher=cv2.bitwise_or(g_channel,filter2)
    b_cipher=cv2.bitwise_or(b_channel,filter3)

    cipher=cv2.merge((b_cipher, g_cipher, r_cipher))
    save_image(cipher,"cipherImage")
    return cipher


#Decode image 
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

    save_image(message_image,"message")

    return message_image



#Save image
def save_image(image,name):
    output_path = name+".jpg"
    cv2.imwrite(output_path, image)


#Print pixel values as binary
def print_binary_image(temp,shifted):
    height, width= temp.shape   #if the image has more than 1 channel than must be 3 return variables needed
    for i in range(height):
        for j in range(width):
            pixel_value1 = temp[i, j]
            pixel_value2=shifted[i,j]
            binary_value1 = np.binary_repr(pixel_value1,width=8)
            binary_value2 = np.binary_repr(pixel_value2,width=8)
            print(binary_value1)
            print(binary_value2)
            pass
    


def see_histogram(image1,image2):
    histogram1 = cv2.calcHist([image1], [0], None, [256], [0, 256])
    histogram2 = cv2.calcHist([image2], [0], None, [256], [0, 256])



    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].bar(range(256), histogram1[:,0], color='black')
    axes[0].set_title('Image1')
    axes[0].set_xlabel('Pixel Values')
    axes[0].set_ylabel('Pixel Count')

    # İkinci grafik paneline kümülatif histogramı çiz
    axes[1].bar(range(256), histogram2[:,0], color='black')
    axes[1].set_title('Image2')
    axes[1].set_xlabel('Pixel Values')
    axes[1].set_ylabel('Pixel Count')

    # Grafikleri göster
    plt.tight_layout()
    plt.show()