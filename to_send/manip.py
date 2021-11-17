import numpy as np


class manip:
    """
        Cette Classe contient des méthodes qui permettent de cacher un message
        dans une image, ainsi que l'opértion inverse.

        ####Attributs####:
            # ascii_list: représente le message par une liste de codes ascii.
            # binary_list: représenter le message par une liste de chaines de
             caractères binaires.
            # image_with_message: Contient le résultat du codage.
            # stop_int: ASCII de stop_char.
            # stop_char: caractère de fin de chaine(pour permettre le décodage)
            # decoded_message: résultat du décodage.

        ####Fonctions####:

    """

    def __init__(self):
        self.ascii_list = list()
        self.binary_list = list()
        self.image_with_message = None
        self.stop_int = 248
        self.stop_char = '{:08b}'.format(248)
        self.decoded_message = str()

    # Convertir le message en ASCII puis en binaire
    def messageToBinary(self, message):
        # Coder le message en ASCII
        for char in message:
            self.ascii_list.append(ord(char))
        # Coder le message en binaire
        for number in self.ascii_list:
            self.binary_list.append('{:08b}'.format(number))

    # Changement de l'image en binaire
    def binaryImage(self, image):
        h, w = image.shape
        new_image = np.empty(image.shape, dtype='U8')
        for y in range(h):
            for x in range(w):
                # Forcer la représentation du pixel sur 8 bits
                new_image[y, x] = '{:08b}'.format(image[y, x])
        return new_image

    # Coder l'image en binaire
    def codeBinaryImage(self, image):
        h, w = image.shape
        y = 0
        x = 0
        element = 0
        char = 0
        end_of_message = False
        while y < h and not end_of_message:
            while x < w and not end_of_message:
                temp = image[y, x]
                temp_2 = self.binary_list[element]
                # Codage : 7 premiers bits du pixels et 1 du message
                image[y, x] = '{}{}'.format(temp[0:7], temp_2[char])
                char += 1
                # Vérifier si on doit passer vers le prochain
                # élémént du message
                if char == 8:
                    char = 0
                    element += 1
                # Vérifier si on est arrivé à la fin du message
                if element >= len(self.binary_list):
                    end_of_message = True
                x += 1
            y += 1

        return image

    # Créer l'image final
    def makeFinalImage(self, image):
        h, w = image.shape
        for y in range(h):
            for x in range(w):
                # Convertir une chaine en un entier
                self.image_with_message[y, x] = int('0b'+image[y, x], 2)

    # Cacher le message dans l'image
    def codeMessage(self, message, image):
        # Convertir le message en liste de chaines binaires
        self.messageToBinary(message)
        # Ajouter le caractère d'arret à la liste
        self.binary_list.append(self.stop_char)
        # Initialisation de l'attribut qui va contenir la nouvelle image
        self.image_with_message = np.zeros(image.shape, np.uint8)
        # Convertir les pixels de l'image d'origine en chaines binaires
        new_image = self.binaryImage(image)
        # Coder l'image binaire
        new_image_coded = self.codeBinaryImage(new_image)
        # Reconvertir les pixels en entiers
        # Le résultat va etre contenu dans l'attribut 'image_with_message'
        self.makeFinalImage(new_image_coded)

    # Obtenir le message à partir d'une image
    def uncodeMessage(self, image):
        # Sofia's part
        binary_image = self.binaryImage(image)
        self.getMessageFromImage(binary_image)

    def getMessageFromImage(self, image):
        check_step = 0
        h, w = image.shape
        message = ''
        binary_char = ''
        for y in range(h):
            for x in range(w):
                pix = image[y, x]
                # récupérer le dernier bit du pixel courant
                binary_char = binary_char + pix[-1]
                check_step += 1
                # Vérifier i on a lu 8 Bits
                if check_step == 8:
                    # Convertir une chaine binaire en entier(ASCII)
                    temp = int('0b'+binary_char, 2)
                    # Vérifier si le caractère lu est un caractère d'arret
                    if temp == self.stop_int:
                        break
                    else:
                        # Ajouter le caractère lu dans le message
                        message += chr(temp)
                        # Réinitialisation des du temporaire(binary_char) de
                        # l'itérateur check_step
                        binary_char = str()
                        check_step = 0
            if temp == self.stop_int:
                break
        # Validation : Mettre à jour l'objet de classe manip
        self.decoded_message = message
