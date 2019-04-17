#!/usr/bin/python

import os
import re
import psycopg2

conn = psycopg2.connect(database="manga", user="yoxzhang",
                        password="123456", host="localhost", port="5432")
print('Opened database successfully')


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
    sqlTemp = "insert into manga_name(dir, name) values ('{0}','{0}')"
    sql = sqlTemp.format(manga)
    cur.execute(sql)
    conn.commit()


def saveChapter(manga, chapter):
    chapterNumStr = re.findall(r'\d+', chapter)[0]
    chapNum = int(chapterNumStr)
    print('保存章节', chapNum)
    sqlTemp = "insert into manga_chapter(manga_id, chapter_number, dir) values ((select id from manga_name where name='{0}'), {1},'{2}')"
    sql = sqlTemp.format(manga, chapNum, chapter)
    cur.execute(sql)
    conn.commit()


def saveFileDir(manga, chapter, file):
    fileIndexStr = re.findall(r'(\(.*?\))', file)
    fileNum = 1
    if (len(fileIndexStr) > 0):
        fileNum = int(re.findall(r'\d+', fileIndexStr[0])[0])
    sqlTemp = "insert into manga_file(manga_id, chapter_id, file_number, dir) values ((select id from manga_name where name='{0}'), (select id from manga_chapter where dir='{1}'), {2}, '{3}')"
    sql = sqlTemp.format(manga, chapter, fileNum, file)
    cur.execute(sql)
    conn.commit()


def initDb():
    cur.execute('drop table  IF EXISTS manga_name;')
    cur.execute('drop table  IF EXISTS manga_chapter;')
    cur.execute('drop table  IF EXISTS manga_file;')
    conn.commit()
    cur.execute('CREATE TABLE manga_name('
                'id SERIAL,'
                'manga_size int,'
                'name char(50),'
                'dir char(50)'
                ');')
    cur.execute('CREATE TABLE manga_chapter('
                'id SERIAL,'
                'manga_id int,'
                'chapter_number int,'
                'chapter_size int,'
                'dir char(50)'
                ');')
    cur.execute('CREATE TABLE manga_file('
                'id SERIAL,'
                'manga_id int,'
                'chapter_id int,'
                'file_number int,'
                'dir char(50)'
                ');')
    conn.commit()


if __name__ == '__main__':
    cur = conn.cursor()
    initDb()
    iterMangas('../pic')
    print("Records created successfully")
    conn.close()
