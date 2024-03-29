from fastapi import FastAPI, Path, Query, Form, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Union
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import copy
import re

class MadLib(BaseModel):
    title: str
    HTML: str
    adjectives: List[str]
    nouns: List[str]
    verbs: List[str]
    miscellanies: List[str]

app = FastAPI()

async def CRUDForm(request: Request):
    form_data = await request.form()
    form_json = jsonable_encoder(form_data)
    
    all_keys = form_json.keys()
    
    madlib = MadLib(
        title = form_json["title"],
        HTML = form_json["madlib"],
        adjectives = [form_json[word_key] for word_key in all_keys if re.match('^adjective', word_key)],
        nouns = [form_json[word_key] for word_key in all_keys if re.match('^noun', word_key)],
        verbs = [form_json[word_key] for word_key in all_keys if re.match('^verb', word_key)],
        miscellanies = [form_json[word_key] for word_key  in all_keys if re.match('^miscellany',  word_key)]
    )

    print(madlib)
    return madlib

templates = Jinja2Templates(directory='templates')

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
async def root(request: Request):
    games = {k:v.get('title') for k, v in madlibsDB.items() if v.get('active', True)}
    print(games)
    return templates.TemplateResponse('landing.html', {
        "request": request,
        "games": games        
    })

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

@app.get('/madlibsgame/{name}')
async def getMadLibGame(request: Request, name: str):
    my_mad_lib = madlibsDB.get(name, None)
    if my_mad_lib and my_mad_lib.get('active', True):
        return templates.TemplateResponse('madlib.html', {'request': request, **my_mad_lib})

@app.get('/madlibsadd/')
async def getForm4CRUD():
    with open('templates/CreateRUD.html', 'r') as fd:
        CreateRUD_HTML = fd.read()
    return HTMLResponse(CreateRUD_HTML);

@app.post('/madlibsadd/')
async def postFormData(madlib: MadLib = Depends(CRUDForm)):
    mad_name = re.sub(r'\W+', '', madlib.title)
    mad_name = re.sub(r'\s+', '_', mad_name)
    madlibsDB[mad_name] = madlib.dict()

    return RedirectResponse('/madlibsgame/' + mad_name, status_code=status.HTTP_302_FOUND)

@app.get('/madlibsupdate/{name}')
async def updateForm4CRUD(request: Request, name: str):
    my_mad_lib = madlibsDB.get(name, None) 
    if my_mad_lib and my_mad_lib.get('active', True):
        return templates.TemplateResponse('CRUpdateD.html', {
            'request': request,
            'name': name,
            **my_mad_lib
        })
     
@app.post('/madlibsupdate/{name}')
async def putFormData(name: str, madlib: MadLib = Depends(CRUDForm)):
    madlibsDB[name] = dict()
    madlibsDB[name] = madlib.dict()

    return RedirectResponse('/madlibsgame/' + name, status_code=status.HTTP_302_FOUND)

@app.get('/madlibsdelete/{name}')
async def deleteForm4CRUD(request: Request, name: str):
    my_mad_lib = madlibsDB.get(name, None)
    if my_mad_lib and my_mad_lib.get('active', True):
        return templates.TemplateResponse('CRUDelete.html', {
            'request': request,
            'name': name,
            **my_mad_lib
        })

@app.post('/madlibsdelete/{name}')
async def delRecord(name: str):
    my_mad_lib = madlibsDB.get(name, None)
    if my_mad_lib:
        my_mad_lib['active'] = False
    return my_mad_lib