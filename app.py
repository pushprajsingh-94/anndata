import streamlit as st
import requests
import plotly.graph_objects as go
from predict import predict_prices

st.title("🌾 AnnData")
st.subheader("Right Market · Right Time · Right Price")

crop = st.selectbox("Select Crop", ["Wheat", "Chana", "Soya", "Makka"])
district = st.selectbox("Select Your District", ["Hoshangabad", "Indore", "Bhopal", "Narsinghpur", "Sehore", "Vidisha", "Raisen"])

if st.button("Get My Advisory"):
    response = requests.get(
        f"https://anndata-xigg.onrender.com/advisory?crop={crop}&district={district}"
    )
    data = response.json()

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
        x=mandis,
        y=prices,
        marker_color=["red" if m != data["best_mandi"] else "green" for m in mandis],
        text=prices,
        textposition="auto"
    ))
    fig.update_layout(xaxis_title="Mandi", yaxis_title="Price (Rs. per Quintal)", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 14-Day Price Prediction")
    prediction = predict_prices(crop, data["best_mandi"])

    if prediction:
        fig2 = go.Figure(go.Scatter(
            x=prediction["dates"],
            y=prediction["prices"],
            mode="lines+markers",
            line=dict(color="green", width=2),
            marker=dict(size=6)
        ))
        fig2.update_layout(xaxis_title="Date", yaxis_title="Predicted Price (Rs.)", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

        if prediction["prices"][-1] > prediction["prices"][0]:
            st.success("📈 Price is expected to RISE in next 14 days — consider waiting!")
        else:
            st.warning("📉 Price may DROP — sell soon!")