import cv2
import helpers as help




#image1 reads in Gray Scale 
#image2 reads in RGB

#Read the images
image1,image2=help.read_images("street.jpg","slainte.jpg")

#Set 0 to LSB 2 bits of rgb image
image2_zeros=help.LSB_2_bit_to_0(image2)

#Encode image
cipher_image=help.encode_image(image1,image2_zeros)

#Decode image
message_image=help.decode_image(cipher_image)


cv2.imshow('Cipher', cipher_image)

cv2.imshow('Message', message_image)

# help.see_histogram(image2,image2_zeros)


cv2.waitKey(0)
cv2.destroyAllWindows()


