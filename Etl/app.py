import streamlit as st
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clinique des Nuits Complètes",
    page_icon="🌙",
    layout="wide",
)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #21262d; }
    .kpi-card {
        background: #161b22; border: 1px solid #21262d; border-radius: 10px;
        padding: 1.1rem 1.3rem; margin-bottom: 0.5rem;
    }
    .kpi-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1.5px; color: #7d8590; margin-bottom: 4px; }
    .kpi-value { font-size: 1.8rem; font-weight: 600; color: #e6edf3; line-height: 1; }
    .kpi-unit  { font-size: 0.75rem; color: #7d8590; margin-left: 3px; }
    .badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:0.7rem; font-weight:600; margin-top:4px; }
    .badge-green  { background:#0d4429; color:#3fb950; }
    .badge-orange { background:#3d2107; color:#f0883e; }
    .badge-red    { background:#3d0c0c; color:#f85149; }
    .badge-blue   { background:#0c2d4a; color:#58a6ff; }
    .section-header {
        font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px;
        color: #7d8590; border-bottom: 1px solid #21262d;
        padding-bottom: 4px; margin: 1.5rem 0 1rem 0;
    }
    div[data-testid="stMetric"] { background:#161b22; border:1px solid #21262d; border-radius:10px; padding:0.8rem 1rem; }
    div[data-testid="stMetric"] label { color:#7d8590 !important; }
    .login-box { max-width: 400px; margin: 5rem auto; padding: 2rem; background:#161b22; border:1px solid #21262d; border-radius:12px; }
</style>
""", unsafe_allow_html=True)


# ── Connexion MySQL ───────────────────────────────────────────────────────────
@st.cache_resource
def get_conn():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3333)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "cliniquearles"),
    )

def query(sql, params=None):
    conn = get_conn()
    return pd.read_sql(sql, conn, params=params)



USERS = {
    "thomas.estrii@clinique-sommeil-arles.fr":    {"password": "medecin1", "role": "medecin",   "id": 1,  "nom": "Dr Estri Thomas"},
    "isabelle.faure@clinique-sommeil-arles.fr":   {"password": "medecin2", "role": "medecin",   "id": 2,  "nom": "Dr Faure Isabelle"},
    "nathalie.roux@clinique-sommeil-arles.fr":    {"password": "infirmier1","role": "infirmier", "id": 8,  "nom": "Roux Nathalie"},
    "sophie.martin@clinique-sommeil-arles.fr":    {"password": "infirmier2","role": "infirmier", "id": 9,  "nom": "Martin Sophie"},
    "admin@clinique-sommeil-arles.fr":            {"password": "admin2024", "role": "admin",     "id": None,"nom": "Administrateur"},
}


# ── Login ─────────────────────────────────────────────────────────────────────
def show_login():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("## 🌙 Clinique des Nuits Complètes")
    st.markdown("Connexion au portail médical")
    st.markdown("---")
    email = st.text_input("Email professionnel", placeholder="prenom.nom@clinique-sommeil-arles.fr")
    pwd   = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter", use_container_width=True):
        user = USERS.get(email)
        if user and user["password"] == pwd:
            st.session_state.authenticated = True
            st.session_state.role          = user["role"]
            st.session_state.user_nom      = user["nom"]
            st.session_state.user_id       = user["id"]
            st.rerun()
        else:
            st.error("Email ou mot de passe incorrect.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Comptes de test → medecin : thomas.estrii@... / medecin1 | infirmier : nathalie.roux@... / infirmier1")


# ── Helpers sévérité ─────────────────────────────────────────────────────────
def iah_badge(iah):
    if iah is None:
        return '<span class="badge badge-blue">N/A</span>'
    iah = float(iah)
    if iah < 5:   return f'<span class="badge badge-green">Normal ({iah:.1f})</span>'
    if iah < 15:  return f'<span class="badge badge-orange">Léger ({iah:.1f})</span>'
    if iah < 30:  return f'<span class="badge badge-red">Modéré ({iah:.1f})</span>'
    return f'<span class="badge badge-red">⚠ Sévère ({iah:.1f})</span>'

def spo2_badge(v):
    if v is None: return ""
    v = float(v)
    cls = "badge-green" if v >= 95 else "badge-orange" if v >= 90 else "badge-red"
    return f'<span class="badge {cls}">{v:.1f}%</span>'


# ── Pages ─────────────────────────────────────────────────────────────────────

def page_patients():
    st.markdown('<div class="section-header">Liste des patients</div>', unsafe_allow_html=True)
    df = query("""
        SELECT p.id_patient, CONCAT(p.prenom,' ',p.nom) AS patient,
               p.date_naissance,
               TIMESTAMPDIFF(YEAR, p.date_naissance, CURDATE()) AS age,
               p.sexe, p.imc_initial, p.profession,
               IF(p.fumeur, 'Oui','Non') AS fumeur,
               p.niveau_activite,
               IF(p.actif,'Actif','Inactif') AS statut
        FROM patient p ORDER BY p.nom
    """)
    st.dataframe(df.set_index("id_patient"), use_container_width=True)

    st.markdown('<div class="section-header">Détail patient</div>', unsafe_allow_html=True)
    ids = df["id_patient"].tolist()
    noms = dict(zip(df["id_patient"], df["patient"]))
    sel = st.selectbox("Sélectionner un patient", ids, format_func=lambda x: noms[x])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Comorbidités**")
        df_co = query("""
            SELECT c.libelle, c.categorie, pc.date_diagnostic
            FROM patient_comorbidite pc
            JOIN comorbidite c ON c.id_comorbidite = pc.id_comorbidite
            WHERE pc.id_patient = %s
        """, params=(sel,))
        if df_co.empty:
            st.info("Aucune comorbidité enregistrée.")
        else:
            st.dataframe(df_co, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("**Dernier suivi**")
        df_sv = query("""
            SELECT date_suivi, poids, imc, tension_systolique, tension_diastolique,
                   statut_tabac, notes_evolution, statut_patient
            FROM suivi_patient WHERE id_patient = %s ORDER BY date_suivi DESC LIMIT 1
        """, params=(sel,))
        if df_sv.empty:
            st.info("Aucun suivi enregistré.")
        else:
            r = df_sv.iloc[0]
            st.metric("Poids", f"{r['poids']} kg")
            st.metric("IMC", f"{r['imc']}")
            st.metric("Tension", f"{r['tension_systolique']}/{r['tension_diastolique']} mmHg")
            st.caption(f"Statut tabac : {r['statut_tabac']} | {r['statut_patient']}")
            if r['notes_evolution']:
                st.markdown(f"> {r['notes_evolution']}")


def page_nuits():
    st.markdown('<div class="section-header">Nuits d\'étude — vue v_nuit_etude</div>', unsafe_allow_html=True)
    df = query("SELECT * FROM v_nuit_etude")
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown('<div class="section-header">Détail par nuit</div>', unsafe_allow_html=True)
    df_ids = query("""
        SELECT n.id_nuit, n.date_nuit, CONCAT(p.prenom,' ',p.nom) AS patient
        FROM nuit_etude n JOIN patient p ON p.id_patient = n.id_patient
        ORDER BY n.date_nuit DESC
    """)
    if df_ids.empty:
        st.info("Aucune nuit enregistrée.")
        return

    sel_nuit = st.selectbox(
        "Nuit",
        df_ids["id_nuit"].tolist(),
        format_func=lambda x: f"Nuit {x} — {df_ids[df_ids['id_nuit']==x]['patient'].values[0]} ({df_ids[df_ids['id_nuit']==x]['date_nuit'].values[0]})"
    )

    df_ev = query("""
        SELECT type_evenement, debut_sec, fin_sec, duree_sec, severite, decibels, spo2_avant, spo2_apres
        FROM evenement_respiratoire WHERE id_nuit = %s ORDER BY debut_sec
    """, params=(sel_nuit,))

    st.markdown(f"**{len(df_ev)} événements respiratoires**")
    if not df_ev.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Apnées",     int((df_ev["type_evenement"].str.contains("apn")).sum()))
        c2.metric("Hypopnées",  int((df_ev["type_evenement"]=="hypopnée").sum()))
        c3.metric("RERA",       int((df_ev["type_evenement"]=="RERA").sum()))
        c4.metric("Durée moy.", f"{df_ev['duree_sec'].mean():.0f} s")
        st.dataframe(df_ev, hide_index=True, use_container_width=True)

        st.markdown('<div class="section-header">Répartition des événements</div>', unsafe_allow_html=True)
        st.bar_chart(df_ev["type_evenement"].value_counts())


def page_resultats():
    st.markdown('<div class="section-header">Résultats des nuits</div>', unsafe_allow_html=True)
    df = query("""
        SELECT n.date_nuit,
               CONCAT(per.prenom,' ',per.nom) AS medecin_validateur,
               r.date_validation, r.iah, r.severite_iah,
               r.spo2_min, r.spo2_moy, r.spo2_mediane,
               r.nb_apnees, r.nb_hypopnees, r.nb_rera, r.nb_microeveils,
               r.duree_sommeil_min, r.duree_hypoxie_min,
               r.position_dominante, r.duree_apnee_moy_sec, r.duree_apnee_max_sec,
               r.decibels_max, r.decibels_moy, r.nb_ronflements_forts,
               r.commentaire_medical
        FROM resultat_nuit r
        JOIN nuit_etude n ON n.id_nuit = r.id_nuit
        JOIN personnel per ON per.id_personnel = r.id_medecin_validateur
        ORDER BY n.date_nuit DESC
    """)

    if df.empty:
        st.info("Aucun résultat disponible.")
        return

    # Affichage carte par nuit
    for _, r in df.iterrows():
        with st.expander(f"📅 Nuit du {r['date_nuit']} — validé par {r['medecin_validateur']}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">IAH</div>
                <div class="kpi-value">{float(r['iah']):.1f}<span class="kpi-unit">/h</span></div>
                {iah_badge(r['iah'])}
            </div>""", unsafe_allow_html=True)
            col2.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">SpO₂ min</div>
                <div class="kpi-value">{float(r['spo2_min']):.1f}<span class="kpi-unit">%</span></div>
                {spo2_badge(r['spo2_min'])}
            </div>""", unsafe_allow_html=True)
            col3.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Apnées</div>
                <div class="kpi-value">{int(r['nb_apnees'])}</div>
                <span class="badge badge-blue">+ {int(r['nb_hypopnees'])} hypopnées</span>
            </div>""", unsafe_allow_html=True)
            col4.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Durée sommeil</div>
                <div class="kpi-value">{int(r['duree_sommeil_min'])}<span class="kpi-unit">min</span></div>
                <span class="badge badge-blue">Hypoxie : {float(r['duree_hypoxie_min']):.0f} min</span>
            </div>""", unsafe_allow_html=True)

            st.markdown("---")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("RERA",           int(r['nb_rera']))
            c2.metric("Micro-éveils",   int(r['nb_microeveils']))
            c3.metric("Position",       str(r['position_dominante']))
            c4.metric("Ronflements >70dB", int(r['nb_ronflements_forts']))
            c1.metric("SpO₂ moyenne",   f"{float(r['spo2_moy']):.1f}%")
            c2.metric("SpO₂ médiane",   f"{float(r['spo2_mediane']):.1f}%")
            c3.metric("Déc. max",       f"{float(r['decibels_max']):.0f} dB")
            c4.metric("Déc. moyen",     f"{float(r['decibels_moy']):.1f} dB")

            if r['commentaire_medical']:
                st.markdown(f"**Commentaire médical :** {r['commentaire_medical']}")

    st.markdown('<div class="section-header">Tableau comparatif</div>', unsafe_allow_html=True)
    st.dataframe(df, hide_index=True, use_container_width=True)


def page_appareils():
    st.markdown('<div class="section-header">Appareils PSG</div>', unsafe_allow_html=True)
    df_psg = query("""
        SELECT a.id_appareil, a.modele, a.fabricant, a.numero_serie,
               a.statut, a.localisation, a.date_installation,
               p.version_firmware, p.type_montage
        FROM appareil a
        JOIN appareil_psg p ON p.id_appareil = a.id_appareil
        ORDER BY a.id_appareil
    """)
    for s in ["actif", "maintenance", "hors service"]:
        sub = df_psg[df_psg["statut"] == s]
        if not sub.empty:
            badge = "badge-green" if s == "actif" else "badge-orange" if s == "maintenance" else "badge-red"
            st.markdown(f'<span class="badge {badge}">{s.upper()} — {len(sub)} appareils</span>', unsafe_allow_html=True)
    st.dataframe(df_psg.set_index("id_appareil"), use_container_width=True)

    st.markdown('<div class="section-header">Appareils CPAP</div>', unsafe_allow_html=True)
    df_cpap = query("""
        SELECT a.id_appareil, a.modele, a.fabricant, a.numero_serie,
               a.statut, a.localisation,
               CONCAT(p.prenom,' ',p.nom) AS patient,
               c.pression_initiale, c.type_masque, c.taille_masque
        FROM appareil a
        JOIN appareil_cpap c ON c.id_appareil = a.id_appareil
        LEFT JOIN patient p ON p.id_patient = c.id_patient
        ORDER BY a.id_appareil
    """)
    st.dataframe(df_cpap.set_index("id_appareil"), use_container_width=True)


def page_vue_suivi():
    st.markdown('<div class="section-header">Dernier suivi patient — vue v_dernier_suivi</div>', unsafe_allow_html=True)
    df = query("SELECT * FROM v_dernier_suivi")
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown('<div class="section-header">Derniers événements respiratoires — vue v_derniers_event_respi</div>', unsafe_allow_html=True)
    df2 = query("SELECT * FROM v_derniers_event_respi")
    st.dataframe(df2, hide_index=True, use_container_width=True)



def page_outputs():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(BASE_DIR, "outputs")

    if not os.path.exists(output_dir):
        st.error(f"Dossier outputs introuvable : {output_dir}")
        return

    # Détecter les nuits disponibles depuis les fichiers
    import glob, re
    fichiers = os.listdir(output_dir)
    nuits = sorted(set(
        int(m.group(1))
        for f in fichiers
        for m in [re.search(r'_(\d+)\.(?:png|txt)$', f)]
        if m
    ))

    if not nuits:
        st.info("Aucun fichier trouvé dans le dossier outputs/.")
        return

    sel = st.selectbox("Nuit", nuits, format_func=lambda x: f"Nuit {x}")

    # ── Rapport texte ──
    rapport_path = os.path.join(output_dir, f"rapport_medecin_nuit_{sel}.txt")
    if os.path.exists(rapport_path):
        st.markdown('<div class="section-header">Rapport médecin</div>', unsafe_allow_html=True)
        raw = open(rapport_path, "rb").read()
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                rapport = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        st.markdown(f'<div style="background:#161b22;border:1px solid #21262d;border-left:3px solid #58a6ff;border-radius:8px;padding:1rem 1.4rem;font-family:monospace;font-size:0.85rem;white-space:pre-wrap;color:#c9d1d9">{rapport}</div>', unsafe_allow_html=True)
        st.download_button("⬇ Télécharger le rapport", data=rapport,
                           file_name=f"rapport_medecin_nuit_{sel}.txt", mime="text/plain")

    # ── Courbes ──
    st.markdown('<div class="section-header">Courbes générées</div>', unsafe_allow_html=True)

    images = {
        "SpO₂": os.path.join(output_dir, f"courbe_spo2_nuit_{sel}.png"),
        "Débit nasal": os.path.join(output_dir, f"courbe_debit_nasal_nuit_{sel}.png"),
        "Ronflements": os.path.join(output_dir, f"ronflements{sel}_vs_temps.png"),
    }

    cols = st.columns(2)
    idx = 0
    for label, path in images.items():
        if os.path.exists(path):
            with cols[idx % 2]:
                st.image(path, caption=label, use_container_width=True)
            idx += 1
        else:
            with cols[idx % 2]:
                st.info(f"{label} — fichier non trouvé")
            idx += 1

    # ── Tous les fichiers disponibles ──
    with st.expander("Voir tous les fichiers outputs/"):
        for f in sorted(fichiers):
            fpath = os.path.join(output_dir, f)
            size = os.path.getsize(fpath)
            st.text(f"{f}  ({size:,} octets)")

# ── Main ──────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    show_login()
    st.stop()

role = st.session_state.role

# Sidebar
with st.sidebar:
    st.markdown(f"### 🌙 Portail médical")
    st.markdown(f"**{st.session_state.user_nom}**")
    role_label = {"medecin": "🩺 Médecin", "infirmier": "💉 Infirmier", "admin": "⚙️ Admin"}.get(role, role)
    st.caption(role_label)
    st.markdown("---")

    # Pages disponibles selon le rôle
    if role == "medecin":
        pages = ["Patients", "Nuits d'étude", "Résultats", "Appareils", "Vues de suivi", "Outputs"]
    elif role == "infirmier":
        pages = ["Patients", "Nuits d'étude", "Appareils", "Outputs"]
    else:  # admin
        pages = ["Patients", "Nuits d'étude", "Résultats", "Appareils", "Vues de suivi", "Outputs"]

    page = st.radio("Navigation", pages, label_visibility="collapsed")
    st.markdown("---")
    if st.button("Déconnexion"):
        for k in ["authenticated", "role", "user_nom", "user_id"]:
            st.session_state.pop(k, None)
        st.rerun()

# Header
st.markdown(f"# 🌙 {page}")
st.caption(f"Clinique des Nuits Complètes · Base MySQL `cliniquearles`")
st.divider()

# Routing
try:
    if page == "Patients":
        page_patients()
    elif page == "Nuits d'étude":
        page_nuits()
    elif page == "Résultats":
        if role == "infirmier":
            st.warning("Accès réservé aux médecins.")
        else:
            page_resultats()
    elif page == "Appareils":
        page_appareils()
    elif page == "Vues de suivi":
        page_vue_suivi()
    elif page == "Outputs":
        page_outputs()
except mysql.connector.Error as e:
    st.error(f"Erreur de connexion MySQL : {e}")
    st.info("Vérifiez que votre serveur MySQL est démarré et que le fichier `.env` est correct.")
    if st.button("Réessayer"):
        st.cache_resource.clear()
        st.rerun()