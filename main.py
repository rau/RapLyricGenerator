import lyricsgenius
import markovify
import os
import pronouncing

scrape_mode = False # use if scraping lyrics
numToScrape = 100 # number of songs to scrape
charsInSentence = 60 # num of max chars in a sentence

os.chdir(r'C:\Users\rauna\Desktop\RapLyricGenerator')  # set directory to be used

def getJaccardSim(str1, str2):  # Used from Medium Post (calculates similarity)
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def scrape(artistName, genius, numToScrape): # scrapes lyrics
    artist = genius.search_artist(artistName, max_songs=100, sort="popularity")
    for i in range(numToScrape):
        with open('Drake.txt', 'a') as file:
            file.write(artist.songs[i].lyrics)

def createBarPair(bar, rhymesForLines): # takes in a bar, and creates a rhyming pair
    barPair = bar + '\n'
    for i in range(400):
        sentence = lyricsModel.make_short_sentence(charsInSentence)
        if(abs(countSyllables(sentence) - countSyllables(bar)) < 3):
            if(sentence.split()[-1].lower() in rhymesForLines.get(bar)):
                barPair = barPair + sentence
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

genius = lyricsgenius.Genius("F-vy2XhE-SntPk2wsqt-whOYRTURrSy4ucTCgcTsSTHeBBGRZB3A-QC-M_GlQ-VI")
genius.remove_section_headers = True
genius.skip_non_songs = True

if scrape_mode is True:
    scrape("Drake", genius, numToScrape) # can change to any artist

allLyrics = open("Drake.txt", "r").read()
lyricsModel = markovify.NewlineText(allLyrics)

generatedLines = []
i = 0
while i < 10:
    sentence = lyricsModel.make_short_sentence(charsInSentence)
    if(getJaccardSim(sentence, open("Drake.txt", "r").read()) > .001):
        generatedLines.append(sentence)
        i = i + 1

rhymesForLines = {}
for bar in generatedLines:
    rhymesForLines[bar] = pronouncing.rhymes(bar.split()[-1])

with open('DrakeBars.txt', 'a') as file:
    for bar in generatedLines:
        barPair = createBarPair(bar, rhymesForLines)
        if barPair:
            file.write(barPair)
            file.write('\n')
