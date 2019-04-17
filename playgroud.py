#!/usr/bin/python

import os 
import re

def iterMangas(path):
    dirs = os.listdir(path)
    for manga in dirs:
        saveManga(manga)
        iterChapters(path, manga)

def iterChapters(path, manga):
    currentPath = path + '/' + manga
    dirs = os.listdir(currentPath)
    for chapter in dirs:
        saveChapter(manga, chapter)
        iterFiles(path, manga, chapter)

def iterFiles(path, manga, chapter):
    currentPath = path + '/' + manga + '/' + chapter
    dirs = os.listdir(currentPath)
    for file in dirs:
        saveFileDir(manga, chapter, file)

def saveManga(manga):
    print('保存漫画', manga)

def saveChapter(manga, chapter):
    chapterNumStr = re.findall(r'\d+', chapter)[0]
    chapNum = int(chapterNumStr)
    print('保存章节', chapNum)

def saveFileDir(manga, chapter, file):
    fileIndexStr = re.findall(r'(\(.*?\))', file)
    fileNum = 1
    if (len(fileIndexStr) > 0):
        fileNum = int(re.findall(r'\d+', fileIndexStr[0])[0])
    print('保存文件', fileNum, fileIndexStr)

if __name__=='__main__':
    iterMangas('pic')