from PySide6.QtWidgets import (QApplication,QWidget,QTextEdit,QPushButton,QComboBox,QFileDialog)

from threading import Thread

from pytube import YouTube

class YtDowdloander(Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)

    def start(self,links, file, method, resolution) -> None:
        self.links = links
        self.file = file
        self.method = method
        self.resolution = resolution

        return super().start()


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

class Window(QWidget):
    yt = YtDowdloander()
    
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
        self.resolutionOptions.setToolTip('Jakość wideo.')

        self.convertOptionsBox = QComboBox(self)
        self.convertOptionsBox.resize(100,30)
        self.convertOptionsBox.move(400,370)
        self.convertOptionsBox.addItems( ['Dźwięk','Wideo'] )
        self.convertOptionsBox.setToolTip('Co pobrać?')

        self.convertButton = QPushButton(self,text='Konwertuj')
        self.convertButton.resize(100,30)
        self.convertButton.move(500,370)
        self.convertButton.clicked.connect(self.dowdloand)

    def paintEvent(self,e):
        option = self.convertOptionsBox.currentText()

        match option:
            case 'Dźwięk':
                self.resolutionOptions.setDisabled(True)
            case 'Wideo':
                self.resolutionOptions.setEnabled(True)

        if self.yt.is_alive():
            self.convertButton.setDisabled(True)
            self.convertOptionsBox.setDisabled(True)

        else:
            self.yt = YtDowdloander()
            self.convertButton.setEnabled(True)
            self.convertOptionsBox.setEnabled(True)

    def getLinks(self):
        text = self.textEdit.toPlainText()
        links = text.splitlines()

        return links

    def dowdloand(self):
        links = self.getLinks()
        file = QFileDialog.getExistingDirectory()

        method = self.convertOptionsBox.currentText()
        resolution = self.resolutionOptions.currentText()

        self.yt.start(links,file, method, resolution)


if __name__ == '__main__':
    app = QApplication()
    
    ws = Window()
    ws.show()
    
    app.exec()