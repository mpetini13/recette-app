from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

chemin_csv = r"C:\Users\PC\Documents\App\recettes.csv"

if not os.path.exists(chemin_csv):
    raise FileNotFoundError(f"Le fichier {chemin_csv} n'a pas été trouvé !")

recettes_df = pd.read_csv(chemin_csv)

if 'Plat' not in recettes_df.columns or 'Ingrédients' not in recettes_df.columns:
    raise ValueError("Le CSV doit avoir les colonnes 'Plat' et 'Ingrédients' !")


@app.route('/')
def home():
    recettes = recettes_df['Plat'].tolist()
    return render_template('index.html', recettes=recettes)


@app.route('/recettes')
def recette():
    plat = request.args.get('plat')
    if not plat:
        return "Aucun plat sélectionné"

    # Récupère les ingrédients correspondant au plat
    row = recettes_df[recettes_df['Plat'] == plat]
    if row.empty:
        return "Plat introuvable"

    ingredients = row['Ingrédients'].values[0].split(';')  # Séparer par ;
    return render_template('recette.html', plat=plat, ingredients=ingredients)


if __name__ == '__main__':
    app.run()