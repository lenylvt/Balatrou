import streamlit as st

st.set_page_config(page_title='Calculateur de Points de Poker', page_icon='🃏', layout='wide')

# CSS pour améliorer le style
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .player-button {
        background-color: #4CAF50; /* Vert */
        color: white;
        width: 100%;
        border: none;
        padding: 10px;
        text-align: left;
        font-size: 16px;
        margin: 2px 0;
        cursor: pointer;
        border-radius: 5px;
    }
    .player-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# Données des mains
mains = {
    'Paire': {'base_points': 10, 'multiplicateur': 2},
    'Double Paire': {'base_points': 20, 'multiplicateur': 2},
    'Brelan': {'base_points': 30, 'multiplicateur': 3},
    'Suite': {'base_points': 30, 'multiplicateur': 4},
    'Couleur (Flush)': {'base_points': 35, 'multiplicateur': 4},
    'Full (Main Pleine)': {'base_points': 40, 'multiplicateur': 4},
    'Carré': {'base_points': 60, 'multiplicateur': 7},
    'Quinte Flush': {'base_points': 100, 'multiplicateur': 8},
    'Quinte Flush Royale': {'base_points': 100, 'multiplicateur': 8}
}

# Initialisation des variables de session
if 'joueurs' not in st.session_state:
    st.session_state['joueurs'] = []
    st.session_state['scores'] = {}
    st.session_state['selected_player'] = None

# Barre latérale pour la gestion des joueurs
st.sidebar.title('🎴 Gestion des Joueurs')

# Section pour ajouter des joueurs
with st.sidebar:
    st.subheader('Ajouter un Joueur')
    # Utiliser une clé différente pour éviter les conflits
    nouveau_joueur = st.text_input('Nom du Joueur', key='nouveau_joueur_input')
    cols_add = st.columns(2)
    if cols_add[0].button('➕ Ajouter'):
        if nouveau_joueur:
            if nouveau_joueur not in st.session_state['joueurs']:
                st.session_state['joueurs'].append(nouveau_joueur)
                st.session_state['scores'][nouveau_joueur] = []
                st.success(f'Joueur {nouveau_joueur} ajouté !')
                st.session_state['selected_player'] = nouveau_joueur
                # Réinitialiser le champ de texte en rafraîchissant l'application
                st.rerun()
            else:
                st.warning('Ce joueur existe déjà.')
        else:
            st.warning('Veuillez entrer un nom de joueur.')

    # Boutons Reset All et Delete All côte à côte
    st.markdown('---')
    st.subheader('Options Globales')
    cols_reset = st.columns(2)
    if cols_reset[0].button('🔄 Reset '):
        for joueur in st.session_state['joueurs']:
            st.session_state['scores'][joueur] = []
        st.success('Tous les scores ont été réinitialisés.')
    if cols_reset[1].button('🗑️ Delete '):
        st.session_state['joueurs'] = []
        st.session_state['scores'] = {}
        st.session_state['selected_player'] = None
        st.success('Tous les joueurs ont été supprimés.')

    # Bouton Podium
    st.markdown('---')
    if st.button('🏆 Podium'):
        st.session_state['selected_player'] = 'PODIUM'

    # Liste des joueurs
    st.markdown('---')
    st.subheader('Liste des Joueurs')
    for joueur in st.session_state['joueurs']:
        if st.button(joueur, key=f'select_{joueur}'):
            st.session_state['selected_player'] = joueur

# Contenu principal
st.title('🃏 Calculateur de Points de Poker')

if st.session_state['selected_player'] == 'PODIUM':
    st.header('🏆 Podium des Joueurs')
    if st.session_state['joueurs']:
        total_scores = {joueur: sum(st.session_state['scores'][joueur]) for joueur in st.session_state['joueurs']}
        classement = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
        medals = ['🥇', '🥈', '🥉']
        for idx, (joueur, score) in enumerate(classement):
            medal = medals[idx] if idx < 3 else ''
            st.write(f'{medal} **{joueur}**: {score} points')
    else:
        st.info('Aucun joueur pour le moment.')
elif st.session_state['selected_player']:
    joueur = st.session_state['selected_player']
    st.header(f'👤 Joueur Sélectionné : {joueur}')
    st.divider()

    st.subheader('📝 Enregistrer une Main')
    main_selectionnee = st.selectbox('Type de Main', list(mains.keys()))

    # Demander les cartes selon le type de main
    cartes = []
    if main_selectionnee == 'Paire':
        carte = st.number_input('Valeur de la Carte', min_value=1, max_value=14, step=1, key='carte_paire')
        if carte:
            cartes = [carte, carte]
    elif main_selectionnee == 'Double Paire':
        carte1 = st.number_input('Première Paire', min_value=1, max_value=14, step=1, key='dp1')
        carte2 = st.number_input('Deuxième Paire', min_value=1, max_value=14, step=1, key='dp2')
        if carte1 and carte2:
            cartes = [carte1, carte1, carte2, carte2]
    elif main_selectionnee == 'Brelan':
        carte = st.number_input('Valeur de la Carte', min_value=1, max_value=14, step=1, key='carte_brelan')
        if carte:
            cartes = [carte, carte, carte]
    elif main_selectionnee == 'Full (Main Pleine)':
        brelan = st.number_input('Brelan (3 cartes identiques)', min_value=1, max_value=14, step=1, key='full_brelan')
        paire = st.number_input('Paire (2 cartes identiques)', min_value=1, max_value=14, step=1, key='full_paire')
        if brelan and paire:
            cartes = [brelan, brelan, brelan, paire, paire]
    elif main_selectionnee == 'Carré':
        carte = st.number_input('Valeur de la Carte', min_value=1, max_value=14, step=1, key='carte_carre')
        if carte:
            cartes = [carte]*4
    elif main_selectionnee in ['Suite', 'Couleur (Flush)', 'Quinte Flush', 'Quinte Flush Royale']:
        cartes_input = st.text_input('Valeurs des 5 Cartes (séparées par des virgules)', key='cartes_speciales')
        if cartes_input:
            try:
                cartes = [int(val.strip()) for val in cartes_input.split(',')]
                if len(cartes) != 5:
                    st.error('Vous devez entrer exactement 5 cartes.')
                    cartes = []
            except ValueError:
                st.error('Veuillez entrer des valeurs de cartes valides (nombres entiers).')
    else:
        cartes_input = st.text_input('Valeurs des Cartes (séparées par des virgules)', key='cartes_autres')
        if cartes_input:
            try:
                cartes = [int(val.strip()) for val in cartes_input.split(',')]
            except ValueError:
                st.error('Veuillez entrer des valeurs de cartes valides (nombres entiers).')

    # Bouton pour calculer et enregistrer les points
    if st.button('💾 Enregistrer les Points'):
        if cartes:
            base_points = mains[main_selectionnee]['base_points']
            multiplicateur = mains[main_selectionnee]['multiplicateur']
            somme_cartes = sum(cartes)
            total_points = (base_points + somme_cartes) * multiplicateur
            # Enregistrer les points pour le joueur
            st.session_state['scores'][joueur].append(total_points)
            st.success(f'Points enregistrés pour {joueur}: {total_points} points')
        else:
            st.warning('Veuillez entrer les valeurs des cartes.')

    # Historique des points
    st.subheader('📈 Historique des Points')
    if st.session_state['scores'][joueur]:
        # Affichage amélioré de l'historique des points
        historique = st.session_state['scores'][joueur]
        manches = list(range(1, len(historique)+1))
        df_historique = {'Manche': manches, 'Points': historique}
        st.table(df_historique)
    else:
        st.write('Aucun point enregistré pour le moment.')

    total_points = sum(st.session_state['scores'][joueur])
    st.write(f'## **Points Totaux : {total_points}**')
else:
    st.info('Veuillez sélectionner un joueur dans la barre latérale.')