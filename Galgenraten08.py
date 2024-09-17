from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import os
import sys
import math
from openpyxl import Workbook, load_workbook

def filter_words(filename):
    filtered_words = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            word_group = line.strip()
            if len(word_group) >= 4:
                filtered_words.append(word_group)
    
    return filtered_words

def filter_quotes(quotes_file):
    filtered_quotes = []

    with open(quotes_file, "r", encoding="utf-8") as file:
        for line in file:
            quotes_group = line.strip()
            if len(quotes_group) >= 4:
                filtered_quotes.append(quotes_group)
    
    return filtered_quotes

def calculate_word_difficulty(word):
    global medium_count, hard_count, total_letters, difficulty_per_letter, coins
    
    if selected_language == "Deutsch":
        easy_letters = {'a', 'e', 'i', 'u', 's', 'r', 't', 'n', 'l', 'h', 'g'}
        medium_letters = {'m', 'k', 'b', 'f', 'c', 'o', 'w', 'd'}
        hard_letters = {'y', 'x', 'q', 'v', 'j', 'ü', 'ö', 'ß', 'ä', 'p', 'z'}
    elif selected_language == "Englisch":
        easy_letters = {'a', 'e', 'i', 'r', 'n', 'l', 'b', 'd', 'o'}
        medium_letters = {'m', 't', 's', 'y', 'g', 'u', 'v', 'h'}
        hard_letters = {'x', 'q', 'j', 'p', 'z', 'c', 'k', 'w', 'f'}
    elif selected_language == "Französisch":
        easy_letters = {'e', 's', 'a', 'i', 't', 'n', 'r', 'u', 'l'}
        medium_letters = {'o', 'd', 'c', 'p', 'm', 'v', 'q', 'f'}
        hard_letters = {'é', 'b', 'g', 'h', 'j', 'à', 'x', 'y', 'w', 'k', 'z'}
    elif selected_language == "Spanisch":
        easy_letters = {'e', 'a', 'o', 's', 'r', 'n', 'i', 'd', 'l'}
        medium_letters = {'c', 't', 'u', 'm', 'p', 'b', 'g'}
        hard_letters = {'v', 'y', 'q', 'h', 'f', 'z', 'j', 'x', 'w'}
    else:
        easy_letters = {'a', 'e', 'i', 'u', 's', 'r', 't', 'n', 'l', 'h', 'g'}
        medium_letters = {'m', 'k', 'b', 'f', 'c', 'o', 'w', 'd'}
        hard_letters = {'y', 'x', 'q', 'v', 'j', 'ü', 'ö', 'ß', 'ä', 'p', 'z'}

    
    medium_count = sum(1 for char in word.lower() if char in medium_letters)
    hard_count = sum(1 for char in word.lower() if char in hard_letters) * 2
    total_letters = len(word)
    
    difficulty = 0
    for char in word.lower():
        if char in hard_letters:
            difficulty += 3
            coins += 0.3
        elif char in medium_letters:
            difficulty += 2
            coins += 0.2
        elif char in easy_letters:
            difficulty += 1
            coins += 0.1
        else:
            difficulty += 1
            coins += 0.1
    
    difficulty_per_letter = difficulty / total_letters
    coins = round(coins, 1)
    save_coins()
    return difficulty_per_letter

def convert_to_stars(difficulty_per_letter):
    if difficulty_per_letter >= 1.55:
        return "★★★★★"
    elif difficulty_per_letter <= 1.2:
        return "★☆☆☆☆"
    elif difficulty_per_letter <= 1.3:
        return "★★☆☆☆"
    elif difficulty_per_letter <= 1.4:
        return "★★★☆☆"
    else:
        return "★★★★☆"

def calculate_letter_difficulty(letter):
    if selected_language == "Deutsch":
        easy_letters = {'a', 'e', 'i', 'u', 's', 'r', 't', 'n', 'l', 'h', 'g'}
        medium_letters = {'m', 'k', 'b', 'f', 'c', 'o', 'w', 'd'}
        hard_letters = {'y', 'x', 'q', 'v', 'j', 'ü', 'ö', 'ß', 'ä', 'p', 'z'}
    elif selected_language == "Englisch":
        easy_letters = {'a', 'e', 'i', 'r', 'n', 'l', 'b', 'd', 'o'}
        medium_letters = {'m', 't', 's', 'y', 'g', 'u', 'v', 'h'}
        hard_letters = {'x', 'q', 'j', 'p', 'z', 'c', 'k', 'w', 'f'}
    elif selected_language == "Französisch":
        easy_letters = {'e', 's', 'a', 'i', 't', 'n', 'r', 'u', 'l'}
        medium_letters = {'o', 'd', 'c', 'p', 'm', 'v', 'q', 'f'}
        hard_letters = {'é', 'b', 'g', 'h', 'j', 'à', 'x', 'y', 'w', 'k', 'z'}
    elif selected_language == "Spanisch":
        easy_letters = {'e', 'a', 'o', 's', 'r', 'n', 'i', 'd', 'l'}
        medium_letters = {'c', 't', 'u', 'm', 'p', 'b', 'g'}
        hard_letters = {'v', 'y', 'q', 'h', 'f', 'z', 'j', 'x', 'w'}
    else:
        easy_letters = {'a', 'e', 'i', 'u', 's', 'r', 't', 'n', 'l', 'h', 'g'}
        medium_letters = {'m', 'k', 'b', 'f', 'c', 'o', 'w', 'd'}
        hard_letters = {'y', 'x', 'q', 'v', 'j', 'ü', 'ö', 'ß', 'ä', 'p', 'z'}

    if letter in hard_letters:
        return 3
    elif letter in medium_letters:
        return 2
    elif letter in easy_letters:
        return 1
    else:
        return 1

def choose_random_word():
    global current_word, display_word, guessed_letters, mistake_count, word_difficulty, game_over, mmr_change
    
    if not game_over:
        result_label.config(text="Bitte errate das aktuelle Wort zuerst.")
        return
    
    mistake_count = 0
    game_over = False
    mmr_change = 0

    if words:
        current_word = random.choice(words)
        words.remove(current_word)
        
        display_word = ["_" if char != "-" else "-" for char in current_word]
        
        guessed_letters = []
        
        difficulty_rating = calculate_word_difficulty(current_word)
        #difficulty_stars = convert_to_stars(difficulty_rating)
        
        label.config(text=" ".join(display_word))
        update_difficulty_label(difficulty_frame, difficulty_rating)
        result_label.config(text="")
        show_image("0.png")
        
        word_difficulty = calculate_word_difficulty(current_word)
        mmr_label.config(text=f"MMR: {mmr_points}")
        mmr_change_label.config(text="", fg="black")
        update_coins_label()
        update_winstreak_label()  
        log_event_diff(f"{word_difficulty}")
    else:
        label.config(text="Keine Wörter mehr übrig")

wrong_letters = []  # Neue Liste für falsch geratene Buchstaben

def guess_letter(event=None):
    global current_word, display_word, guessed_letters, mistake_count, mmr_points, game_over, mmr_change, winstreak, coins, wrong_letters
    
    if game_over:
        return

    user_input = entry.get().lower()
    entry.delete(0, END)
    
    if not user_input.isalpha() or len(user_input) != 1:
        result_label.config(text="Bitte gib einen einzelnen Buchstaben ein.")
        return
    
    if user_input in guessed_letters:
        result_label.config(text="Du hast diesen Buchstaben bereits geraten.")
        return

    guessed_letters.append(user_input)
    
    positions = [pos for pos, char in enumerate(current_word) if char.lower() == user_input]
    
    if positions:
        for pos in positions:
            display_word[pos] = current_word[pos]
        label.config(text=" ".join(display_word))
        positions = [pos + 1 for pos in positions]
        result_label.config(text=f"Der Buchstabe '{user_input}' befindet sich\n an den Positionen: {positions}")
        
        letter_difficulty = calculate_letter_difficulty(user_input)
        if total_letters >= 19:
            change = round(max(1, 2 * letter_difficulty)*((-2*math.sqrt(abs(mmr_points)))*0.01 + 1.5))
            mmr_points += change
            define_rank(mmr_points)
            mmr_change += change
        else:
            change = round(max(1, 3 * letter_difficulty)*((-2*math.sqrt(abs(mmr_points)))*0.01 + 1.5))
            mmr_points += change
            define_rank(mmr_points)
            mmr_change += change
            
       # update_letter_stats(workbook, user_input, True)
        
    else:
        result_label.config(text=f"Der Buchstabe '{user_input}' ist \n nicht im Wort enthalten.")
        mistake_count += 1
        
        # Falsche Buchstaben speichern und anzeigen
        wrong_letters.append(user_input)
        wrong_letters_label.config(text=f"Falsche Buchstaben: {', '.join(wrong_letters)}")
        
        letter_difficulty = calculate_letter_difficulty(user_input)
        change = max(1, 4 - letter_difficulty)
        mmr_points -= change
        define_rank(mmr_points)
        mmr_change -= change
        
        #update_letter_stats(workbook, user_input, False)  # Buchstabe war nicht im Wort


    picture = f"{mistake_count}.png"
    show_image(picture)
    mmr_label.config(text=f"MMR: {mmr_points}")

    if mistake_count > 7:
        label.config(text="Das Wort war " + current_word)
        result_label.config(text="Du hast verloren")
        log_event_succ("Spiel verloren")
        change = round(max(20, 60 - 20 * word_difficulty))
        mmr_points -= change
        define_rank(mmr_points)
        mmr_change -= change
        mmr_label.config(text=f"MMR: {mmr_points}")
        save_mmr()
        
        winstreak = 0  
        save_winstreak()
        update_winstreak_label()
        log_event_mmr(f"{mmr_change}")
        game_over = True
        #update_all_letter_stats(workbook, current_word, guessed_letters)
        
    elif "_" not in display_word:
        result_label.config(text="Glückwunsch! Du hast das Wort erraten:\n" + current_word)
        log_event_succ("Spiel gewonnen")
        if winstreak >= 3:
            change = round((max(20, word_difficulty * 20) * (1 + 0.05 * winstreak)) * ((-2*math.sqrt((abs(mmr_points))))*0.01 + 1.5))
            #print(round(max(20, word_difficulty * 20)))
            #print(1 + 0.05 * winstreak)
        else:
            change = round((max(20, word_difficulty * 20)) * ((-2*math.sqrt((abs(mmr_points))))*0.01 + 1.5))
            
        #print(change)
        #print(word_difficulty)
       # print(round((max(20, word_difficulty * 20))))
       # print(mmr_points)
        #print(((-2*math.sqrt(mmr_points))*0.01 + 1.5))
        mmr_points += change
        define_rank(mmr_points)
        mmr_change += change
        mmr_label.config(text=f"MMR: {mmr_points}")
        save_mmr()
        coins += 2 * round(word_difficulty,1)
        save_coins()
        load_coins()
        winstreak += 1 
        save_winstreak()
        update_winstreak_label()
        log_event_mmr(f"{mmr_change}") 
        game_over = True
        update_highscore()
        #update_all_letter_stats(workbook, current_word, guessed_letters)

    update_mmr_change_label()

def reveal_random_letter():
    global coins, display_word, guessed_letters, winstreak, game_over
    
    if coins < 50:
        result_label.config(text="Nicht genügend Münzen für einen Tipp.")
        return
    
    save_coins()
    update_coins_label()
    
    # Suche nach allen unaufgedeckten Buchstaben im aktuellen Wort
    remaining_indices = [i for i, char in enumerate(display_word) if char == "_"]
    if not remaining_indices:
        result_label.config(text="Alle Buchstaben sind bereits aufgedeckt.")
        return
    
    # Ziehe zufällig einen Index und finde den Buchstaben an dieser Position
    coins -= 50
    random_index = random.choice(remaining_indices)
    letter_to_reveal = current_word[random_index].lower()

    # Decke alle Vorkommen dieses Buchstabens im Wort auf
    for i, char in enumerate(current_word):
        if char.lower() == letter_to_reveal:
            display_word[i] = char
    
    guessed_letters.append(letter_to_reveal)
    
    # Aktualisiere das Label mit dem neu aufgedeckten Wort
    label.config(text=" ".join(display_word))
    result_label.config(text=f"Der Buchstabe '{letter_to_reveal}' wurde aufgedeckt.")
    
    # Überprüfe, ob das Wort vollständig aufgedeckt wurde
    if "_" not in display_word:
        result_label.config(text="Glückwunsch! Du hast das Wort erraten:\n" + current_word)
        log_event_succ("Spiel gewonnen")
        
        define_rank(mmr_points)
        
        mmr_label.config(text=f"MMR: {mmr_points}")
        save_mmr()
        save_coins()
        load_coins()
        save_winstreak()
        update_winstreak_label()
        log_event_mmr(f"{mmr_change}") 
        game_over = True
        update_highscore()



def update_highscore():
    global highscore
    if mmr_points > highscore:
        highscore = mmr_points
        save_highscore()
        highscore_label.config(text=f"Highscore: {highscore}", fg="gold")
    else:
        highscore_label.config(text=f"Highscore: {highscore}", fg="black")
        
def update_mmr_change_label():
    if mmr_change > 0:
        mmr_change_label.config(text=f"+{mmr_change} MMR", fg="green")
    elif mmr_change < 0:
        mmr_change_label.config(text=f"{mmr_change} MMR", fg="red")
    else:
        mmr_change_label.config(text="0 MMR", fg="black")

def update_winstreak_label():
    if winstreak > 2:
        winstreak_label.config(text=f"Winstreak: {winstreak}")
    else:
        winstreak_label.config(text="")

def update_coins_label():
    if coins:
        coins_label.config(text=f"{coins} ◎")
    else:
        winstreak_label.config(text=" 0 ◎")
                
def define_rank(mmr_points):
    
    if mmr_points < 133:
        rank = "Bronze"
        subdivision = "III"
        text_color = "#cd7f32"  
    elif mmr_points < 266:
        rank = "Bronze"
        subdivision = "II"
        text_color = "#cd7f32"  
    elif mmr_points < 400:
        rank = "Bronze"
        subdivision = "I"
        text_color = "#cd7f32"  
    elif mmr_points < 533:
        rank = "Silber"
        subdivision = "III"
        text_color = "#c0c0c0"  
    elif mmr_points < 666:
        rank = "Silber"
        subdivision = "II"
        text_color = "#c0c0c0"  
    elif mmr_points < 800:
        rank = "Silber"
        subdivision = "I"
        text_color = "#c0c0c0"  
    elif mmr_points < 933:
        rank = "Gold"
        subdivision = "III"
        text_color = "#ffd700"  
    elif mmr_points < 1066:
        rank = "Gold"
        subdivision = "II"
        text_color = "#ffd700"  
    elif mmr_points < 1200:
        rank = "Gold"
        subdivision = "I"
        text_color = "#ffd700"  
    elif mmr_points < 1333:
        rank = "Platin"
        subdivision = "III"
        text_color = "#e5e4e2" 
    elif mmr_points < 1466:
        rank = "Platin"
        subdivision = "II"
        text_color = "#e5e4e2" 
    elif mmr_points < 1600:
        rank = "Platin"
        subdivision = "I"
        text_color = "#e5e4e2" 
    elif mmr_points < 1733:
        rank = "Diamant"
        subdivision = "III"
        text_color = "#b9f2ff"  
    elif mmr_points < 1866:
        rank = "Diamant"
        subdivision = "II"
        text_color = "#b9f2ff"  
    elif mmr_points < 2000:
        rank = "Diamant"
        subdivision = "I"
        text_color = "#b9f2ff"  
    elif mmr_points < 2133:
        rank = "Champion"
        subdivision = "III"
        text_color = "#91DFFF"  
    elif mmr_points < 2266:
        rank = "Champion"
        subdivision = "II"
        text_color = "#91DFFF"  
    elif mmr_points < 2400:
        rank = "Champion"
        subdivision = "I"
        text_color = "#91DFFF"  
    else:
        rank = "Grand Champion"
        subdivision = ""
        text_color = "#ffdf00" 
    
    label_rank.config(text=f"{rank} {subdivision}", fg=text_color)

def show_image(image_name):
    try:
        image = PhotoImage(file=os.path.join(image_path, image_name))
        label_image.config(image=image)
        label_image.image = image
    except TclError as e:
        print(f"Fehler beim Laden des Bildes: {e}")

def start_game():
    start_frame.pack_forget()
    game_frame.pack()
    choose_random_word()
    

def save_mmr():
    with open(mmr_file, "w", encoding="utf-8") as file:
        file.write(str(mmr_points))

def load_mmr():
    global mmr_points
    try:
        with open(mmr_file, "r", encoding="utf-8") as file:
            mmr_points = int(file.read())
            
    except FileNotFoundError:
        mmr_points = 0  
        
def save_coins():
    with open(coins_file, "w", encoding="utf-8") as file:
        file.write(str(coins))

def load_coins():
    global coins
    try:
        with open(coins_file, "r", encoding="utf-8") as file:
            coins = round(float(file.read()))
            
    except FileNotFoundError:
        coins = 0  

def save_winstreak():
    with open(winstreak_file, "w", encoding="utf-8") as file:
        file.write(str(winstreak))

def load_winstreak():
    global winstreak
    try:
        with open(winstreak_file, "r", encoding="utf-8") as file:
            winstreak = int(file.read())
    except FileNotFoundError:
        winstreak = 0  

def save_highscore():
    with open(highscore_file, "w", encoding="utf-8") as file:
        file.write(str(highscore))

def load_highscore():
    global highscore
    try:
        with open(highscore_file, "r", encoding="utf-8") as file:
            highscore = int(file.read())
    except FileNotFoundError:
        highscore = 0  
                
def log_event_succ(event):
    #timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_succ, "a", encoding="utf-8") as file:
        file.write(f"{event}\n")
def log_event_diff(event):
    #timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_diff, "a", encoding="utf-8") as file:
         file.write(f"{format_decimal(event)}\n")
def log_event_mmr(event):
    #timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_mmr, "a", encoding="utf-8") as file:
        file.write(f"{event}\n")

def format_decimal(value):
    return str(value).replace('.', ',')

def update_difficulty_label(frame, difficulty_rating):
    difficulty_stars = convert_to_stars(difficulty_rating)
    label_difficulty.config(text=f"Schwierigkeit: ", font=('Helvetica', 12), bg='#212121')
    label_stars.config(text=difficulty_stars, font=('Helvetica', 12), bg='#212121', fg='gold')

def load_words_for_language(language):
    global words, filename
    filename = f"{exe_path}\\words_{language}.txt"
    words = filter_words(filename)

def on_language_change(event):
    global selected_language
    selected_language = language_var.get()
    load_words_for_language(selected_language)


def reset_data():
    global mmr_points, coins, winstreak
    
    # Setze die Werte auf 0
    mmr_points = 0
    winstreak = 0
    
    # Speichere die neuen Werte
    save_mmr()       # Speichert 0 in die MMR-Datei
    save_winstreak() # Speichert 0 in die Winstreak-Datei

    result_label.config(text="Alle Daten wurden zurückgesetzt.")

def confirm_reset():
    # Öffnet ein Bestätigungsfenster und fragt den Benutzer
    answer = messagebox.askyesno("Bestätigung", "Möchtest du wirklich deinen Spielstand zurücksetzen?")
    
    if answer:  # Wenn der Benutzer auf "Ja" klickt
        reset_data()  # Reset-Daten aufrufen
        result_label.config(text="Daten wurden zurückgesetzt.")
    else:
        result_label.config(text="Zurücksetzen abgebrochen.")


if getattr(sys, 'frozen', False):
    exe_path = sys._MEIPASS  
else:
    exe_path = os.path.dirname(os.path.abspath(__file__))


image_path = os.path.join(exe_path, "images")
filename = os.path.join(exe_path, "words_Deutsch.txt")
words = filter_words(filename)
quotes_file = os.path.join(exe_path, "quotes.txt")
quotes = filter_quotes(quotes_file)
mmr_file = os.path.join(exe_path, "mmr.txt")
winstreak_file = os.path.join(exe_path, "winstreak.txt")
highscore_file = os.path.join(exe_path, "highscore.txt")
coins_file = os.path.join(exe_path, "coins.txt")

log_file_succ = os.path.join(exe_path, "game_log_success.txt")
log_file_diff = os.path.join(exe_path, "game_log_difficulty.txt")
log_file_mmr = os.path.join(exe_path, "game_log_mmr.txt") 

selected_language = "Deutsch"
current_word = ""
game_over = True
display_word = []
guessed_letters = []
mistake_count = 0
word_difficulty = 0
mmr_change = 0
winstreak = 0
highscore = 0
coins = 0
rank = "Bronze"

load_mmr()  
load_winstreak()
load_highscore()
load_coins()

root = Tk()
root.title("Galgenraten Spiel")
root.geometry("600x925")
root.configure(bg='#212121')

# Start Frame
start_frame = Frame(root, bg='#212121')
start_frame.pack()

random_quote = random.choice(quotes)
quote_label = Label(start_frame, text=random_quote, wraplength=300,fg='#f0f0f0', bg='#212121', font=('Helvetica', 12))
quote_label.pack(pady=20)

language_var = StringVar()
language_var.set("Deutsch")
    
languages = ["Deutsch", "Englisch", "Französisch", "Spanisch", "Chaos"]

language_menu = ttk.Combobox(start_frame, textvariable=language_var, values=languages)
language_menu.bind("<<ComboboxSelected>>", on_language_change)
language_menu.pack(pady=10)

style = ttk.Style()
style.configure("TButton", font=('Helvetica', 12), padding=10)
style.configure("TLabel", font=('Helvetica', 12), background='#212121')


start_button = ttk.Button(start_frame, text="Start", width=26, command=start_game)
start_button.pack(pady=20)

start_label = Label(start_frame, text="Version: 1.08", wraplength=300,fg='#f0f0f0', bg='#212121', font=('Helvetica', 10))
start_label.pack(pady=20)

# Game Frame
game_frame = Frame(root, bg='#212121')

reset_button = Button(root, text="Reset", command=confirm_reset, width=5, height=1)  # Button kleiner machen
reset_button.place(relx=1.0, rely=0.0, anchor="ne") 

label_rank =Label(game_frame, text="",fg='#f0f0f0', bg='#212121', font=('Helvetica', 15))
label_rank.pack(pady=10)

right_frame = Frame(game_frame, bg='#212121')
right_frame.pack(side=RIGHT, padx=10, pady=10)

# Label für das Bild
label_image = Label(right_frame, bg='#212121')
label_image.pack(pady=10)  # Nur pady für Abstand verwenden

# Label für falsche Buchstaben unter dem Bild
wrong_letters_label = Label(right_frame, text="Falsche Buchstaben: \n ")
wrong_letters_label.pack(pady=(0, 10)) 
label = Label(game_frame, text="Drücke den Knopf, um ein zufälliges Wort auszuwählen", wraplength=300,fg='#f0f0f0', bg='#212121', font=('Helvetica', 12))
label.pack(pady=10)

difficulty_frame = Frame(game_frame, bg='#212121')
difficulty_frame.pack(pady=10)

label_difficulty = Label(difficulty_frame, text="Schwierigkeit",fg='#f0f0f0', bg='#212121', font=('Helvetica', 12))
label_difficulty.pack(side=LEFT)

label_stars = Label(difficulty_frame, text="", bg='#212121', font=('Helvetica', 12), fg='gold')
label_stars.pack(side=LEFT)

# Entry Style
entry_style = ttk.Style()
entry_style.configure("TEntry", padding=5, foreground='#212121', fieldbackground='#666666', bordercolor='#f0f0f0')

# Eingabefenster mit Entry Style
entry = ttk.Entry(game_frame,style="TEntry",font=('Helvetica', 12), width=2, justify='center')
entry.pack(pady=10, ipadx=5, ipady=5)  # ipadx und ipady für Innenabstände
entry.bind("<Return>", guess_letter)

guess_button = ttk.Button(game_frame, text="Rate den Buchstaben", width=26, command=guess_letter)
guess_button.pack(pady=5)

word_button = ttk.Button(game_frame, text="Wähle ein zufälliges Wort", width=26, command=choose_random_word)
word_button.pack(pady=10)


result_label = Label(game_frame, text="",fg='#f0f0f0', bg='#212121', font=('Helvetica', 12))
result_label.pack(pady=10)

tip_button = ttk.Button(game_frame, text="Tipp (50 Münzen)", width=26, command=reveal_random_letter)
tip_button.pack(pady=5)


mmr_label = Label(game_frame, text=f"MMR: {mmr_points}",fg='#f0f0f0', bg='#212121', font=('Helvetica', 12))
mmr_label.pack(pady=10)

mmr_change_label = Label(game_frame, text="0 MMR", wraplength=300,fg='#f0f0f0', bg='#212121', font=('Helvetica', 12))
mmr_change_label.pack(pady=1)

winstreak_label = Label(game_frame, text="", fg='#f0f0f0',bg='#212121', font=('Helvetica', 12))
winstreak_label.pack(pady=5)

highscore_label = Label(game_frame, text=f"Highscore: {highscore}", fg='#f0f0f0', bg='#212121', font=('Helvetica', 10))
highscore_label.pack(pady=10)

coins_label = Label(game_frame, text=f"{coins} ◎", fg='#f0f0f0', bg='#212121', font=('Helvetica', 10))
coins_label.place (relx= 1.0, rely= 0.0, anchor= 'ne')

show_image("0.png")

root.mainloop()

#TODO erledigt
#Bei Tipp wird ein Buchstabe aufgedeckt, den kannes aber mehrmals geben, die werden dann nicht aufgedeckt und können auch nicht aufgedeckt werden, weil wurde ja schon erraten bruder