import streamlit as st
import requests

API = "https://movie-recommendation-system-v068.onrender.com"

st.set_page_config(page_title="Movie Recommender", layout="wide")

# ---------- NETFLIX STYLE ----------
st.markdown("""
<style>
.stApp {
    background-color: #0b0b0b;
    color: white;
}

h1 {
    color: #E50914;
    text-align: center;
}

img {
    border-radius: 10px;
}

img:hover {
    transform: scale(1.05);
    transition: 0.3s;
}

.stButton button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='margin-bottom:30px;'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)

.stButton button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1>NETFLIX AI RECOMMENDER</h1>", unsafe_allow_html=True)

st.write("")

# ---------- TRENDING MOVIES ----------
st.subheader("🔥 Trending Movies")

try:
    trending = requests.get(f"{API}/home?category=popular").json()

    cols = st.columns(6)

    for i, m in enumerate(trending[:6]):
        with cols[i]:
            if m["poster_url"]:
                st.image(m["poster_url"])
                st.caption(m["title"])
except:
    st.warning("Trending movies unavailable")

st.divider()

# ---------- SEARCH ----------
st.subheader("🔍 Search a Movie")

movie = st.text_input("Enter movie name")

if st.button("Recommend"):

    url = f"{API}/movie/search?query={movie}"
    res = requests.get(url)

    if res.status_code == 200:

        data = res.json()

        # ---------- SELECTED MOVIE ----------
        st.subheader("🎬 Selected Movie")

        m = data["movie_details"]

        col1, col2 = st.columns([1, 2])

        with col1:
            if m["poster_url"]:
                st.image(m["poster_url"], width=250)

        with col2:
            st.write("###", m["title"])
            st.write(m["overview"])

        st.divider()

        # ---------- RECOMMENDATIONS ----------
        st.subheader("🔥 Recommended Movies")

        recs = data["tfidf_recommendations"]

        cols = st.columns(5)

        for i, r in enumerate(recs):
            with cols[i % 5]:
                if r["tmdb"] and r["tmdb"]["poster_url"]:
                    st.image(r["tmdb"]["poster_url"])
                    st.caption(r["title"])

    else:

        st.error("Movie not found")

