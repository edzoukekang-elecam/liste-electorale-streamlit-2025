# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Vérification Liste Électorale", layout="centered")
st.title("Vérification de l'inscription sur la liste électorale")
st.write("Entre ton nom pour vérifier votre éligibilité - Enter your last name to see if you are registered to vote")

# Upload CSV (admin)
st.sidebar.header("Administration")
csv_file = st.sidebar.file_uploader("Uploader la liste électorale (CSV)", type=["csv"])

if csv_file is not None:
    try:
        df = pd.read_csv(csv_file, dtype=str, sep=";")  # Point-virgule pour Excel français
    except Exception as e:
        st.sidebar.error(f"Erreur lecture CSV: {e}")
        st.stop()

    # Nettoyage colonnes
    df.columns = [c.strip() for c in df.columns]

    # Vérifier colonnes essentielles
    required = {"member_id", "first_name", "last_name", "email"}
    if not required.intersection(set(df.columns)):
        st.sidebar.warning("Le CSV doit contenir au moins une des colonnes : member_id, first_name, last_name, email")
    else:
        st.sidebar.success(f"Liste chargée. Nombre d'enregistrements : {len(df)}")

        # Recherche utilisateur
        query = st.text_input("Entrez numéro d'adhérent / nom complet / courriel", "")
        if st.button("Vérifier"):
            q = query.strip().lower()
            if q == "":
                st.info("Veuillez entrer une valeur pour vérifier.")
            else:
                # Recherche flexible
                # Recherche utilisateur
query = st.text_input("Entre ton nom pour vérifier votre éligibilité", "")
if st.button("Vérifier"):
    q = query.strip().lower()
    if q == "":
        st.info("Veuillez entrer une valeur pour vérifier.")
    else:
        # Recherche uniquement dans la colonne des noms
        mask = df["Nom / Last Name"].astype(str).str.lower().str.contains(q)

        results = df[mask]
        if results.empty:
            st.error("Aucun enregistrement correspondant trouvé. Si tu penses que c'est une erreur, contacte le secrétariat.")
        else:
            st.success(f"{len(results)} enregistrement(s) trouvé(s).")
            st.table(results.head(10))
else:
    st.info("Aucun fichier chargé. Demande au secrétariat d'uploader le fichier CSV via la barre latérale.")
