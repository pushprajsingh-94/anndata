import streamlit as st
import plotly.graph_objects as go
from advisory import get_advisory
from predict import predict_prices
from auth import register_farmer, login_farmer, init_db

init_db()

if "farmer" not in st.session_state:
    st.session_state.farmer = None

if st.session_state.farmer is None:
    st.title("🌾 AnnData")
    st.subheader("Right Market · Right Time · Right Price")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            farmer = login_farmer(phone, password)
            if farmer:
                st.session_state.farmer = farmer
                st.rerun()
            else:
                st.error("Wrong phone or password!")

    with tab2:
        st.header("Register")
        name = st.text_input("Your Name")
        reg_phone = st.text_input("Phone Number ", key="reg_phone")
        district = st.selectbox("Your District", ["Hoshangabad", "Indore", "Bhopal", "Narsinghpur", "Sehore", "Vidisha", "Raisen"])
        reg_password = st.text_input("Password ", type="password", key="reg_pass")
        if st.button("Register"):
            if name and reg_phone and reg_password:
                success = register_farmer(name, reg_phone, district, reg_password)
                if success:
                    st.success("Registered! Now login.")
                else:
                    st.error("Phone already registered!")
            else:
                st.error("Fill all fields!")

else:
    farmer = st.session_state.farmer
    st.title(f"🌾 Welcome, {farmer['name']}!")
    st.subheader("Right Market · Right Time · Right Price")

    if st.button("Logout"):
        st.session_state.farmer = None
        st.rerun()

    crop = st.selectbox("Select Crop", ["Wheat", "Chana", "Soya", "Makka"])
    district = farmer["district"]
    st.info(f"Your District: **{district}**")

    if st.button("Get My Advisory"):
        data = get_advisory(crop, district)
        st.success(data["message"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=f"Your Rate ({data['your_mandi']})", value=f"Rs. {data['your_price']}")
        with col2:
            st.metric(label=f"Best Rate ({data['best_mandi']})", value=f"Rs. {data['best_price']}")
        with col3:
            st.metric(label="Profit per Quintal", value=f"Rs. {data['profit_per_quintal']}")

        st.info(f"Total Extra Earning on 10 Quintals: Rs. {data['extra_earning_10_quintal']}")

        st.subheader("📊 Mandi Price Comparison")
        mandis = ["Hoshangabad", "Itarsi", "Bhopal", "Narsinghpur", "Sehore", "Vidisha", "Indore"]
        prices = [2100, 2180, 2220, 2200, 2310, 2250, 2380]
        fig = go.Figure(go.Bar(
            x=mandis, y=prices,
            marker_color=["green" if m == data["best_mandi"] else "red" for m in mandis],
            text=prices, textposition="auto"
        ))
        fig.update_layout(xaxis_title="Mandi", yaxis_title="Price (Rs.)", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📈 14-Day Price Prediction")
        prediction = predict_prices(crop, data["best_mandi"])
        if prediction:
            fig2 = go.Figure(go.Scatter(
                x=prediction["dates"], y=prediction["prices"],
                mode="lines+markers", line=dict(color="green", width=2)
            ))
            fig2.update_layout(xaxis_title="Date", yaxis_title="Predicted Price (Rs.)", showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
            if prediction["prices"][-1] > prediction["prices"][0]:
                st.success("📈 Price RISE expected — consider waiting!")
            else:
                st.warning("📉 Price may DROP — sell soon!")