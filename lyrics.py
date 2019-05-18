import lyricsgenius
import markovify
import os
import pronouncing

scrape_mode = False # use if scraping lyrics
numToScrape = 100 # number of songs to scrape
wordsInSentence = 8 # num of max words in a sentence

os.chdir(r'C:\Users\rauna\Documents\GitHub\RapLyricGenerator')  # set directory to be used

genius = lyricsgenius.Genius("F-vy2XhE-SntPk2wsqt-whOYRTURrSy4ucTCgcTsSTHeBBGRZB3A-QC-M_GlQ-VI")
genius.remove_section_headers = True
genius.skip_non_songs = True

allLyrics = open("Drake.txt", "r").read()
lyricsModel = markovify.NewlineText(allLyrics)

def getJaccardSim(str1, str2):  # Used from Medium Post (calculates similarity)
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def makeSentence():
    return lyricsModel.make_sentence(tries=100, max_words=wordsInSentence)

def scrape(artistName, genius, numToScrape): # scrapes lyrics
    artist = genius.search_artist(artistName, max_songs=100, sort="popularity")
    for i in range(numToScrape):
        with open('Drake.txt', 'a') as file:
            file.write(artist.songs[i].lyrics)

def createBarPair(bar, rhyme): # takes in a bar, and creates a rhyming pair
    barPair = []
    barPair.append(bar)
    for i in range(400):
        sentence = makeSentence()
        if(abs(countSyllables(sentence) - countSyllables(bar)) < 3):
            if(sentence.split()[-1].lower() in rhyme):
                barPair.append(sentence)
                return barPair
    return ''

def countSyllables(sentence): # counts syllables in a sentnece
    words = sentence.split()
    syllables = 0
    for word in words:
        table = str.maketrans(dict.fromkeys('!.,?;:)('))
        word = word.translate(table)
        try:
            pronunciation_list = pronouncing.phones_for_word(word)
            syllables += pronouncing.syllable_count(pronunciation_list[0])
        except Exception as e:
            continue
    return syllables

def createLinesAndRhymes():
    generatedLines = []
    while len(generatedLines) < 10:
        sentence = makeSentence()
        if(getJaccardSim(sentence, open("Drake.txt", "r").read()) > .001):
            generatedLines.append(sentence)

    rhymesForLines = []
    for bar in generatedLines:
        rhymesForLines.append(pronouncing.rhymes(bar.split()[-1]))

    return generatedLines, rhymesForLines

def getLines():
    generatedLines, rhymesForLines = createLinesAndRhymes()
    allLines = []
    for bar, rhyme in zip(generatedLines, rhymesForLines):
        barPair = createBarPair(bar, rhyme)
        if barPair:
            for line in barPair:
                allLines.append(line)
    return allLines

if scrape_mode is True:
    scrape("Drake", genius, numToScrape) # can change to any artist

lines = []
while(len(lines) < 1):
    lines = lines + getLines()

songStructure = 'c v c'
struc = songStructure.split()
print(struc)
