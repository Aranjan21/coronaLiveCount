from flask import Flask,render_template
from bs4 import BeautifulSoup
import requests
from flask import render_template

url = requests.get('https://ncov2019.live/').text
soup = BeautifulSoup(url, 'html.parser')

app = Flask(__name__)


from app import routes