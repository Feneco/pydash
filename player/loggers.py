# -*- coding: utf-8 -*-
"""
@author: Wagner C. C. Batalha (200044486@aluno.unb.br) 05/2023

@description: PyDash Project

Cuter, more intuitive and cleaner stdout logger for the project.

"""


from math import floor

class PlayerLogger:
    def __init__(self, maxBufferLength:int, maxRequestsQtd:int, maxQi:int, bufferBarLength:int=10, qualityBarLength:int=10):
        self.maxBufferLength= maxBufferLength
        self.maxQi = maxQi
        self.maxRequestsQtd = maxRequestsQtd
        self.bufferBarLength = bufferBarLength
        self.qualityBarLength = qualityBarLength

        self.bufLength = 0
        self.requestNumber = 0

        self._PercentPlayed = f"{0.0:3.0f}% downloaded" # So the first one doesn't come out bugged
        self._additionalMessage = ""
        self._playing = "stopped"
        self._qi = 0


    def addAdditionalMessage(self, message):
        self._additionalMessage += f"| {message} "

    def setBuffer(self, bufLength:int):
        self.bufLength = bufLength

    def setRequestNumber(self, requestNumber:int):
        self.requestNumber = requestNumber

    def _bar(self, x, maxValue, length, messageLow="", messageMax="", fullSymbol = '█', emptySymbol='░'):
        if x == maxValue:
            bar = f"{fullSymbol * (length - (len(messageMax)))}{messageMax}"
        elif x == 0:
            bar = f"{messageLow}{emptySymbol * (length - len(messageLow))}"
        else:
            fullSquareQtd = floor(x/maxValue * length)
            emptySquareQtd = length - fullSquareQtd
            bar = f"{fullSymbol * fullSquareQtd}{emptySymbol * emptySquareQtd}"
        return bar

    def _bufferBar(self) -> str:
        return f"buffer {self._bar(self.bufLength, self.maxBufferLength, self.bufferBarLength)} [{self.bufLength:2d}/{self.maxBufferLength:2d}]s"

    def _qualityBar(self) -> str:
        return f"Qi ({self._bar(self._qi, self.maxQi-1, self.qualityBarLength, fullSymbol='@', emptySymbol='~')}) [{self._qi:2d}/{self.maxQi-1:2d}]"

    def _getPercentPlayed(self) -> None:
        percent = self.requestNumber / self.maxRequestsQtd
        percent *= 100
        self._PercentPlayed = f"segments: {percent:3.0f}% downloaded"

    def setRequest(self, qi):
        self._qi = qi
        self.addAdditionalMessage(f"> request {self.requestNumber:d}: {self._qualityBar()}")

    def setResponse(self, number, throughput):
        self._getPercentPlayed()
        kbps = floor(throughput / 1000);
        self.addAdditionalMessage(f"< response {number:d}: Throughput = {kbps:d} kbps")

    def setPlaying(self):
        self._playing = "playing"
        self.addAdditionalMessage("video resumed")

    def setPaused(self):
        self._playing = "paused "
        self.addAdditionalMessage("video paused")

    def setStopped(self):
        self._playing = "stopped"
        self.addAdditionalMessage("video stopped")

    def render(self) -> str:

        retString = f"{self._playing} | {self._bufferBar()} | {self._PercentPlayed} {self._additionalMessage}"
        self._additionalMessage = ""
        return retString

    def log(self):
        print(self.render())


if __name__ == "__main__":
    l = PlayerLogger(60, 400, 30)
    l.setBuffer(35)
    l.setRequest(46, 23)
    print(l.render())

    l.setBuffer(34)
    print(l.render())

    l.setBuffer(0)
    l.setResponse(46, 640123)
    print(l.render())
