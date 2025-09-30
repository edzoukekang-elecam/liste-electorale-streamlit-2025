# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Vérification Liste Électorale", layout="centered")
st.title("Vérification de l'inscription sur la liste électorale")
st.write("Entre ton nom pour vérifier votre éligibilité - Enter your last name to verify you are registered to vote")

# Upload CSV (barre latérale)
st.sidebar.header("Administration")
csv_file = st.sidebar.file_uploader("Uploader la liste électorale (CSV)", type=["csv"])

if csv_file is not None:
    try:
        df = pd.read_csv(csv_file, dtype=str, sep=";")  # point-virgule pour CSV français
    except Exception as e:
        st.sidebar.error(f"Erreur lecture CSV: {e}")
        st.stop()

    # Vérifier que la colonne essentielle est présente
    if "Nom / Last Name" not in df.columns:
        st.error("Le CSV doit contenir la colonne : Nom / Last Name")
    else:
        # Zone de recherche utilisateur
        query = st.text_input("Nom complet")
        if st.button("Vérifier"):
            q = query.strip().lower()
            if q == "":
                st.info("Veuillez entrer un nom pour vérifier.")
            else:
                # Recherche uniquement dans la colonne Nom / Last Name
                mask = df["Nom / Last Name"].astype(str).str.lower().str.contains(q)
                results = df[mask]

                if results.empty:
                    st.error("Aucun enregistrement correspondant trouvé. Si tu penses que c'est une erreur, contacte le secrétariat.")
                else:
                    st.success(f"{len(results)} enregistrement(s) trouvé(s).")
                    st.table(results.head(10))

else:
    st.info("Aucun fichier chargé. Demande au secrétariat d'uploader le fichier CSV via la barre latérale.")
