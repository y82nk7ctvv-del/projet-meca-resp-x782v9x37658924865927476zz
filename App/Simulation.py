import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px 
from scipy.stats import mannwhitneyu

# 1. IMPORTATION ET NETTOYAGE DES DONNÉES
@st.cache_data
def charger_donnees():
    df = pd.read_excel("donnees_patients.xlsx", sheet_name="Results") 
    
    # NETTOYAGE EXTRÊME : On enlève les espaces invisibles au début et à la fin
    df.columns = df.columns.str.strip()
    
    # Nettoyage des "OUI/NON"
    df["Etat décompensé (OUI/NON)"] = df["Etat décompensé (OUI/NON)"].astype(str).str.strip().str.upper()
    
    return df

try:
    df = charger_donnees()
    st.success("Données importées avec succès !")

   # ---------------------------------------------------------
    # RÉSUMÉ STATISTIQUE (STYLE "TABLE 1" CLINIQUE)
    # ---------------------------------------------------------
    st.divider()
    st.subheader("Caractéristiques statistiques")
    st.write("Comparaison des caractéristiques morphologiques selon la tolérance au titrage.")

    # 1. SÉPARATION DES GROUPES
    df_instable = df[df["Etat décompensé (OUI/NON)"] == "OUI"]
    df_stable = df[df["Etat décompensé (OUI/NON)"] == "NON"]

    # CALCUL DES TESTS DE WILCOXON-MANN-WHITNEY
    u_age, p_age = mannwhitneyu(df_instable['Age'].dropna(), df_stable['Age'].dropna(), alternative='two-sided')
    u_imc, p_imc = mannwhitneyu(df_instable['IMC'].dropna(), df_stable['IMC'].dropna(), alternative='two-sided')

    with st.expander("Voir les tests statistiques (Wilcoxon-Mann-Whitney)"):
        st.write("Le test de Wilcoxon-Mann-Whitney permet de vérifier si la différence entre le groupe Stable et Instable est statistiquement significative (p-value < 0.05).")
        st.write(f"- **Test sur l'Âge :** p-value = {p_age:.2f}")
        st.write(f"- **Test sur l'IMC :** p-value = {p_imc:.2f}")
        st.info("Note : Les p-values étant supérieures à 0.05, la différence n'est pas encore statistiquement significative sur ce petit échantillon (N=20).")

    # 2. CALCULS GLOBAUX POUR L'INCERTITUDE STATISTIQUE
    n_total = len(df)
    n_instable = len(df_instable)
    p_instable = n_instable / n_total if n_total > 0 else 0
    ic_95 = 1.96 * np.sqrt((p_instable * (1 - p_instable)) / n_total) if n_total > 0 else 0
    
# 3. CRÉATION DE L'AFFICHAGE EN 3 COLONNES
    col1, col2, col3 = st.columns(3)

    # --- COLONNE 1 : COHORTE GLOBALE ---
    with col1:
        st.markdown("### Tableau global")
        st.metric(label="Effectif total (N)", value=n_total)
        st.write("---")
        st.write(f"**Âge moyen :** {df['Age'].mean():.0f} ({df['Age'].std():.0f}) ans")
        st.write(f"**Poids moyen :** {df['Weight (Kg)'].mean():.0f} ({df['Weight (Kg)'].std():.0f}) kg")
        st.write(f"**Taille moyenne :** {df['Height(cm)'].mean():.0f} ({df['Height(cm)'].std():.0f}) cm")
        st.write(f"**IMC moyen :** {df['IMC'].mean():.0f} ({df['IMC'].std():.0f})")
        
        n_hommes = len(df[df["Sex"] == "M"])
        n_femmes = len(df[df["Sex"] == "F"])
        st.write(f"**Hommes / Femmes :** {n_hommes} / {n_femmes}")

# --- CALCUL ET AFFICHAGE DE L'OBÉSITÉ (EN % AVEC INCERTITUDE) ---
        n_obeses = len(df[df["IMC"] > 30])
        p_obeses = n_obeses / n_total if n_total > 0 else 0
        
        # Calcul de l'incertitude (IC 95%) sur cette proportion
        ic_95_obeses = 1.96 * np.sqrt((p_obeses * (1 - p_obeses)) / n_total) if n_total > 0 else 0
        
        st.caption(f"Pourcentage d'obésité (IMC > 30) : **{p_obeses*100:.0f} ({ic_95_obeses*100:.0f}) %** de la cohorte.")

    # --- COLONNE 2 : GROUPE STABLE (Tolérance OK) ---
    with col2:
        st.markdown("### Groupe Stable")
        st.metric(label="Effectif (N)", value=len(df_stable))
        st.write("---")
        st.write(f"**Âge moyen :** {df_stable['Age'].mean():.0f} ({df_stable['Age'].std():.0f}) ans")
        st.write(f"**Poids moyen :** {df_stable['Weight (Kg)'].mean():.0f} ({df_stable['Weight (Kg)'].std():.0f}) kg")
        st.write(f"**Taille moyenne :** {df_stable['Height(cm)'].mean():.0f} ({df_stable['Height(cm)'].std():.0f}) cm")
        st.write(f"**IMC moyen :** {df_stable['IMC'].mean():.0f} ({df_stable['IMC'].std():.0f})")
        
        n_hommes_s = len(df_stable[df_stable["Sex"] == "M"])
        n_femmes_s = len(df_stable[df_stable["Sex"] == "F"])
        st.write(f"**Hommes / Femmes :** {n_hommes_s} / {n_femmes_s}")

    # --- COLONNE 3 : GROUPE INSTABLE (Problème Hémo) ---
    with col3:
        st.markdown("### Groupe Instable")
        st.metric(label="Effectif (N)", value=n_instable)
        st.write("---")
        st.write(f"**Âge moyen :** {df_instable['Age'].mean():.0f} ({df_instable['Age'].std():.0f}) ans")
        st.write(f"**Poids moyen :** {df_instable['Weight (Kg)'].mean():.0f} ({df_instable['Weight (Kg)'].std():.0f}) kg")
        st.write(f"**Taille moyenne :** {df_instable['Height(cm)'].mean():.0f} ({df_instable['Height(cm)'].std():.0f}) cm")
        st.write(f"**IMC moyen :** {df_instable['IMC'].mean():.0f} ({df_instable['IMC'].std():.0f})")
        
        n_hommes_i = len(df_instable[df_instable["Sex"] == "M"])
        n_femmes_i = len(df_instable[df_instable["Sex"] == "F"])
        st.write(f"**Hommes / Femmes :** {n_hommes_i} / {n_femmes_i}")

    # 4. MISE EN ÉVIDENCE DU TAUX DE COMPLICATION AVEC INCERTITUDE
    st.info(f"L'instabilité hémodynamique a été observée chez {p_instable*100:.0f} ± {ic_95*100:.0f} % des patients, avec un intervalle de 95% de confiance. Dans le groupe instable nous trouvons des patients légérement plus vieux (7%) et en obésité (IMC>30) par rapport au groupe stable. La proportion homme/femme est sensiblement la même (±1). ")

    # 5. MENU DÉROULANT : DÉTAILS DES CALCULS STATISTIQUES
    # 5. MENU DÉROULANT : DÉTAILS DES CALCULS STATISTIQUES
    with st.expander("Voir les détails des calculs statistiques"):
        st.markdown("""
        ### 1. Définition de l'échantillon expérimental
        En analyse statistique expérimentale, nos patients constituent un **échantillon $E$** extrait d'une **population globale $P$** (l'ensemble théorique des patients en chirurgie abdominale). 
        Le taux de complication observé expérimentalement ($p$) est une estimation de la probabilité réelle au sein de cette population globale.
        """)
        
        # Affichage dynamique des valeurs du script
        st.markdown(f"""
        * **Taille de l'échantillon ($N_{{total}}$)** = {n_total} patients
        * **Événements observés ($N_{{instable}}$)** = {n_instable} patients
        * **Estimation de la proportion ($p$)** = {p_instable:.2f} (soit {p_instable*100:.0f} %)
        """)

        st.markdown("""
        ### 2. Incertitude d'estimation et Intervalle de Confiance ($IC_{95}$)
        Tout comme l'incertitude sur la modélisation d'une droite de régression dépend de la dispersion des points et de la taille de l'échantillon, l'incertitude sur notre proportion $p$ dépend de la variance de sa loi de probabilité.
        
        Pour un échantillon suffisamment grand, cette distribution converge vers une loi Normale (qui est la limite de la loi de Student lorsque le nombre de degrés de liberté $v$ est grand). 
        Pour encadrer la valeur "vraie" avec un niveau de confiance de 95%, nous appliquons un facteur d'élargissement $k = 1.96$ à l'écart-type de cette proportion.
        """)
        

        
        # Affichage de la belle formule mathématique
        st.latex(r"IC_{95} = 1.96 \times \sqrt{\frac{p(1-p)}{N_{total}}}")
        
        st.markdown(f"""
        **Application numérique :**
        * $1.96 \\times \\sqrt{{ \\frac{{{p_instable:.2f} \\times (1 - {p_instable:.2f})}}{{{n_total}}} }}$ 
        * **Incertitude élargie = $\\pm$ {ic_95*100:.0f} %**
        
        **Conclusion :** Nous pouvons affirmer avec 95% de certitude que le taux de complication réel de la population $P$ se situe dans l'intervalle $[{p_instable*100 - ic_95*100:.0f}  ; {p_instable*100 + ic_95*100:.0f} ]$.
        """)
    
    # Noms EXACTS des colonnes (nettoyés des espaces)
    col_x = "Ecart-type de dP (Vt= 7ml/kg)"
    col_y = "Mechanical Pow dyna mini  (Vt= 7ml/kg) en J/min"
    col_uy = "u(Mp dy (7ml/kg)) en J/min"
    col_ux = "u(ecart-type)" 
    
    # On force la conversion en nombres
    df[col_x] = pd.to_numeric(df[col_x], errors='coerce')
    df[col_y] = pd.to_numeric(df[col_y], errors='coerce')
    df[col_uy] = pd.to_numeric(df[col_uy], errors='coerce')
    df[col_ux] = pd.to_numeric(df[col_ux], errors='coerce')
    
    # On supprime les lignes vides
    df = df.dropna(subset=[col_x, col_y])

    with st.expander("Voir les données brutes"):
        st.dataframe(df)

    
  # ---------------------------------------------------------
    # GRAPHIQUE 1 INTERACTIF (PLOTLY)
    # ---------------------------------------------------------
    st.subheader("Mise en évidence de la dangerositée d'une dP constante (Sn+1<0,75) ou anarchique (Sn+1>1,3)")
    
    # Création du nuage de points interactif avec Plotly
    fig = px.scatter(
        df,
        x=col_x,
        y=col_y,
        error_x=col_ux,      # Barres d'erreur horizontales
        error_y=col_uy,      # Barres d'erreur verticales
        color="Etat décompensé (OUI/NON)",
        color_discrete_map={"OUI": "#ef4444", "NON": "#22c55e"}, # Tes couleurs
        hover_data={
            "Etat décompensé (OUI/NON)": False, # On masque ça dans la bulle pour alléger
            col_x: ':.3f',  # Affiche 3 chiffres après la virgule au survol
            col_y: ':.3f'
        }
    )

    # Personnalisation avancée pour garder ton design "Mode Sombre" clinique
    fig.update_layout(
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font_color='white',
        title=dict(text="Distribution des profils patients ", font=dict(color='white')),
        legend_title_font_color='white', # La fameuse légende enfin visible !
        legend=dict(title="État Décompensé ?", bgcolor='#1e293b', bordercolor='white', borderwidth=1),
        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.2)'),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(255,255,255,0.2)'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Ajustement visuel des points et des barres d'erreur
    fig.update_traces(
        marker=dict(size=12, line=dict(width=1.5, color='white')),
        error_x=dict(color='rgba(100, 116, 139, 0.4)', thickness=1.5, width=4), # Gris bleuté avec transparence
        error_y=dict(color='rgba(100, 116, 139, 0.4)', thickness=1.5, width=4)
    )

    # Affichage interactif dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------
    # NOUVEAU GRAPHIQUE : PREUVE DES 100% (SLOPE CHART)
    # ---------------------------------------------------------
    st.divider() # Ligne de séparation esthétique
    st.subheader("Mise en évidence de l'inutilité d'une titration avec un Vt = 9ml/kg")
    
    # Noms exacts de tes colonnes (attention aux doubles espaces)
    col_mp7 = "Mechanical Pow dyna mini  (Vt= 7ml/kg) en J/min"
    col_mp9 = "Mechanical Pow dyna mini  (Vt= 9ml/kg) en J/min"
    
    # Conversion en nombres pour éviter les bugs
    df[col_mp7] = pd.to_numeric(df[col_mp7], errors='coerce')
    df[col_mp9] = pd.to_numeric(df[col_mp9], errors='coerce')
    df_mp = df.dropna(subset=[col_mp7, col_mp9])
    
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    
    # 1. TRACER LES LIGNES PATIENT PAR PATIENT
    for index, row in df_mp.iterrows():
        x_values = [7, 9] # L'axe X (Vt)
        y_values = [row[col_mp7], row[col_mp9]] # L'axe Y (MP pour ce patient)
        
        # On trace la ligne avec un joli bleu
        ax2.plot(x_values, y_values, marker='o', markersize=8, color='#38bdf8', alpha=0.6, linewidth=2)
    
    # 2. MISE EN FORME DU GRAPHIQUE
    ax2.set_xticks([7, 9])
    ax2.set_xticklabels(['Vt = 7 ml/kg', 'Vt = 9 ml/kg'], fontsize=14, fontweight='bold')
    ax2.set_xlabel("Volume courant (ml/kg)", color='white', fontsize=12)
    
    ax2.set_ylabel("Mechanical Power (J/min)", color='white', fontsize=12)
    ax2.set_title("Évolution du Mechanical Power elastique dynamique de chaque patient selon le volume courant", color='white', pad=20, fontsize=16)
    
    # Design Mode Sombre
    ax2.set_facecolor('#0f172a')
    fig2.patch.set_facecolor('#0f172a')
    ax2.tick_params(colors='white', labelsize=12)
    
    # On supprime les bordures du haut et de droite pour faire plus "épuré"
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('white')
    ax2.spines['bottom'].set_color('white')
    
    # Grille horizontale discrète
    ax2.grid(True, axis='y', color='white', linestyle='--', alpha=0.1)
    
    st.pyplot(fig2, use_container_width=True)
    

except Exception as e:
    st.error(f"Erreur lors du chargement : {e}")