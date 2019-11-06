# Project: Lyric Searching Engine
#### Course: IEORE4501_001
#### Group: CGTY

## What is it?
Have you ever come across with the situation that you could get a tune out of your head but couldn’t remember the song’s name except only a few words from it’s lyrics? Here is a tool to help with that desperate situation. Lyric Searching Engine is designed to get detailed information of songs with a few words from their lyrics. Besides than songs’ names and artists, you can get recommendations of fancy activities related to the song that you search.

## Main Features

#### Proximity search of songs according to input lyrics:
Input will be searched through the lyrics of the most up-to-date Top100 songs, and names of possible songs will be returned.
#### Detailed information of the song:
From the pop-up songs, more detailed information can be presented for the chosen one song.
* Youtube Video Viewing: A Youtube MV link can be displayed or an MV webpage can be opened in your default browser.
* Concert Information: Show information of recent concerts of the artist (time and location). It will also check if a concert will be held in desired city, and ticket purchase links will be available if so. If required, information can be sent to the input email address.
* Albums: Demonstrate information of all albums of the artist.
* Song Recommendation: Recommend a song similar in content and display its sentiment (joy, anticipation, sadness or fear).

## Installation Instruction
 - As this program is written in Python 3, please make sure a proper version of Python has been installed.
 - Download NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt to the same file with the Lyric Searching Engine.
 - See requirements.txt for all the Python packages needed.
 
## Run Instruction
 - Please make sure a stable Internet connection.
 - Both py and ipynb file can finish the lyric searching task, you can choose whichever you like.
 - For py, in the terminal, cd to the directory where you keep both 'NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt' and 'lyric_search_engine.py', then run 'python lyric_search_engine.py'.
 - For ipynb, execute 'run all cells' in jupyter notebook, then go to the very last cell to follow the instructions. 
 - Please type in a few words, phrases or sentences, whatever you can recall from the lyrics of the song you would like to search.
 - Remember that the song you search should be a latest popular song. Or you will get either no search result or a popular song that might not be the one you are looking for.
 
