import os
import fnmatch
import random


class Server:
    extensions = ["*.mp3", "*.wav", "*.ogg", "*.flac"]

    def __init__(self, folder: str, play_mode: str, index: int, volume: float) -> None:
        self.play_mode = play_mode
        self.firstStart = True
        self.index = index
        self.volume = volume
        self.folder = folder
        self.playlist = Server.getPlayList(folder)
        self.endIndex = len(self.playlist)-1

        if self.endIndex < 0:
            raise RuntimeError("这个文件夹里没有歌曲")
        if index >= len(self.playlist) or index < 0:
            raise IndexError("Index out of range")

    def getPlayList(folder):
        playlist = []
        try:
            for filename in os.listdir(folder):
                for extension in Server.extensions:
                    if fnmatch.fnmatch(filename, extension):
                        playlist.append(filename)
        except FileNotFoundError:
            raise FileNotFoundError("这个文件夹不存在")

        return playlist

    def swap(self, index1, index2):
        temp = self.playlist[index1]
        self.playlist[index1] = self.playlist[index2]
        self.playlist[index2] = temp

    def pick(self):
        randIndex = random.randint(0, self.endIndex)
        self.swap(randIndex, self.endIndex)
        self.index = self.endIndex
        self.endIndex -= 1

    def drawlots(self):
        if self.endIndex >= 0:
            self.pick()
        else:
            self.endIndex = len(self.playlist)-1
            self.pick()

    def firstStartFunc(self):
        self.firstStart = False
        if self.play_mode == "random":
            self.swap(self.index, self.endIndex)
            self.index = self.endIndex
            self.endIndex -= 1

    def getNext(self):
        if self.firstStart:
            self.firstStartFunc()
        elif self.play_mode == "random":
            self.drawlots()
        elif self.play_mode == "loop":
            self.index += 1
            self.index %= len(self.playlist)

        return self.playlist[self.index]
