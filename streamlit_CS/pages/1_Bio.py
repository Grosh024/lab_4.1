import streamlit as st

st.title("👋 My Bio")

# ---------- TODO: Replace with your own info ----------
NAME = "Nathan Groshek"
PROGRAM = "BS Data Science/Machine Learning at MSU Denver"
INTRO = (
    "Hi, I'm Nathan, Im 34 years old, and I'm currently pursuing my bachelor's degree in Data Science and Machine Learning at MSU Denver. "
    "I'm passionate about using data to uncover insights and creating meaningful visualizations."
)
FUN_FACTS = [
    "I love hiking and exploring the outdoors.",
    "I’m learning advanced machine learning techniques.",
    "I want to build impactful data-driven applications.",
]
PHOTO_PATH = "streamlit_CS/assets/20250104_125255.jpg"  # Put a file in repo root or set a URL

from PIL import Image

# Open and rotate the image here (replace angle with the actual rotation needed, e.g., 90)
try:
    image = Image.open(PHOTO_PATH)
    image = image.rotate(-90, expand=True)  # Use positive/negative degrees as needed
    st.image(image, caption="Nathan Groshek", use_container_width=True)
except Exception:
    st.info("Add a photo named your_photo.jpg to the repo root, or change PHOTO_PATH.")


# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    try:
        st.image(PHOTO_PATH, caption=NAME, use_container_width=True)
    except Exception:
        st.info("Add a photo named `your_photo.jpg` to the repo root, or change PHOTO_PATH.")
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")
