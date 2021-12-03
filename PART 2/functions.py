import cv2
import numpy as np


####          ETAPE 1
'''
return une matrice (Nx3) qui représente les positions des sources lumineuses 
(chaque ligne représente une position x,y,z)
'''

def load_lightSources():

	pass

'''
return une matrice (N*3) qui représente les 
intensités des sources lumineuses (chaque ligne représente l’intensité d’un pixel R,G,B).
'''
def load_intensSources():
	return 

'''
3- Créer une fonction load_objMask qui retourne une matrice (image) binaire tel que :
1 représente un pixel de l’objet et 0 : un pixel du fond.
'''
def load_objMask():
	pass

'''
permet de charger les N images, les traiter et retourner une matrice N * (h*w)

'''
def load_images():
	#charger les noms des N images
	with open('data//filenames.txt') as f:
		names = f.read().splitlines()

	#charger une image et la traiter
	for i in range(1):
		image_name='data/objets/'+names[i]
		image = cv2.imread(image_name,cv2.IMREAD_UNCHANGED)

		#verifier si l'image n'est pas vide
		if image is None :
			print('erreur ')
			exit(0)		

		#normaliser les valeurs entre [0,1]
		imgNorm=Normaliser(image)
	
		#Diviser chaque pixel sur l’intensité de la source (B/intB, G/intG, R/intR)
		imgNorm=divide_intensSources(imgNorm)

		#Convertir les images en niveau de gris (NVG = 0.3 * R + 0.59 * G + 0.11 * B) .
		#Redimensionner l’image telle que chaque image est représentée dans une seule ligne.
		#Ajout des img dans un tableau (pour former une matrice de N lignes et (h*w) colonnes où chaque ligne représente une image).
    #Retourner la matrice des images

	cv2.imshow('image',image)
	cv2.imshow('imgNorm',imgNorm)
	cv2.waitKey()
	cv2.destroyAllWindows()
	return

def Normaliser(image):
		imgNorm=image.astype(np.float32)
		imgNorm/=65535

		return imgNorm

def divide_intensSources(image):

	pass



####     ETAPE 2



if __name__ == '__main__':
	load_images()