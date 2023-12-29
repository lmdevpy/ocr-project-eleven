import json
from flask import Flask,render_template,request,redirect,flash,url_for, abort, session
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         date_now = datetime.now()
         for competition in listOfCompetitions:
             competition['date'] = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S" )
             competition['finished'] = competition['date'] < date_now
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("Invalid email adress")
        return render_template('index.html'), 401
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
    except IndexError:
        flash("club not found : please login again")
        return render_template('index.html'), 404
    try:
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash("competition not found")
        return render_template('welcome.html', club=club, competitions=competitions), 404
    if foundCompetition['finished']:
        flash("competition is finished")
        return render_template('welcome.html', club=club, competitions=competitions)
    return render_template('booking.html',club=foundClub,competition=foundCompetition)


@app.route('/purchasePlaces/',methods=['POST'])
def purchasePlaces():
    try:
        club = [c for c in clubs if c['name'] == request.form['club']][0]
    except IndexError:
        flash("Invalid club : please login again")
        return render_template('index.html'), 404
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    except IndexError:
        flash("Invalid competition")
        return render_template('welcome.html', club=club, competitions=competitions), 404
    placesRequired = int(request.form['places'])
    # club cannot use more than their points
    if placesRequired > 12 or placesRequired > int(club['points']):
        flash("Invalid number of places")
        return render_template('welcome.html', club=club, competition=competition)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash(f'booking completed! - {placesRequired} places reserved')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/displayPointsBoard/')
def displayPointsBoard():
    return render_template('display_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))