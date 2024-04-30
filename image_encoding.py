import cv2
import helpers as help

#image1 reads in Gray Scale 
#image2 reads in RGB

#Read the images
message_image,encoding_image=help.read_images("slainte.jpg","wholefoods.jpg")

#Set 0 to LSB 2 bits of rgb image
encoding_image_zeros=help.LSB_2_bit_to_0(encoding_image)

#Encode image
cipher_image=help.encode_image(message_image,encoding_image_zeros)

#Decode image
decoded_image=help.decode_image(cipher_image)


cv2.imshow('Cipher', cipher_image)

cv2.imshow('Message', decoded_image)

help.see_histogram(encoding_image,encoding_image_zeros)


cv2.waitKey(0)
cv2.destroyAllWindows()


