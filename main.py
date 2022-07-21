from PySide6.QtWidgets import QApplication,QWidget,QTextEdit,QPushButton,QComboBox,QFileDialog,QMessageBox

from threading import Thread

from pytube import YouTube

class Window(QWidget):
    CovertOptions = [
        'mp4','mp3'
    ]
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YT Converter')
        self.setFixedSize(600,400)

        self.textEdit = QTextEdit(self)
        self.textEdit.resize(600,370)
        self.textEdit.setToolTip('Wprowadź tu linki do pobrania.\nKażdy w odzielnej linii.')

        self.resolutionOptions = QComboBox(self)
        self.resolutionOptions.resize(100,30)
        self.resolutionOptions.move(300,370)
        self.resolutionOptions.addItems( ['Wysoka', 'Niska'] )
        self.resolutionOptions.setToolTip('Jakość filmu.')

        self.convertOptionsBox = QComboBox(self)
        self.convertOptionsBox.resize(100,30)
        self.convertOptionsBox.move(400,370)
        self.convertOptionsBox.addItems( ['mp3','mp4'] )
        self.convertOptionsBox.setToolTip('Rozszerzenie pliku.')

        self.convertButton = QPushButton(self,text='Konwertuj')
        self.convertButton.resize(100,30)
        self.convertButton.move(500,370)
        self.convertButton.clicked.connect(self.dowdloand)

    def paintEvent(self,e):
        option = self.convertOptionsBox.currentText()

        match option:
            case 'mp3':
                self.resolutionOptions.setDisabled(True)
            case 'mp4':
                self.resolutionOptions.setEnabled(True)

    def getLinks(self):
        text = self.textEdit.toPlainText()
        links = text.splitlines()

        return links

    def dowdloand(self):
        links = self.getLinks()
        file = QFileDialog.getExistingDirectory()

        method = self.convertOptionsBox.currentText()
        resolution = self.resolutionOptions.currentText()

        yt = YtDowdloander(links,file, method, resolution)
        yt.start()

class YtDowdloander(Thread):
    def __init__(self, links, file, method, resolution) -> None:
        super().__init__(daemon=True)

        self.links = links
        self.file = file
        self.method = method
        self.resolution = resolution

    def run(self) -> None:
        for link in self.links:

            yt = YouTube(link)

            match self.method:
                case 'mp4':
                    match self.resolution:
                        case 'Wysoka':
                            data = yt.streams.get_highest_resolution()

                        case 'Niska':
                            data = yt.streams.get_lowest_resolution()

                case 'mp3':
                    data = yt.streams.get_audio_only()
                    
            data.download(self.file)

    def __del__(self):
        info = QMessageBox()
        info.setWindowTitle('YT Converter')
        info.setText('Pobieranie zakończone')
        info.setIcon(QMessageBox.Information)
        info.exec()

if __name__ == '__main__':
    app = QApplication()
    
    ws = Window()
    ws.show()
    
    app.exec()