from flask import Flask, render_template, url_for, flash, redirect, request
from forms import *
from methods import *
import pandas as pd
import os

#---------IMPORTS^-----------------------------------------------------------------------------------------------------

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = '33b88069a6bf75538f1478eee983f497'

port = int(os.getenv('PORT', 5000))

#----------CONFIGURATIONS^----------------------------------------------------------------------------------------------------

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = MatchConditionsForm()
    if request.method == 'POST':
        pitch_type = form.pitch.data
        algo = form.algorithm.data
        return redirect(url_for('script', pitch_type = pitch_type, algo = algo))
    
    return render_template('home.html', title = "R.E.F.C - Home Page", form = form)

#----------HOME PAGE^----------------------------------------------------------------------------------------------------

@app.route("/about")
def about():
    return render_template('about.html', title = "R.E.F.C - About")

#----------ABOUT PAGE^----------------------------------------------------------------------------------------------------

@app.route("/contact")
def contact():
    return render_template('contact.html', title = "R.E.F.C - Contact Us")

#-----------CONTACT PAGE^---------------------------------------------------------------------------------------------------

@app.route("/script<pitch_type>,<algo>")
def script(pitch_type, algo):
    ptype = pitch_type

    if algo == "m1":
        
        if ptype == 'Green':
            players_green, sub_players_green = greenPitch()
            return render_template('result.html', title = "R.E.F.C - Result", method = algo, ptype = ptype, players = players_green, sub_players = sub_players_green)
            #return render_template('result.html', title = "Result", ptype = ptype, tables=[players_green.to_html(classes='data')], cols=players_green.columns.values)
    
        elif ptype == 'Dusty':
            players_dusty, sub_players_dusty = dustyPitch()
            return render_template('result.html', title = "R.E.F.C - Result", method = algo, ptype = ptype, players = players_dusty, sub_players = sub_players_dusty)
        
        elif ptype == 'Dead':
            players_dead, sub_players_dead = deadPitch()
            return render_template('result.html', title = "R.E.F.C - Result", method = algo, ptype = ptype, players = players_dead, sub_players = sub_players_dead)
        
        else:
            flash("Invalid Pitch Type!!", "danger")
            return render_template('home.html', title = "R.E.F.C - Home")
    
    elif algo == 'm2':

        if ptype == 'Green':
            players_green, sub_players_green = kmeans_green()
            return render_template('result.html', title = "R.E.F.C - Result", method = algo, ptype = ptype, players = players_green, sub_players = sub_players_green)
            #return render_template('result.html', title = "Result", method = algo, ptype = ptype, tables=[players_green.to_html(classes='data')], cols=players_green.columns.values)
        
        elif ptype == 'Dusty':
            players_dusty, sub_players_dusty = kmeans_dusty()
            return render_template('result.html', title = "R.E.F.C - Result", method = algo, ptype = ptype, players = players_dusty, sub_players = sub_players_dusty)

        elif ptype == 'Dead':
            players_dead, sub_players_dead = kmeans_dead()
            return render_template('result.html', title = "R.E.F.C - Result", method = algo, ptype = ptype, players = players_dead, sub_players = sub_players_dead)

    else:
        print("ALGORITHM:", algo)

#------------PITCH LOGIC^---------------------------------------------------------------------------------------------------------
'''
@app.route("/condition")
def condition():
    form = PitchForm()
    return render_template('condition.html', title = "Match Conditions", form = form)

@app.route("/result", methods=['GET', 'POST'])
def result():
    players = [{'name':'Sachin Tendulkar', 'role':'Batsman'}, {'name':'Virendra Sehwag', 'role':'Batsman'}, {'name':'R. Ashwin', 'role':'Bowler'}]
    return render_template('result.html', title = "Result Team", players = players)
'''
#------------PITCH LOGIC BACKUP^--------------------------------------------------------------------------------------------------

@app.route("/stats<player>,<role>,<ptype>,<method>")
def stats(player, role, ptype, method):
    player_name = player
    player_role = role
    pitch_type = ptype
    method = method

    description = player_stats(player_name, player_role, pitch_type, method)
    if description == False:
        flash("Performance data for '{}' is not available currently".format(player_name), "danger")
        return redirect(url_for('script', pitch_type = pitch_type, algo = method))
    elif description == 'invalid category':
        flash("Cannot get performance data. Invalid player category mentioned for '{}'".format(player_name), "danger")
        return redirect(url_for('script', pitch_type = pitch_type, algo = method))
    else:
        return render_template("player_stat.html", title = "Player Stats", player_name = player_name, description = description)

#------------STATS LOGIC^---------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=port)