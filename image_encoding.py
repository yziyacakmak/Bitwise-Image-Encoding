import cv2
import helpers as help



#image1 grayscale olarak okunur
#image2 renkli olarak okunur
#image1 in en degerli 6 biti image2 nin rgb kanalarinin en degersiz 2 bitine yerlestirilir

#resimlerin okunmasi
image1,image2=help.read_images("street.jpg","slainte.jpg")

#renkli resmin rgb kanallarinin son 2 bitini 0la
image2_zeros=help.LSB_2_bit_to_0(image2)

#renkli resmin icine grayscale image i gizle
cipher_image=help.encode_image(image1,image2_zeros)

#resmi coz
message_image=help.decode_image(cipher_image)


cv2.imshow('Cipher', cipher_image)

cv2.imshow('Message', message_image)

# help.see_histogram(image2,image2_zeros)


cv2.waitKey(0)
cv2.destroyAllWindows()


