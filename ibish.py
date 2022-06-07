# Filename: ibish.py

"""Ibish is a translator english words to ibish. 
Ibish is built using Python and PyQt5
"""

import sys

#Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from window import Ui_MainWindow
from hyphen import Hyphenator

__date___ = '05/31/22'
__author__ = 'Beatrice Bridge'

VOW = {'a', 'e', 'i', 'o', 'u'}
VOW_Y = {'a', 'e', 'i', 'o', 'u', 'y'}

#top-level function used to create Model
def _concatSyl(sylist):
        """Concatenate syllable translations of a word."""
        result = ""
        for syl in sylist:
            result += _translateSyl(syl) + "-"
        return result[0:-1:]

#top-level function used to create Model
def _translateSyl(str):
        """Translate one syllable to ibish."""

        def translateCon():
            """Translate a syllable starting with a consonant"""
            i = 1
            nonlocal first_sound
            while str[i] not in VOW and i < len(str):
               first_sound += str[i]
               i += 1

            return first_sound + "ibe-" + str[i::]

        first_sound = str[0]
        if first_sound in VOW:
            result = "ibe-" + str
        else:
            result = translateCon()
        return result

#top-level function used to create Model dictionary
def _load_words():
    """Load dictionary words from txt file.
    Source: https://github.com/dwyl/english-words.
    """
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

#VIEW/GUI made using Qt Designer
class MainWindow(QMainWindow):
    """Ibish main window and signals/slots."""
    def __init__(self):
        """Main window initializer"""
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._translate = translateWord
        self._connectSignals()
        
    def _connectSignals(self):
        """Connect signals and slots."""
        self.ui.pushButton.clicked.connect(self._onSubmit)
        self.ui.lineEdit.returnPressed.connect(self._onSubmit)
        self.ui.lineEdit.textEdited.connect(self._onEdit)

    def _onEdit(self):
        """Clear error messages and translation."""
        self.clearTranslationText()
        self.setErrorText('')

    def _onSubmit(self):
        """Submit for translation."""
        try:
            txt = self.getSearchText()
            if len(txt) > 0:
                result = self._translate(word=txt)
            else:
                raise ValueError("Error: Enter a word")
            
            self.setTranslationText(result)
        except ValueError as e:
            self.setTranslationText('')
            self.setErrorText(str(e))

    def setErrorText(self,text):
        """Set the error message text."""
        self.ui.lineEdit_3.setText(text)

    def setTranslationText(self,text):
        """Set the translation line edit's text"""
        self.ui.lineEdit_2.setText(text)
        
    def clearTranslationText(self):
        """Clear the translation line edit"""
        self.setTranslationText('')
        self.ui.lineEdit_2.setPlaceholderText('')

    def getSearchText(self):
        """Get the search line edit's text"""
        return self.ui.lineEdit.text()

# Create a Model to handle the translator's operations
def translateWord(word):
    """Translate a word to Ibish"""
    word = word.lower()
    english_words = _load_words()
    if word not in english_words:
        if ' ' in word:
            raise ValueError('Error: Remove Spaces')
        raise ValueError('Error: Invalid Word or Character')

    sylist = [word]
    if len(word) >= 4:
        hyp = Hyphenator('en_US')
        sylist = hyp.syllables(word)

    if len(sylist) < 1:
        raise ValueError('Error: Translation Not Found')

    result = _concatSyl(sylist)
    return result

#Client code
def main():
    """Main function."""
    app = QApplication(sys.argv)
    view = MainWindow()
    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()