from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from typing import List
import copy

app = FastAPI()

with open('dino_rhyme.html', 'r') as fd:
    dino_rhyme_html = fd.read()
with open('mystery_museum.html', 'r') as fd:
    mystery_museum_html = fd.read()
with open('furry_scaly_pets.html', 'r') as fd:
    furry_scaly_pets_html = fd.read()

madlibsDB = dict()
# 3 mad-libs
madlibsDB['dino_rhyme'] = dict()
madlibsDB['mystery_museum'] = dict()
madlibsDB['furry_scaly_pets'] = dict()
# mad-lib: Dino Rhymes
madlibsDB['dino_rhyme']['title'] = "Dinosaur Rhymes"
madlibsDB['dino_rhyme']['HTML'] = dino_rhyme_html
madlibsDB['dino_rhyme']['adjectives'] = ['long', 'exciting', 'amazing', 'sharp', 'golden', 'silly', 'difficult', 'warm', 'ridiculous', 'delightful', 'tired', 'weepy']
madlibsDB['dino_rhyme']['nouns'] = ['basketball', 'butterfly', 'corn', 'firetruck', 'globe', 'newspaper', 'orange slice', 'owl', 'palm-tree', 'rhino', 'superhero', 'train']
madlibsDB['dino_rhyme']['verbs'] = ['dig', 'zip', 'slurp', 'scratch', 'clap', 'sail', 'dance', 'gallop', 'blink', 'tango', 'chew', 'pedal']
madlibsDB['dino_rhyme']['miscellanies'] = ['banana', 'bread', 'celery', 'cookies', 'deer', 'dice', 'eagle', 'hat', 'moon', 'plant', 'surfer', 'trumpet']
# mad-lib: Mystery Museum
madlibsDB['mystery_museum']['title'] = "Museum Mystery"
madlibsDB['mystery_museum']['HTML'] = mystery_museum_html
madlibsDB['mystery_museum']['adjectives'] = ['sticky', 'bumpy', 'slimy', 'charming', 'bouncy', 'tall', 'happy', 'wiggly', 'stylish', 'ripe', 'weird', 'wrinkly']
madlibsDB['mystery_museum']['nouns'] = ['canoe', 'castle', 'clown', 'elephant', 'fish', 'flowers', 'knight', 'parrot', 'pirate', 'soccerball', 'tortoise', 'unicorn', ]
madlibsDB['mystery_museum']['verbs'] = ['skipped', 'burped', 'jogged', 'yelled', 'scrambled', 'rolled', 'walked', 'rode', 'dribbled', 'wobbled', 'jumped', 'sang']
madlibsDB['mystery_museum']['miscellanies'] = ['bat', 'beaker', 'caterpillar', 'dinosaur', 'dolphin', 'frog', 'kid', 'Little Red Riding Hood', 'eel', 'piano', 'present', 'rocks']
# mad-lib: Furry Scaly Pets
madlibsDB['furry_scaly_pets']['title'] = "Quiz: Furry or Scaly Pets"
madlibsDB['furry_scaly_pets']['HTML'] = furry_scaly_pets_html
madlibsDB['furry_scaly_pets']['adjectives'] = ['crunchy', 'dry', 'prickly', 'cuddly', 'sweaty', 'slow', 'quiet', 'hot', 'fresh', 'friendly']
madlibsDB['furry_scaly_pets']['nouns'] = ['apple', 'cat', 'Dragon', 'flamingo', 'football', 'Lion', 'Pinnoccio', 'Snorkler', 'tree', 'UFO']
madlibsDB['furry_scaly_pets']['verbs'] = ['smell', 'fetch', 'love', 'call', 'type', 'drip', 'catch', 'yawn', 'whistle', 'cry']
madlibsDB['furry_scaly_pets']['miscellanies'] = ['astronaut', 'cake', 'car', 'dragon', 'grapes', 'guitar', 'potion', 'robot', 'teapot']

@app.get('/')
async def root():
    return HTMLResponse("<h2>Marvellous Mavericks Make Methodical Mad-Libs</h2>")

@app.get('/madlibs/{name}')
async def getMadLib(name: str, q: List[str] = Query(default=[])):
    payload = dict()
    madlib = madlibsDB.get(name, None)
    if madlib:
        payload['title'] = madlib['title']
        payload['HTML'] = madlib['HTML']
    if q:
        for key in q:
            if key in ['adjectives', 'nouns', 'verbs', 'miscellanies']:
                payload[key] = madlib[key]
    
    return payload































'''
@app.get('/madlib/{name}')
async def getMadLib(name: str, q: List[str] = Query(default=[])):
    payload = dict()
    madlib = madlibsDB.get(name, None)
    if not madlib:
        return
    payload['title'] = madlib.get('title')
    payload['HTML'] = madlib.get('HTML')

    if q:
        for key in q:
            if key in ['adjectives', 'nouns', 'verbs', 'miscellanies']:
                payload[key] = madlib[key] 

    return payload
'''
