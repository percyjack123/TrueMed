import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
import re
from datetime import datetime
from huggingface_hub import hf_hub_download
USE_OCR = False 
st.set_page_config(page_title="Medicine Legal Verifier", layout="wide")
st.title("Medicine Legal Authenticity Verification System")

@st.cache_resource
def load_all():
    
    model_path = hf_hub_download(
        repo_id="SKumarii/truemed-real-fake-model",
        filename="real_fake_model.h5"
    )
    model = tf.keras.models.load_model(model_path)

    
    medicine_metadata = pd.read_csv(
        "https://raw.githubusercontent.com/Supriyaranigouda/medicine-auth-system/main/medicine_metadata.csv"
    )
    manufacturer_registry = pd.read_csv(
        "https://raw.githubusercontent.com/Supriyaranigouda/medicine-auth-system/main/manufacturer_registry.csv"
    )
    batch_database = pd.read_csv(
        "https://raw.githubusercontent.com/Supriyaranigouda/medicine-auth-system/main/batch_database.csv"
    )

    for df in [medicine_metadata, manufacturer_registry, batch_database]:
        df.columns = df.columns.str.replace("\ufeff", "", regex=False).str.strip()

    medicine_metadata["brand_name"] = medicine_metadata["brand_name"].astype(str).str.lower().str.strip()
    batch_database["brand_name"] = batch_database["brand_name"].astype(str).str.lower().str.strip()
    batch_database["batch_number"] = batch_database["batch_number"].astype(str).str.upper().str.strip()
    manufacturer_registry["manufacturer"] = manufacturer_registry["manufacturer"].astype(str).str.strip()

    return model, medicine_metadata, manufacturer_registry, batch_database

model, medicine_metadata, manufacturer_registry, batch_database = load_all()

brand_name = st.selectbox(
    "Select Medicine Brand",
    sorted(medicine_metadata["brand_name"].unique())
)

valid_batches = batch_database[
    (batch_database["brand_name"] == brand_name) &
    (batch_database["valid"].astype(str).str.lower().isin(["yes", "true", "1"]))
]["batch_number"].tolist()

manual_batch = st.text_input(
    "Batch Number (auto-filled, editable)",
    value=valid_batches[0] if valid_batches else ""
)

uploaded_image = st.file_uploader(
    "Upload Medicine Packaging Image",
    type=["jpg", "jpeg", "png"]
)

if st.button("Verify Medicine"):

    if not uploaded_image:
        st.warning("Please upload a medicine image.")
        st.stop()

    image = Image.open(uploaded_image).convert("RGB")
    img = image.resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    prediction = model.predict(img_array)[0][0]
    visual_ok = prediction >= 0.75
    visual_status = "Visually Authentic" if visual_ok else "Visually Suspicious"

    extracted_text = ""

    dataset_batch = manual_batch.strip().upper() if manual_batch else None
    batch_match = dataset_batch in valid_batches if dataset_batch else False

    brand_row = medicine_metadata[medicine_metadata["brand_name"] == brand_name]
    manufacturer = brand_row.iloc[0]["manufacturer"]

    discontinued = bool(brand_row.iloc[0].get("is_discontinued", False))

    mfg_row = manufacturer_registry[
        manufacturer_registry["manufacturer"] == manufacturer
    ]
    manufacturer_approved = (
        not mfg_row.empty and
        str(mfg_row.iloc[0]["approved"]).strip().lower() in ["yes", "true", "1"]
    )

    batch_row = batch_database[
        (batch_database["brand_name"] == brand_name) &
        (batch_database["batch_number"] == dataset_batch)
    ]

    batch_valid = not batch_row.empty
    expired = False

    if batch_valid and "expiry_date" in batch_row.columns:
        try:
            expiry_date = datetime.strptime(
                str(batch_row.iloc[0]["expiry_date"]), "%Y-%m-%d"
            )
            expired = expiry_date < datetime.now()
        except:
            expired = False

    reasons = []

    if not visual_ok:
        reasons.append("Visual authenticity failed")
    if discontinued:
        reasons.append("Medicine is discontinued")
    if not manufacturer_approved:
        reasons.append("Manufacturer not approved")
    if not batch_match:
        reasons.append("Batch number mismatch")
    if not batch_valid:
        reasons.append("Invalid batch number")
    if expired:
        reasons.append("Medicine batch expired")

    verdict = "LEGALLY AUTHENTIC" if not reasons else "LEGALLY FAKE / SUSPICIOUS"

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, use_container_width=True)
        st.subheader("OCR Text")
        st.text("OCR disabled in cloud deployment")

    with col2:
        st.subheader("Verification Results")
        st.write(f"Visual AI Result: {visual_status}")
        st.write(f"Manufacturer: {manufacturer}")
        st.write(f"Manufacturer Approved: {'Yes' if manufacturer_approved else 'No'}")
        st.write(f"Batch Used: {dataset_batch}")
        st.write(f"Batch Valid: {'Yes' if batch_valid else 'No'}")
        st.write(f"Expired: {'Yes' if expired else 'No'}")

        st.divider()
        if not reasons:
            st.success(verdict)
        else:
            st.error(verdict)
            st.subheader("Reasons")
            for r in reasons:
                st.warning(r)
