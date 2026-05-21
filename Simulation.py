

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np 

# 1. TITRE DE L'APPLICATION
st.title("Simulateur Interactif de Tolérance Hémodynamique")

# 2. CURSEURS INTERACTIFS (Inputs)
st.sidebar.header("Paramètres du Patient")

# Curseur définir la PAM initiale au repos 
pam_initiale = st.sidebar.slider("PAM de base (mmHg)", min_value=50, max_value=120, value=88)

# Curseur définir la dP du patient
dp = st.sidebar.slider("Driving Pressure (dP) [cmH2O]", min_value=3, max_value=20, value = 6)

# Curseur définir la PBW du patient
PBW = st.sidebar.slider("PBW", min_value=40, max_value=80, value=48)

# Remplacement du slider par un menu déroulant avec choix fixes
Vt = st.sidebar.selectbox("Vt facteur (ml/kg)", options=[7, 9], index=0)

# Curseur définir constante d'Hugo du patient
k = st.sidebar.slider("k", min_value= 0.0000 , max_value=0.1000, value=0.0400, step=0.0001, format="%.4f")


# 3. LE MOTEUR DE CALCUL 

# On définit la plage de PEEP (axe X de notre graphique, de 5 à 15 cmH2O)
peep_range = np.arange(5, 16, 1) # Un vecteur [5, 6, 7, ..., 15]


# Calcul de la pénalité hémodynamique POUR TOUS les points de PEEP d'un coup (grâce à numpy)
# Rappel de la formule physique unifiée : Penalty = k * PEEP * (Vt / dP)

delta_pam = k * peep_range * ((Vt*PBW) / dp)

# Calcul de la PAM théorique pour tous les points de PEEP
pam_range_theorique = pam_initiale - delta_pam


# 4. AFFICHAGE DES RÉSULTATS (Graphique et Alertes)

#A. Résumé ponctuel à PEEP Haute 
st.subheader("Prédiction à PEEP Haute (15 cmH2O)")
pam_max = pam_range_theorique[-1] # La PAM pour la dernière valeur de peep_range (PEEP 15)
st.metric(label="PAM Prédite à PEEP 15", value=f"{pam_max:.1f} mmHg")

if pam_max < 65:
    st.error("ALERTE : Risque de chute hémodynamique théorique à PEEP élevée (PAM < 65) !")
else:
    st.success(" Hémodynamique stable théorique.")

# --- B. Le Graphique Interactif (La Courbe) ---

st.subheader("Graphique")

fig, ax = plt.subplots(figsize=(10, 6))
couleur_ligne = '#2563eb' # Bleu électrique

# 1. La courbe principale (solide, bleue, sans transparence)
ax.plot(peep_range, pam_range_theorique, color=couleur_ligne, linewidth=4)

# 2. Le point de départ avec la valeur (à PEEP 15)
ax.plot(15, pam_range_theorique[-1], marker='o', markersize=12, color=couleur_ligne, markeredgecolor='white', markeredgewidth=2)
ax.text(14.8, pam_range_theorique[-1] + 1.5, f"{pam_range_theorique[-1]:.1f}", fontweight='bold', fontsize=12)

# 3. Ligne rouge en pointillés pour le seuil critique
ax.axhline(y=65, color='#dc2626', linestyle='--', linewidth=2)

# 4. L'EFFET OPAQUE ROUGE : Remplissage de la zone de danger (sous 65 mmHg)
# On colorie entre y=65 et y=40, sur toute la largeur (de x=5 à x=15)
ax.fill_between([5, 15], 65, 40, color='#dc2626', alpha=0.15)

# --- Mise en page du graphique ---
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

ax.set_xlabel('Niveau de PEEP (cmH2O)', fontsize=12, fontweight='bold', color='#4b5563')
ax.set_ylabel('PAM théorique [mmHg]', fontsize=12, fontweight='bold', color='#4b5563')
ax.set_title('Dynamique de la Tension Artérielle', fontsize=16, fontweight='bold', pad=20)

# Blocage de l'axe Y pour correspondre à ton image
ax.set_ylim(bottom=40, top=100) 
ax.set_xlim(left=5, right=15) 

ax.set_xticks(range(5, 16))

# Grille
ax.grid(axis='y', linestyle='-', alpha=0.3)
ax.grid(axis='x', linestyle='-', alpha=0.3)

# Affichage dans Streamlit
st.pyplot(fig)