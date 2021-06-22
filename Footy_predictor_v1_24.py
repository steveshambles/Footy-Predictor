"""
Footy Predictor V1.24
For English Premier League 2021\2022 season.
Freeware By steve shambles. June 2021
For Windows 7 and higher.

Blog:
stevepython.wordpress.com

Thanks to:
Image buttons - https://www.clickminded.com/button-generator/
PL data - https://www.football-data.co.uk/data.php
Except 1992-93 season, I made that.

Requirements:
--------------
pip3 install pillow
pip3 install pyautogui
pip3 install pyperclip

New in this version:
--------------------
todo: 
      test on linux. Not working with h2h, needs work.
      Update links to tables and form when season starts and site updated
      to 2021-2022season.

V1.24 PEP8 check, not great but fixed what I could.Linux test failed.
V1.20 Now supports leagues of up to 28 teams.
V1.19 Updated logo img and draw list rating.
V1.18 Updated champship and L2 teams and ratings
V1.17 Updated prem league teams, promotion relegation, updated pl ratings.
V1.16 Updated Tkinter code for best practice using tk.widget.
V1.15 Rmoved update news menu item and related function.
V1.14 Removed visit new blog menu item and function.
V1.13 Updated full PL results for 2020-2021 season
V1.12 code tidy, small fixes and improvements
V1.11 added copy text button for h2h
V1.10 Romoved rubbish prediction algo, start again, keep it simple.
V1.09 removed tons remmed out code.
V1.08 removed h2h history files
v1.07-removed fred
"""
import csv
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Combobox
import webbrowser as web

from PIL import Image, ImageTk
import pyautogui
import pyperclip


class Fp():
    """Variables, set at defaults for global use.
       Add Fp. to each var then its effectively global."""
    VAR = 0
    sb_but = ''
    spn_bx = 0
    ht_combo = False
    at_combo = False
    custom_league_in_use = False
    cstm_tm_file_name = 'English Premiership.txt'
    cstm_tm_ratings_file_name = ''
    cstm_league_name = 'English Premiership'
    number_of_teams_in_league = 20
    ratings_file_name = 'epl-ratings.txt'
    orig_ratings_file_name = 'epl-ratings'
    team_list_file_name = 'English Premiership.txt'
    premier = True
    championship = False
    league_one = False
    league_two = False
    h2h_wndw_is_open = False
    team_error = False


def create_pred_hist():
    """Create prediction history save file, if not already exist."""
    if not os.path.exists('footy-predictions.txt'):
        with open('footy-predictions.txt', 'w') as contents:
            contents.write('Footy Predictor V1.24 Predictions History\n'
                           + '-' * 41 + '\n')


def new_hist_file():
    """Erase history text file."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to erase\n'
                                 'all previously saved predictions?')
    if ask_yn is False:
        return

    with open('footy-predictions.txt', 'w') as contents:
        contents.write('Footy Predictor V1.24 Predictions History\n'
                       + '-' * 41 + '\n')
    messagebox.showinfo('Reset',
                        '\n\nPredictions history file reset\n\n')


# Create new prediction history file if none found.
create_pred_hist()


# Set up main window.
root = tk.Tk()
root.title('Footy Predictor V1.24 - June 2021')
root.resizable(False, False)


# Insert logo.
logo_frame = tk.LabelFrame(root)
logo_frame.grid(padx=8, pady=8)
logo_image = Image.open('images/fp-logo-2021-2022.png')
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid(padx=2, pady=2, row=0, column=0)

"""This list is in relation and order of the teams list,
   and is used to calc the amount of goals
   scored in a predicted drawn match, for now, the away
   teams record is ignored. So ifthe first team in the list
   is a predicted draw then it will be a 1-1 draw (first item is a 1)."""
Fp.common_draws = [1, 1, 2, 0, 2, 1, 1, 1, 2, 1,
                   0, 1, 1, 1, 2, 2, 2, 0, 0, 1,
                   0, 0, 0, 0, 0, 0, 0, 0]
"""The extra 8 digits on end are to allow for up to 28 team custom leagues.
   This data will be refined a lot more over time.just starting out.
   If instead the score is randomly chosen for a draw then different
   result predictions will be shown for same fixture."""

Fp.predicted_score = ''


def about_menu():
    """About program menu text."""
    messagebox.showinfo('Program Information', 'Footy Predictor V1.24\n'
                        'June 2021\n\n'
                        'Freeware. By Steve Shambles.\n')


def help_menu():
    """How to use the program menu help text."""
    web.open(r'help\fp-help.txt')


def visit_blog():
    """Visit my old python blog."""
    web.open('https://stevepython.wordpress.com/')


def exit_app():
    """Yes-no requestor to exit program."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to\n'
                                 'quit Footy Predictor?')
    if ask_yn is False:
        return

    root.destroy()
    sys.exit()


def pred_hist():
    """View history file with systems default text viewer."""
    web.open('footy-predictions.txt')


def view_pl_stats():
    """Open web browser to see current team and player stats."""
    web.open('https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats')


def view_pl_data():
    """Open web browser to see epl historical data."""
    web.open('https://www.football-data.co.uk/data.php')


def view_results_fixtures():
    """Open web browser to see epl results and fixtures."""
    web.open(
        'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures')


def view_odds():
    """Open web browser to see current team and player stats."""
    same_team_check()
    if Fp.team_error:
        Fp.team_error = False
        return

    if Fp.championship:
        web.open(
            'http://odds.bestbetting.com/football/england/english-football-league-championship/?showMostPopular=true')
        return
    if Fp.league_one:
        web.open(
            'http://odds.bestbetting.com/football/england/english-football-league-one/?showMostPopular=true')
        return
    if Fp.league_two:
        web.open(
            'http://odds.bestbetting.com/football/england/english-football-league-two/?showMostPopular=true')
        return
    if Fp.premier:
        web.open(
            'http://odds.bestbetting.com/football/england/english-premier-league/?showMostPopular=true')
        return

    web.open('http://odds.bestbetting.com/')


def view_championship_table():
    """Open web browser to see current championship table, stats and form."""
    web.open('https://fbref.com/en/comps/10/Championship-Stats')


def view_league_one_table():
    """Open web browser to see current league one table, stats and form."""
    web.open('https://fbref.com/en/comps/15/League-One-Stats')


def view_league_two_table():
    """Open web browser to see current league two table, stats and form."""
    web.open('https://fbref.com/en/comps/16/League-Two-Stats')


def donate_me():
    """In the vain hope someone generous likes this program enough to
       reward my work."""
    web.open("https:\\paypal.me/photocolourizer")


def contact_me():
    """Send author email from contacts page of blog."""
    web.open('https://stevepython.wordpress.com/contact')


def h2h_help():
    """Load and display the match history help text."""
    web.open(r'help\h2h-help.txt')


def create_own_league_help():
    """Load and display the  how to create a league help text."""
    web.open(r'help\create-league-help.txt')


def close_h2h_wndw():
    """Close h2h window"""
    Fp.cstm_wndw.destroy()
    Fp.h2h_wndw_is_open = False


def custom_window(win_title):
    """Creates a custom window. Takes title name for window as arg."""
    Fp.cstm_wndw = tk.Toplevel(root)
    Fp.cstm_wndw.title(win_title)
    Fp.cstm_wndw.attributes('-topmost', 1)  # Bring custom window to front.
    Fp.cstm_wndw.attributes('-toolwindow', 1)  # Removes part of toolbar.
    Fp.cstm_wndw.protocol('WM_DELETE_WINDOW', Fp.cstm_wndw.iconify)
    Fp.cstm_frame = tk.LabelFrame(Fp.cstm_wndw)
    Fp.cstm_wndw.resizable(False, False)
    Fp.cstm_frame.grid(padx=8, pady=8)


def same_team_check():
    """Error If selected same team for home and away."""
    Fp.home_team = Fp.ht_combo.get()
    Fp.away_team = Fp.at_combo.get()
    if Fp.away_team == Fp.home_team:
        messagebox.showinfo('Doh!',
                            'Please choose two different teams...')
        Fp.team_error = True
        


def per_cent(num1, num2):
    """Calculates percentage of 2 numbers given as args.
       Used to find clean sheet percentages in head2head"""
    Fp.hm_cln_sht_percent = '{0:.2f}'.format((num1 / num2 * 100))


def create_h2h_result_string():
    """Create a string of the h2h match and result, example:
       Leeds V Everton 2-1 10-Mar-1994"""
    Fp.h2h_result = Fp.home_team_h2h + ' V ' + Fp.away_team_h2h  \
        + ' ' + str(Fp.home_goals_h2h)  \
        + '-' + str(Fp.away_goals_h2h) + '  ' + str(Fp.game_date)


def compile_h2h_stats():
    """Gather stats for h2h game."""
    # If we find a match for the two teams selected by the user:
    if Fp.home_team_h2h == Fp.home_team and Fp.away_team_h2h == Fp.away_team:
        # Inc amount of matches found.
        Fp.h2h_matches += 1

        create_h2h_result_string()

        # Insert the match result into the match history scr txt box.
        Fp.scr_txt_box.insert(tk.INSERT, Fp.h2h_result + '\n')

        """The bool checks are to make sure there are no div by zero
           later on when trying to get averages, i.e win check true if
           team has had a win, false if not had a win."""

        # Home team win.
        if Fp.home_goals_h2h > Fp.away_goals_h2h:
            Fp.h2h_home_team_win_count += 1
            Fp.home_team_h2h_pts_total += 3
            Fp.home_team_gls_scored_when_won_total += Fp.home_goals_h2h
            Fp.ht_win_check = True

        # Home team clean sheet?.
        if Fp.away_goals_h2h == 0:
            Fp.ht_clean_sheet += 1

        # Away team win.
        if Fp.away_goals_h2h > Fp.home_goals_h2h:
            Fp.h2h_away_team_win_count += 1
            Fp.away_team_h2h_pts_total += 3
            Fp.away_team_gls_scored_when_won_total += Fp.away_goals_h2h
            Fp.at_win_check = True

        # Away team clean sheecreate_own_league_helpt?.
        if Fp.home_goals_h2h == 0:
            Fp.at_clean_sheet += 1

        # Its a draw.
        if Fp.home_goals_h2h == Fp.away_goals_h2h:
            Fp.h2h_home_team_draw_count += 1
            Fp.h2h_away_team_draw_count += 1

            Fp.home_team_h2h_pts_total += 1
            Fp.away_team_h2h_pts_total += 1

            Fp.h2h_ht_avg_gls_when_draw += Fp.home_goals_h2h
            Fp.h2h_at_avg_gls_when_draw += Fp.away_goals_h2h
            Fp.ht_draw_check = True
            Fp.at_draw_check = True

        # Home team lost.
        if Fp.home_goals_h2h < Fp.away_goals_h2h:
            Fp.h2h_home_team_lost_count += 1
            Fp.h2h_ht_avg_gls_when_lost += Fp.home_goals_h2h
            Fp.ht_lost_check = True

        # Away team lost.
        if Fp.home_goals_h2h > Fp.away_goals_h2h:
            Fp.h2h_away_team_lost_count += 1
            Fp.h2h_at_avg_gls_when_lost += Fp.away_goals_h2h
            Fp.at_lost_check = True

        # Keep track of goals scored by both teams.
        Fp.hm_tm_gls_h2h += Fp.home_goals_h2h
        Fp.aw_tm_gls_h2h += Fp.away_goals_h2h


def store_num_of_h2h_matchs_found():
    """Insert amount of matchs found into the h2h scr txt box."""
    Fp.scr_txt_box.insert(tk.INSERT, '\n'
                          + str(Fp.h2h_matches) +
                          ' Head to head Matches found.\n')


def zero_padding():
    """Make sure all the data is padded with a zero if less than 10
       to keep the h2h table aligned and neat."""
    x = str(Fp.h2h_home_team_win_count).zfill(2)
    Fp.h2h_home_team_win_count = x

    x = str(Fp.h2h_home_team_draw_count).zfill(2)
    Fp.h2h_home_team_draw_count = x

    x = str(Fp.h2h_home_team_lost_count).zfill(2)
    Fp.h2h_home_team_lost_count = x

    x = str(Fp.h2h_away_team_win_count).zfill(2)
    Fp.h2h_away_team_win_count = x

    x = str(Fp.h2h_away_team_draw_count).zfill(2)
    Fp.h2h_away_team_draw_count = x

    x = str(Fp.h2h_away_team_lost_count).zfill(2)
    Fp.h2h_away_team_lost_count = x

    x = str(Fp.hm_tm_gls_h2h).zfill(2)
    Fp.hm_tm_gls_h2h = x

    x = str(Fp.aw_tm_gls_h2h).zfill(2)
    Fp.aw_tm_gls_h2h = x

    x = str(Fp.home_team_h2h_pts_total).zfill(2)
    Fp.home_team_h2h_pts_total = x

    x = str(Fp.away_team_h2h_pts_total).zfill(2)
    Fp.away_team_h2h_pts_total = x


def h2h_stats_table():
    """print match results and head2head table in h2h scr text box."""
    # Pad numbers less than ten with a left zero.
    zero_padding()

    Fp.home_table = 'Home team: ' + str(Fp.h2h_home_team_win_count) + '  ' + str(Fp.h2h_home_team_draw_count)  \
                    + '  ' + str(Fp.h2h_home_team_lost_count) + '  ' + str(Fp.hm_tm_gls_h2h)  \
                    + '  ' + str(Fp.home_team_h2h_pts_total)

    Fp.away_table = 'Away team: ' + str(Fp.h2h_away_team_win_count) + '  ' + str(Fp.h2h_away_team_draw_count)  \
                    + '  ' + str(Fp.h2h_away_team_lost_count) + '  ' + str(Fp.aw_tm_gls_h2h)  \
                    + '  ' + str(Fp.away_team_h2h_pts_total)

    Fp.scr_txt_box.insert(tk.INSERT, '------------------------------\n')
    Fp.scr_txt_box.insert(tk.INSERT, '           W   D   L   G   Pts\n')
    Fp.scr_txt_box.insert(tk.INSERT, Fp.home_table + '\n')
    Fp.scr_txt_box.insert(tk.INSERT, Fp.away_table + '\n')
    Fp.scr_txt_box.insert(tk.INSERT, '\n')


def h2h_stats_header():
    """Print textheader for h2h stats in h2h box and in txt file."""
    Fp.scr_txt_box.insert(tk.INSERT, '\nStats for this fixture:\n' +
                          '-----------------------\n' +
                          str(Fp.home_team))


def draw_rate():
    """Find the draw rate percentage of the h2h match."""
    Fp.h2h_avg_draws = '{0:.2f}'.format(
        (int(Fp.h2h_home_team_draw_count) / Fp.h2h_matches * 100))

    Fp.scr_txt_box.insert(tk.INSERT, '\n\nDraws : '
                          + str(Fp.h2h_avg_draws) + '%')


def avg_home_gls_when_won():
    """Calc and show average goals scored by home team when won the game."""
    if Fp.ht_win_check:
        Fp.h2h_ht_avg_gls_when_won = float(
            Fp.home_team_gls_scored_when_won_total) / float(Fp.h2h_home_team_win_count)
        Fp.h2h_ht_avg_gls_when_won = round(Fp.h2h_ht_avg_gls_when_won, 1)
    else:
        Fp.h2h_ht_avg_gls_when_won = '0.0'

    Fp.scr_txt_box.insert(tk.INSERT, '\nAvg goals scored when won : ' +
                          str(Fp.h2h_ht_avg_gls_when_won))


def h2h_home_team_win_percent():
    """h2h home win percentage."""
    Fp.ht_win_percent = '{0:.2f}'.format(
        (int(Fp.h2h_home_team_win_count) / Fp.h2h_matches * 100))

    Fp.scr_txt_box.insert(tk.INSERT,
                          '\nWin rate: ' + str(Fp.ht_win_percent) + '%')


def h2h_away_team_win_percent():
    """h2h away win percentage."""
    Fp.at_win_percent = '{0:.2f}'.format(
        (int(Fp.h2h_away_team_win_count) / Fp.h2h_matches * 100))

    Fp.scr_txt_box.insert(tk.INSERT, '\nWin rate: '
                          + str(Fp.at_win_percent) + '%')


def avg_home_gls_when_draw():
    """Calc and show average goals scored by both teams when drew the game."""
    if Fp.ht_draw_check:
        Fp.h2h_ht_avg_gls_when_draw = float(
            Fp.h2h_ht_avg_gls_when_draw) / float(Fp.h2h_home_team_draw_count)
        Fp.h2h_ht_avg_gls_when_draw = round(Fp.h2h_ht_avg_gls_when_draw, 1)
    else:
        Fp.h2h_ht_avg_gls_when_draw = '0.0'

    Fp.scr_txt_box.insert(tk.INSERT, '\navg goals scored when draw: '
                          + str(Fp.h2h_ht_avg_gls_when_draw))


def avg_home_gls_when_lost():
    """Calc and show average goals scored by home team when lost the game."""
    if Fp.ht_lost_check:
        Fp.h2h_ht_avg_gls_when_lost = float(
            Fp.h2h_ht_avg_gls_when_lost) / float(Fp.h2h_home_team_lost_count)
        Fp.h2h_ht_avg_gls_when_lost = round(Fp.h2h_ht_avg_gls_when_lost, 1)
    else:
        Fp.h2h_ht_avg_gls_when_lost = '0.0'

    Fp.scr_txt_box.insert(tk.INSERT, '\navg goals scored when lost: '
                          + str(Fp.h2h_ht_avg_gls_when_lost))


def home_clean_sheets():
    """h2h home clean sheet percentage."""
    Fp.hm_cln_sht_percent = '{0:.2f}'.format(
        (Fp.ht_clean_sheet / Fp.h2h_matches * 100))
    Fp.scr_txt_box.insert(tk.INSERT, '\nClean sheets: '
                          + str(Fp.ht_clean_sheet)
                          + ' (' + str(Fp.hm_cln_sht_percent) +
                          '%)')


def away_header():
    """Away team header text."""
    Fp.scr_txt_box.insert(tk.INSERT, '\n\n' + str(Fp.away_team))


def avg_away_gls_when_won():
    """h2h away goals average when won."""
    if Fp.at_win_check:
        Fp.h2h_at_avg_gls_when_won = float(
            Fp.away_team_gls_scored_when_won_total) / float(Fp.h2h_away_team_win_count)
        Fp.h2h_at_avg_gls_when_won = round(Fp.h2h_at_avg_gls_when_won, 1)
    else:
        Fp.h2h_at_avg_gls_when_won = '0.0'

    Fp.scr_txt_box.insert(tk.INSERT, '\navg goals scored when won : '
                          + str(Fp.h2h_at_avg_gls_when_won))


def avg_away_gls_when_draw():
    """h2h away goals average when draw."""
    if Fp.at_draw_check:
        Fp.h2h_at_avg_gls_when_draw = float(
            Fp.h2h_at_avg_gls_when_draw) / float(Fp.h2h_away_team_draw_count)
        Fp.h2h_at_avg_gls_when_draw = round(Fp.h2h_at_avg_gls_when_draw, 1)
    else:
        Fp.h2h_at_avg_gls_when_draw = '0.0'

    Fp.scr_txt_box.insert(tk.INSERT, '\navg goals scored when draw: '
                          + str(Fp.h2h_at_avg_gls_when_draw))


def avg_away_gls_when_lost():
    """Calc and show average goals scored by away team when lost the game."""
    if Fp.at_lost_check:
        Fp.h2h_at_avg_gls_when_lost = float(
            Fp.h2h_at_avg_gls_when_lost) / float(Fp.h2h_away_team_lost_count)
        Fp.h2h_at_avg_gls_when_lost = round(Fp.h2h_at_avg_gls_when_lost, 1)
    else:
        Fp.h2h_at_avg_gls_when_lost = '0.0'

    Fp.scr_txt_box.insert(tk.INSERT, '\navg goals scored when lost: '
                          + str(Fp.h2h_at_avg_gls_when_lost) + '\n')


def away_clean_sheets():
    """h2h away team clean sheets."""
    Fp.at_cln_sht_percent = '{0:.2f}'.format(
        (Fp.at_clean_sheet / Fp.h2h_matches * 100))

    Fp.scr_txt_box.insert(tk.INSERT, 'Clean sheets: '
                          + str(Fp.at_clean_sheet) +
                          ' (' + str(Fp.at_cln_sht_percent) +
                          '%)')


def zero_h2h_vars():
    """Zero all vars used in head to head stats."""
    Fp.home_team_h2h = ''  # Name of home team
    Fp.away_team_h2h = ''  # Name of away team
    Fp.h2h_matches = 0     # Amount of h2h matches found.
    Fp.hm_tm_gls_h2h = 0   # Home team goals counter
    Fp.aw_tm_gls_h2h = 0   # Away team goals counter
    Fp.h2h_home_team_win_count = 0
    Fp.h2h_away_team_win_count = 0
    Fp.h2h_home_team_draw_count = 0
    Fp.h2h_away_team_draw_count = 0
    Fp.h2h_home_team_lost_count = 0
    Fp.h2h_away_team_lost_count = 0
    Fp.h2h_home_team_win_count = 0
    Fp.h2h_away_team_win_count = 0
    Fp.hm_tm_gls_h2h = 0
    Fp.aw_tm_gls_h2h = 0
    Fp.home_team_h2h_pts_total = 0
    Fp.away_team_h2h_pts_total = 0
    Fp.home_team_gls_scored_when_won_total = 0
    Fp.away_team_gls_scored_when_won_total = 0
    Fp.home_team_gls_scored_when_draw_total = 0
    Fp.away_team_gls_scored_when_draw_total = 0
    Fp.h2h_at_avg_gls_when_draw = 0
    Fp.h2h_ht_avg_gls_when_draw = 0
    Fp.h2h_at_avg_gls_when_lost = 0
    Fp.h2h_ht_avg_gls_when_lost = 0
    Fp.ht_win_check = False
    Fp.at_win_check = False
    Fp.ht_draw_check = False
    Fp.at_draw_check = False
    Fp.ht_lost_check = False
    Fp.at_lost_check = False
    Fp.ht_clean_sheet = 0
    Fp.at_clean_sheet = 0
    Fp.hm_cln_sht_percent = 0
    Fp.at_cln_sht_percent = 0
    Fp.ht_win_percent = 0
    Fp.at_win_percent = 0
    Fp.h2h_avg_draws = 0


def copy_h2h_text():
    """Copy all the text from the h2h scr txt box to clipboard, for user."""
    Fp.scr_txt_box.focus()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    Fp.scr_txt_box.update()
    messagebox.showinfo('Program Information', 'H2H report copied\n'
                        'to your clipboard\n')


def h2h_btns_panel():
    """The head to head window buttons."""
    help_frame = tk.LabelFrame(Fp.cstm_wndw)
    help_frame.grid()

    help_btn = tk.Button(help_frame,
                         text='HELP',
                         command=h2h_help)
    help_btn.grid(row=0, column=0)

    edit_btn = tk.Button(help_frame,
                         text='COPY',
                         command=copy_h2h_text)
    edit_btn.grid(row=0, column=1)

    close_btn = tk.Button(help_frame,
                          text='EXIT',
                          command=close_h2h_wndw)
    close_btn.grid(row=0, column=2)


def head_to_head():
    """Output all match results found from csvs to listbox and txt."""
    # Has the user picked the same two teams?
    Fp.team_error = False
    same_team_check()
    if Fp.team_error:
        return

    # Make sure only this one history window is opened.
    if Fp.h2h_wndw_is_open:
        return

    # Flag that the h2h window is now open.
    Fp.h2h_wndw_is_open = True

    # Call create custom window, text for window mame.
    custom_window('EPL Head To Head Stats')

    # Create a scrl txt box in the custom frame.
    Fp.scr_txt_box = tk.scrolledtext.ScrolledText(Fp.cstm_frame,
                                                  bg='white',
                                                  fg='black',
                                                  width=50,
                                                  height=24)
    Fp.scr_txt_box.pack()

    """ ----------------------------Start csv scan----------------------
       Scan through all the CSV files for matches that contain
       both the home team and the away team playing each other
       and grab the data required. Starting with most recent
       results and going backwards thru years."""

    year1 = 2020
    year2 = 2021

    zero_h2h_vars()

    """29 seasons to scan through.
       Rather than list the filename of every CSV I have created the
       filenmaes in a for loop. typical filename is "pl-2020-2021.csv"
       "pl-2019-2020, "pl-2018-2019" etc. Stored in "data" folder."""

    Fp.scr_txt_box.insert(tk.INSERT, 'EPL Head To Head Match History:\n'
                                     '-------------------------------\n')
    for x in range(29):
        file_name = 'pl-' + str(year1) + '-' + str(year2) + str('.csv')

        csv_file = csv.reader(open('data/' + file_name))
        next(csv_file)

        # Collect the data we need.
        for heading in csv_file:
            Fp.game_date = heading[0]
            Fp.home_team_h2h = heading[1]
            Fp.away_team_h2h = heading[2]
            Fp.home_goals_h2h = int(heading[3])
            Fp.away_goals_h2h = int(heading[4])

            # Capture data like goals scored etc from each csv in turn.
            compile_h2h_stats()

        # Change year dates for reading next CSV file.Reading backwards.
        year1 -= 1
        year2 -= 1
    # ----------------------- End of csv scan--------------

    # Make sure there are at least 1 h2h matche found, if none exit.
    if not Fp.h2h_matches:
        close_h2h_wndw()
        messagebox.showinfo('No match data found',
                            'These two teams have not played\n'
                            'each other in the EPL yet.')

        return

    store_num_of_h2h_matchs_found()
    h2h_stats_table()
    h2h_stats_header()
    h2h_home_team_win_percent()
    avg_home_gls_when_won()
    avg_home_gls_when_draw()
    avg_home_gls_when_lost()
    home_clean_sheets()
    away_header()
    h2h_away_team_win_percent()
    avg_away_gls_when_won()
    avg_away_gls_when_draw()
    avg_away_gls_when_lost()
    away_clean_sheets()
    draw_rate()

    # Show btns at bottom of Match History window. help-open-exit.
    h2h_btns_panel()


def prediction():
    """Display dodgy prediction."""
    Fp.team_error = False
    same_team_check()
    if Fp.team_error:
        return

    # Open text file of team names insert into Fp.team_list.
    with open(Fp.team_list_file_name, 'r') as f:
        # splitlines removes the newline esc char.
        Fp.team_list = f.read().splitlines()

    directry = r'leagues/'

    if Fp.custom_league_in_use:
        directry = ''

    # Open text file of team ratings insert into Fp.team_values.
    with open(directry + Fp.ratings_file_name, 'r') as f:
        Fp.team_values = f.read().splitlines()

    ht_indx = Fp.ht_combo.current()
    htw = int(Fp.team_values[ht_indx])

    # htw = home team weighting etc.
    htw += 1  # 1pt added for home adv.

    at_indx = Fp.at_combo.current()
    atw = int(Fp.team_values[at_indx])

    # Calc score prediction.
    # 'abs' function gives the difference between the 2 ratings.
    home_score = 0
    away_score = 0
    orig_diff = 0
    ratings_diff = abs(htw - atw)

    # Limit to 4 goals max.
    if ratings_diff > 4:
        orig_diff = ratings_diff
        ratings_diff = 4

    # Calc how many goals for a draw.
    # Limit to max 2 goals each as 3-3 doesnt happen too often,
    # 4-4 or more is quite rare.
    if htw == atw:
        result = 'A Draw'
        # Pick common score draw result for home team, use as result.
        home_score = Fp.common_draws[ht_indx]
        away_score = Fp.common_draws[ht_indx]

    if htw > atw:
        result = 'Home Win'
        away_score = 0
        home_score = ratings_diff
        if abs(ratings_diff - orig_diff) > 2:  # Away team scores a goal if
            away_score = 1                     # pts diff 3 or more

    if htw < atw:
        result = 'Away Win'
        home_score = 0
        away_score = ratings_diff
        if abs(ratings_diff - orig_diff) > 2:
            home_score = 1

    Fp.predicted_score = (str(home_score) + ' - ' + str(away_score))

    result_msg = ' You Selected:\n {} V {} \n\n My prediction is:\n {}'  \
                 '\n\n Predicted score : {}'  \
                 .format(Fp.home_team, Fp.away_team, result, Fp.predicted_score)

    # Copy prediction to clipboard in format: Tottenham 1 V Liverpool 0.
    clip_text = ''

    clip_text = Fp.cstm_league_name + '\n'

    clip_text = clip_text + (str(Fp.home_team) + ' ' + str(home_score) +
                             ' V ' + str(Fp.away_team) + ' ' + str(away_score))
    pyperclip.copy(clip_text)

    pred_wndw = tk.Toplevel(root)
    pred_wndw.title('FP V1.24')
    pred_wndw.attributes('-topmost', 1)  # Bring custom window to front.

    pred_frame = tk.LabelFrame(pred_wndw)
    pred_wndw.resizable(False, False)
    pred_frame.grid(padx=8, pady=8)

    pred_label = tk.Label(pred_frame, bg='powderblue', text='\n'
                          + str(result_msg) +
                          '\n\nPrediction copied to clipboard')
    pred_label.grid()

    date_stamp = (datetime.now().strftime
                  (r'%d' + ('-') + '%b' + ('-') + '%Y' + ('-') + '%H' + ('.')
                   + '%M' + ('-') + '%S' + 's'))

    with open('footy-predictions.txt', 'a') as contents:
        contents.write(date_stamp + ':\n' + str(clip_text + '\n\n'))


def load_custom_league():
    """Load in a different league."""
    Fp.custom_league_in_use = False
    Fp.championship = False
    Fp.league_one = False
    Fp.league_two = False

    cl_file = filedialog.askopenfilename(
        initialdir='leagues', title='Select a custom league file', filetypes=(
            ('Custom Leagues', '*.fpcl'), ('All files', '*.*')))

    if not cl_file:
        return
    Fp.number_of_teams_in_league = 0

    with open(cl_file, 'r') as contents:
        Fp.team_list = [line.rstrip('\n') for line in contents]

    messagebox.showinfo('Footy Predictor Info',
                        'Custom League Loaded.\n\n'
                        + str(cl_file))

    if 'English Championship' in cl_file:
        Fp.championship = True
        Fp.premier = False

    if 'League One' in cl_file:
        Fp.league_one = True
        Fp.premier = False

    if 'League Two' in cl_file:
        Fp.league_two = True
        Fp.premier = False

    Fp.team_list_file_name = cl_file
    Fp.number_of_teams_in_league = len(Fp.team_list)

    Fp.cstm_league_name = filename = os.path.basename(cl_file)
    (file, ext) = os.path.splitext(filename)
    Fp.cstm_league_name = file

    Fp.orig_ratings_file_name = Fp.cstm_league_name + '-ratings'

    Fp.ht_combo.destroy()
    Fp.ht_combo = Combobox(msg_frame)
    Fp.ht_combo['values'] = (Fp.team_list)
    Fp.ht_combo.current(0)
    Fp.ht_combo.grid(padx=5, pady=5, row=1, column=0)
    Fp.ht_combo.update()

    Fp.at_combo.destroy()
    Fp.at_combo = Combobox(msg_frame)
    Fp.at_combo['values'] = (Fp.team_list)
    Fp.at_combo.current(1)
    Fp.at_combo.grid(padx=5, pady=5, row=1, column=1)
    Fp.at_combo.update()

    Fp.custom_league_in_use = True
    match_hist_btn.configure(state=tk.DISABLED)
    custom_menu.entryconfigure(0, state=tk.DISABLED)

    try:
        Fp.ratings_file_name = r'leagues/' + \
            str(Fp.cstm_league_name) + '-ratings.txt'

        with open(Fp.ratings_file_name, 'r') as f:
            Fp.team_values = f.read().splitlines()
    except BaseException:
        messagebox.showerror('File error',
                             'Something went badly wrong.\n\n'
                             'Did you load the correct file?\n\n'
                             'You will need to re-run FP'
                             ' from scratch.\n\nClick OK to exit.')
        root.destroy()
        sys.exit()


# Drop-down menu.
MENU_BAR = tk.Menu(root)
INFO_MENU = tk.Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Info', menu=INFO_MENU)
INFO_MENU.add_separator()
INFO_MENU.add_command(label='Help', command=help_menu)
INFO_MENU.add_command(label='About', command=about_menu)
INFO_MENU.add_command(
    label='Make a small donation via PayPal',
    command=donate_me)
INFO_MENU.add_separator()
INFO_MENU.add_command(label='Visit my Python blog', command=visit_blog)
INFO_MENU.add_command(label='Contact Author', command=contact_me)
INFO_MENU.add_separator()
INFO_MENU.add_command(label='Exit', command=exit_app)
root.config(menu=MENU_BAR)


# History menu.
HIST_MENU = tk.Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='History', menu=HIST_MENU)
HIST_MENU.add_command(label='View Prediction history file', command=pred_hist)
HIST_MENU.add_command(
    label='Reset prediction history file',
    command=new_hist_file)
root.config(menu=MENU_BAR)


# Links menu.
links_MENU = tk.Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Links', menu=links_MENU)
links_MENU.add_command(
    label='EPL Results and Fixtures',
    command=view_results_fixtures)
links_MENU.add_command(
    label='EPL Table, current form and stats',
    command=view_pl_stats)
links_MENU.add_command(label='EPL Historical Data', command=view_pl_data)
links_MENU.add_separator()
links_MENU.add_command(
    label='England Championship Table stats form',
    command=view_championship_table)
links_MENU.add_command(
    label='England League One Table stats form',
    command=view_league_one_table)
links_MENU.add_command(
    label='England League Two Table stats form',
    command=view_league_two_table)
root.config(menu=MENU_BAR)


# Custom league menu.
custom_menu = tk.Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='leagues', menu=custom_menu)
custom_menu.add_command(label='Load A League',
                        command=load_custom_league)
custom_menu.add_separator()
custom_menu.add_command(label='How To Create Another League',
                        command=create_own_league_help)
root.config(menu=MENU_BAR)


# Open text file of team names insert into Fp.team_list.
with open('English Premiership.txt', 'r') as f:
    # Splitlines removes the newline esc char.
    Fp.team_list = f.read().splitlines()


# Open text file of team ratings insert into Fp.team_values.
with open(r'leagues/' + Fp.ratings_file_name, 'r') as f:
    Fp.team_values = f.read().splitlines()


# Label texts.
msg_frame = tk.LabelFrame(root)
msg_frame.grid(padx=8, pady=8)
sel_ht_label = tk.Label(msg_frame, text='Select Home Team')
sel_ht_label.grid()
sel_at_label = tk.Label(msg_frame, text='Select Away Team')
sel_at_label.grid(row=0, column=1)

# Combo boxes.
# Temporarily remove last list item which is "select team".
temp_list = Fp.team_list
temp_list.pop()

Fp.ht_combo = Combobox(msg_frame)
Fp.ht_combo['values'] = (temp_list)
Fp.ht_combo.current(16)
Fp.ht_combo.grid(padx=5, pady=5)

Fp.at_combo = Combobox(msg_frame)
Fp.at_combo['values'] = (temp_list)
Fp.at_combo.current(11)
Fp.at_combo.grid(padx=5, pady=5, row=1, column=1)

# Frame for the match history, predict and match odds buttons.
btns_frame = tk.Frame(root)
btns_frame.grid(padx=8, pady=3)

# Note. making btns relief=flat removes ugly button surround.
match_hist_btn = tk.Button(btns_frame,
                           command=head_to_head)
photo = tk.PhotoImage(file='images/history-btn.png')
match_hist_btn.config(image=photo, relief=tk.FLAT)
match_hist_btn.grid(column=0, row=0, padx=2, pady=5)

predict_btn = tk.Button(btns_frame,
                        command=prediction)
photo2 = tk.PhotoImage(file='images/prediction-btn.png')
predict_btn.config(image=photo2, relief=tk.FLAT)
predict_btn.grid(column=1, row=0, padx=2, pady=5)

stats_btn = tk.Button(btns_frame,
                      command=view_odds)
photo3 = tk.PhotoImage(file='images/odds-btn.png')
stats_btn.config(image=photo3, relief=tk.FLAT)
stats_btn.grid(column=2, row=0, padx=2, pady=5)

# Checks for a click on the main window X icon.
root.protocol("WM_DELETE_WINDOW", exit_app)

root.mainloop()
