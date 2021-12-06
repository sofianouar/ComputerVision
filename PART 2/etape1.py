import cv2
import numpy as np 
from numpy import zeros,array
####          ETAPE 1

'''
return une matrice (Nx3) qui représente les positions des sources lumineuses 
'''
global allImages
def load_lightSources():
	#charger les sources lumineuses
	global lightSources
	lightSources=np.loadtxt('data/light_directions.txt')
	#print(lightSources)
	
	return lightSources


'''
return une matrice (N*3) qui représente les intensités des sources lumineuses (chaque ligne = intensité d’un pixel R,G,B).
'''
def load_intensSources():
	#charger les sources d'intensite
	global intensSources
	intensSources=np.loadtxt('data/light_intensities.txt')
	#print(intensSources)

	return intensSources

'''
fonction load_objMask qui retourne une matrice (image) binaire tel que 1=pixel de l’objet et 0=pixel du fond.
'''
def load_objMask():
	#chargement du mask dans la variable image
	image = cv2.imread('data/mask.png',cv2.IMREAD_UNCHANGED)
	#lecture du h,w et ignorer la valeur du 3 eme vecteur(rgb) avec *_
	h,w,*_= image.shape
		#h = image.shape[0]
		#w = image.shape[1]
	#creation d'une matrice vide objMask qui va contenir la nouvelle representation binaire du mask
	objMask=np.zeros((h,w))
	#parcourir les lignes et les colones
	for y in range(h):
		for x in range(w):
			#si un pixel != 0 (i.e : ce n'est pas le fond) donc on remplace par 1, sinon on le laisse a zero
			if(image[y,x]!=[0]):
				objMask[y,x]=1
		
	#print(objMask[200])
	return objMask

'''
permet de charger les N images, les traiter et retourner une matrice allImages de N * (h*w)
'''
def load_images():
	
	#charger les N images
	with open('data//filenames.txt') as f:
		names = f.read().splitlines()

	allImages=zeros(len(names))

	#parcourir les images et les traiter une a une
	for i in range(2):
		#lecture d'une image
		image_name='data/objets/'+names[i]
		image = cv2.imread(image_name,cv2.IMREAD_UNCHANGED)

		#verifier si l'image n'est pas vide
		if image is None :
			print('erreur ')
			exit(0)		

		####        traiement d'une image

		#a. Changer l’intervalle des valeurs de uint16 [0 , 2^16-1] à float32 [0 , 1]
		imgNorm=toFloat32(image)

		# charger l'intensite de la source
		load_intensSources()

		#b. Diviser chaque pixel sur l’intensité de la source (B/intB, G/intG, R/intR)
		divImg=divide_intensSources(imgNorm,i)

		#c. Convertir les images en niveau de gris (NVG = 0.3 * R + 0.59 * G + 0.11 * B) .
		gsImg=convertTo_grayscale(divImg)

		#d. Redimensionner l’image telle que chaque image est représentée dans une seule ligne.
		redimImg=redim_Image(gsImg)
		print(type(redimImg)) #<class 'numpy.ndarray'>
		#e. Ajouter les images dans un tableau (pour former une matrice de N lignes et (h*w) colonnes où chaque ligne représente une image).
		allImages[i]=redimImg
	print(allImages)

	#f. Retourner la matrice des images.
	return allImages


'''
les fonctions utilisees dans load_images
'''
#a. Changer l’intervalle des valeurs de uint16 [0 , 2^16-1] à float32 [0 , 1]
def toFloat32(image):
		imgNorm=image.astype(np.float32)
		imgNorm/=65535
		return imgNorm

#b. Diviser chaque pixel sur l’intensité de la source (B/intB, G/intG, R/intR)
def divide_intensSources(image,i):

	#lecture du vecteur 
	intensities=intensSources[i] # R G B 

	#lecture du h,w et la valeur du 3 eme vecteur(bgr) 
	h,w,*_= image.shape

	#parcourir les lignes et les colones
	for y in range(h):
		for x in range(w):
			image[y,x,0]/= intensities[2]  #B
			image[y,x,1]/=intensities[1]	 #G
			image[y,x,2]/=intensities[0]	 #R
	''' 
	cv2.imshow('image',image)
	cv2.waitKey()
	cv2.destroyAllWindows()
	'''
	
	return image

#c. Convertir les images en niveau de gris (NVG = 0.3 * R + 0.59 * G + 0.11 * B) .
def convertTo_grayscale(image):

	#lecture du h,w et la valeur du 3 eme vecteur(bgr) 
	h,w,*_= image.shape

	#creation de la matrice de sortie
	greyImg=np.zeros((h,w))

	#parcourir les lignes et les colones
	for y in range(h):
		for x in range(w):
			#					R						G					B	
			greyImg[y,x]=0.3 * image[y,x,2] + 0.59 * image[y,x,1] + 0.11 * image[y,x,0]
	
	return greyImg

#d. Redimensionner l’image telle que chaque image est représentée dans une seule ligne.
def redim_Image(image):
	return image.reshape(1,-1)

#e. Ajouter les images dans un tableau (pour former une matrice de N lignes et (h*w) colonnes où chaque ligne représente une image).
def regrouper_Images(image):

	pass




########### MAIN 
if __name__ == '__main__':
	load_images()