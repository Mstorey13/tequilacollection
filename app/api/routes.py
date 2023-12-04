from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Collection

api = Blueprint('api',__name__, url_prefix='/api')


# tequila_name, type, abv, region