import streamlit as st
import pandas as pd
from rapidfuzz import fuzz, process
import unidecode

# -------------------------------
# Charger le fichier CSV déjà présent dans l'app
# -------------------------------
@st.cache_data
def load_data():
    # Remplace "latin1" par "utf-8" si ton CSV est UTF-8
    return pd.read_csv("liste_electorale.csv", encoding="latin1")

data = load_data()

# -------------------------------
# Titre de l'application
# -------------------------------
st.title("📋 Vérification de l'inscription sur la liste électorale")

# -------------------------------
# Champ de recherche
# -------------------------------
nom = st.text_input("Entrez votre nom de famille (Last Name) :")

if st.button("Vérifier"):
    if nom.strip() == "":
        st.warning("Veuillez entrer un nom avant de vérifier.")
    else:
        # Normalisation du nom saisi et de la colonne Nom
        nom_saisi = unidecode.unidecode(nom.lower().strip())
        data["Nom_normalise"] = data["Nom"].apply(lambda x: unidecode.unidecode(str(x).lower().strip()))

        # -------------------------------
        # 1. Recherche exacte
        # -------------------------------
        exact_matches = [n for n in data["Nom"] if unidecode.unidecode(n.lower().strip()) == nom_saisi]

        # -------------------------------
        # 2. Recherche partielle
        # -------------------------------
        partial_matches = [n for n in data["Nom"] if nom_saisi in unidecode.unidecode(n.lower().strip())]

        # -------------------------------
        # 3. Recherche fuzzy (tolérance aux fautes)
        # -------------------------------
        results = process.extract(nom_saisi, data["Nom"].tolist(), scorer=fuzz.partial_ratio, limit=50)
        fuzzy_matches = [r[0] for r in results if r[1] >= 70]

        # -------------------------------
        # Fusionner tous les résultats sans doublons
        # -------------------------------
        all_matches = list(set(exact_matches + partial_matches + fuzzy_matches))

        if all_matches:
            st.success(f"✅ {len(all_matches)} résultat(s) trouvé(s) pour : {nom}")
            st.dataframe(pd.DataFrame(all_matches, columns=["Nom"]))
        else:
            st.error("❌ Aucun résultat trouvé. Vérifiez l'orthographe ou contactez le secrétariat.")
