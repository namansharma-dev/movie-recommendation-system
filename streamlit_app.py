import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TMDB_KEY = "73513875319b4848c5eefbc37386f001"

st.set_page_config(page_title="🍿Movie Recommender", layout="wide")

# ---------- REQUEST SESSION WITH RETRY ----------
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

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

.stButton button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("""
<div style="position:relative; text-align:center; margin-bottom:20px;">

<h1 style="color:#E50914;">🍿 MOVIE RECOMMENDER</h1>

<a href="https://github.com/namansharma-dev/movie-recommendation-system"
target="_blank"
style="position:absolute; right:0; top:10px;">

<button style="
background:#E50914;
color:white;
border:none;
padding:8px 16px;
border-radius:8px;
cursor:pointer;">
⭐ GitHub
</button>

</a>

</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- TRENDING MOVIES ----------
st.subheader("🔥 Trending Movies")

try:
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_KEY}"
    res = session.get(url, timeout=10)
    res.raise_for_status()

    data = res.json()
    trending = data.get("results", [])

    cols = st.columns(6)

    for i, m in enumerate(trending[:6]):
        with cols[i]:
            poster = m.get("poster_path")
            if poster:
                st.image("https://image.tmdb.org/t/p/w500" + poster)
                st.caption(m.get("title"))

except requests.exceptions.RequestException:
    st.warning("⚠️ Unable to fetch trending movies right now. Please refresh.")

st.divider()

# ---------- SEARCH ----------
st.subheader("🔍 Search a Movie")

movie = st.text_input("Enter movie name")

if st.button("Recommend"):

    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={movie}"
        res = session.get(search_url, timeout=10)
        res.raise_for_status()

        data = res.json()

        if data.get("results"):

            m = data["results"][0]

            st.subheader("🎬 Selected Movie")

            col1, col2 = st.columns([1,2])

            with col1:
                if m.get("poster_path"):
                    poster = "https://image.tmdb.org/t/p/w500" + m["poster_path"]
                    st.image(poster, width=250)

            with col2:
                st.write("###", m.get("title"))
                st.write(m.get("overview"))

            st.divider()

            # ---------- SIMILAR MOVIES ----------
            st.subheader("🔥 Similar Movies")

            movie_id = m["id"]

            rec_url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={TMDB_KEY}"

            rec_res = session.get(rec_url, timeout=10)
            rec_res.raise_for_status()

            rec_data = rec_res.json()
            recs = rec_data.get("results", [])

            cols = st.columns(5)

            for i, r in enumerate(recs[:5]):
                with cols[i % 5]:
                    if r.get("poster_path"):
                        poster = "https://image.tmdb.org/t/p/w500" + r["poster_path"]
                        st.image(poster)
                        st.caption(r.get("title"))

        else:
            st.error("Movie not found")

    except requests.exceptions.RequestException:
        st.error("API request failed. Please try again.")