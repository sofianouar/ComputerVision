import cv2
import manip as m

if __name__ == '__main__':
    # Créer une instance de classe manip
    composed_image = m.manip()

    """
        Part1
    """
    message = input('Veuillez entrer le message à coder: ')
    image_name = input('Veuillez entrer le nom de l\'image dont laquelle vous\
    voulez mettre le message(avec extension): ')
    image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    # Lancer le codage
    composed_image.codeMessage(message, image)
    final_image_name = input('Sous quel nom vous voulez sauvegarder l\'image\
    (Sans extension): ')
    cv2.imwrite('{}.png'.format(final_image_name),
                composed_image.image_with_message)

    """
        Part2
    """
    image_name = input('Veuillez entrer le nom de l\'image contenant le message\
     secret(Avec extension): ')
    new_image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    composed_image.uncodeMessage(new_image)
    # Afficher le message codé
    print(composed_image.decoded_message)
