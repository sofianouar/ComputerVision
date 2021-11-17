import PyQt5.QtWidgets as w
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import os
import cv2
import manip as m
import time


class MainWindow(w.QWidget):
    def __init__(self):
        super().__init__()
        # Ajouter un titre à la fenetre
        self.setWindowTitle('Projet Vision')
        self.setUpLayout()
        self.createComponents()
        self.setUpComponents()
        self.show()
        # Initialiser les attributs de classe
        self.pwd = None
        self.image_before = None
        self.image_after = None

    def setUpComponents(self):
        self.layout().addWidget(self.hello_label)
        self.layout().addWidget(self.part_chooser_ComboBox)
        self.layout().addWidget(self.choose_file_PushButton)
        self.layout().addWidget(self.message_LineEdit)
        self.layout().addWidget(self.launch_PushButton)
        self.layout().addWidget(self.save_PushButton)
        self.layout().addWidget(self.visualisation_PushButton)
        self.layout().addWidget(self.progressBar)
        self.layout().addWidget(self.hint_label)

        # Set up Labels
        self.hint_label.setSizePolicy(
            w.QSizePolicy.Expanding, w.QSizePolicy.Expanding)
        self.hint_label.setAlignment(core.Qt.AlignCenter)
        self.hint_label.setStyleSheet("QLabel {color: red;}")

        self.hello_label.setSizePolicy(
            w.QSizePolicy.Expanding, w.QSizePolicy.Expanding)
        self.hello_label.setAlignment(core.Qt.AlignCenter)
        self.hello_label.setStyleSheet(
            "QLabel {color: white; background-color: black;}")

        # Setup Buttons
        self.save_PushButton.setMinimumHeight(90)
        self.choose_file_PushButton.setMinimumHeight(90)
        self.visualisation_PushButton.setMinimumHeight(90)
        self.launch_PushButton.setMinimumHeight(90)

        # Setup QComboBox
        self.part_chooser_ComboBox.setMinimumHeight(30)

        # Setup LineEdits
        self.message_LineEdit.setPlaceholderText("Message")
        self.message_LineEdit.setMinimumHeight(40)

        # Setup the progressbar
        self.progressBar.setValue(0)
        self.progressBar.setMinimumHeight(50)

    def createComponents(self):
        self.createLabels()
        self.createTextEdit()
        self.createButtons()
        self.createComboBoxes()
        self.createProgressBar()

    def setUpLayout(self):
        self.setLayout(w.QVBoxLayout())

    def createProgressBar(self):
        self.MAXSTEP = 500
        self.progressBar = w.QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(self.MAXSTEP)

    def createTextEdit(self):
        self.message_LineEdit = w.QLineEdit()
        self.message_LineEdit.setObjectName("message_field")
        self.message_LineEdit.setText("")

    def createComboBoxes(self):
        self.part_chooser_ComboBox = w.QComboBox(self)
        self.part_chooser_ComboBox.addItem("cacher un message dans une photo")
        self.part_chooser_ComboBox.addItem(
            "Extraire un message à partir d'une photo")

    def createButtons(self):
        self.choose_file_PushButton = w.QPushButton(
            "   Choisir une photo", clicked=lambda: self.chooseImage())
        self.choose_file_PushButton.setFont(gui.QFont('Helvetica', 12))
        try:
            self.choose_file_PushButton.setIcon(gui.QIcon('logos/choisir.png'))
            self.choose_file_PushButton.setIconSize(core.QSize(60, 60))
        except FileNotFoundError:
            pass

        self.launch_PushButton = w.QPushButton(
            "Lancer", clicked=lambda: self.launchOperation())
        self.launch_PushButton.setFont(gui.QFont('Helvetica', 12))

        try:
            self.launch_PushButton.setIcon(gui.QIcon('logos/start.png'))
            self.launch_PushButton.setIconSize(core.QSize(60, 60))
        except FileNotFoundError:
            pass

        self.visualisation_PushButton = w.QPushButton(
            "   Visualiser", clicked=lambda: self.visualisationMethod())
        self.visualisation_PushButton.setFont(gui.QFont('Helvetica', 12))

        try:
            self.visualisation_PushButton.setIcon(gui.QIcon('logos/vis.png'))
            self.visualisation_PushButton.setIconSize(core.QSize(100, 100))
        except FileNotFoundError:
            pass

        self.save_PushButton = w.QPushButton(
            "   Sauvegarder", clicked=lambda: self.saveButton())
        self.save_PushButton.setFont(gui.QFont('Helvetica', 12))

        try:
            self.save_PushButton.setIcon(gui.QIcon('logos/save.png'))
            self.save_PushButton.setIconSize(core.QSize(50, 50))
        except FileNotFoundError:
            pass

    def createLabels(self):
        self.acceptDrops()
        self.hello_label = w.QLabel("Bienvenu! Veuillez choisir \
une opération à faire.")
        self.hello_label.setFont(gui.QFont('Helvetica', 18))

        self.hint_label = w.QLabel('')

    # Visualiser les images(avant et après modification)

    def visualisationMethod(self):
        if self.part_chooser_ComboBox.currentIndex() == 0:
            try:
                assert self.image_before is not None
                assert self.image_after is not None
                cv2.imshow('Image avant modification', self.image_before)
                cv2.imshow('Image apres modification', self.image_after)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except TypeError:
                self.hint_label.setText('You should select an image')
            except AssertionError:
                self.hint_label.setText(
                        "Vous devez choisir une image et lancer le traitement")
        else:
            try:
                assert self.image_before is not None
                cv2.imshow('Image contenant le text cache', self.image_before)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except TypeError:
                self.hint_label.setText('You should select an image')
            except AssertionError:
                self.hint_label.setText("Vous devez choisir une image")

    # Ouvrir un selectionneur d'image
    def chooseImage(self):
        self.image_before = None
        self.image_after = None
        file_filter = 'Image (*.jpeg *.jpg *.png)'
        pwd = w.QFileDialog.getOpenFileName(
            parent=self,
            caption='Selectionner une image',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter
        )
        self.image_before = cv2.imread(pwd[0], cv2.IMREAD_GRAYSCALE)
        self.pwd = pwd[0]

    # Lancement de l'opération
    def launchOperation(self):
        # Initialiser la barre de progression
        self.progressBar.setValue(0)
        if self.pwd is None:
            self.hint_label.setText('Vous devez selectionner une image avant')
        else:
            self.progressInProgressBar(62)
            composed_image = m.manip()
            self.progressInProgressBar(62)
            if self.part_chooser_ComboBox.currentIndex() == 0:
                try:
                    self.progressInProgressBar(62)
                    assert self.message_LineEdit.text()
                    self.progressInProgressBar(62)
                    self.image_before = cv2.imread(
                        self.pwd, cv2.IMREAD_GRAYSCALE)
                    self.progressInProgressBar(62)
                    composed_image.codeMessage(
                        self.message_LineEdit.text(), self.image_before)
                    self.progressInProgressBar(62)
                    self.image_after = composed_image.image_with_message
                    self.progressInProgressBar(62)
                    self.hint_label.setText("Done!")
                    self.progressInProgressBar(66)
                except AssertionError:
                    self.hint_label.setText("Vous devez entrer un message!")
            else:
                try:
                    self.progressInProgressBar(62)
                    assert self.pwd is not None
                    self.progressInProgressBar(62)
                    self.image_before = cv2.imread(
                        self.pwd, cv2.IMREAD_GRAYSCALE)
                    self.progressInProgressBar(62)
                    composed_image.uncodeMessage(self.image_before)
                    self.progressInProgressBar(62)
                    self.message_LineEdit.setText(
                        composed_image.decoded_message)
                    self.progressInProgressBar(62)
                    self.hint_label.setText("Done!")
                    self.progressInProgressBar(66)
                except AssertionError:
                    self.hint_label.setText(
                        "Vous devez selectionner une image")

    def progressInProgressBar(self, value):
        for i in range(value):
            time.sleep(0.001)
            self.progressBar.setValue(self.progressBar.value()+1)

    def saveButton(self):
        file_filter = 'Image (*.png)'
        pwd = w.QFileDialog.getSaveFileName(
            parent=self,
            caption='Selectionner une image',
            directory='Coded_Image.png',
            filter=file_filter,
            initialFilter=file_filter
        )
        # self.image_before = cv2.imread(pwd[0], cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(pwd[0], self.image_after)
        self.pwd = pwd[0]


if __name__ == '__main__':
    application = w.QApplication([])
    mainWindow = MainWindow()
    application.exec()

    application.exec()
