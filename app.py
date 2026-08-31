from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Business-Aware Fashion Store",
    page_icon="🛍️",
    layout="wide"
)

DATA_DIR = Path("data/processed")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    customers = pd.read_parquet(
        DATA_DIR / "customers.parquet"
    )

    articles = pd.read_parquet(
        DATA_DIR / "articles.parquet"
    )

    transactions = pd.read_parquet(
        DATA_DIR / "transactions.parquet"
    )

    recommendations = pd.read_parquet(
        DATA_DIR / "optimized_recommendations.parquet"
    )

    demo_users = pd.read_parquet(
        DATA_DIR / "demo_users.parquet"
    )

    bought_together = pd.read_parquet(
        DATA_DIR / "bought_together.parquet"
    )

    return (
        customers,
        articles,
        transactions,
        recommendations,
        demo_users,
        bought_together,
    )


(
    customers,
    articles,
    transactions,
    recommendations,
    demo_users,
    bought_together,
) = load_data()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "customer_id" not in st.session_state:
    st.session_state.customer_id = None

if "cart" not in st.session_state:
    st.session_state.cart = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🛍️ Store")

    st.metric(
        "Items in Cart",
        len(st.session_state.cart)
    )

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if st.session_state.customer_id is None:

    st.title(
        "Business-Aware Fashion Store"
    )

    st.markdown(
        """
        Select a customer to simulate
        a personalized shopping experience.
        """
    )

    selected_user = st.selectbox(
        "Customer",
        demo_users["customer_id"].tolist()
    )

    # ----------------------------------------
    # PREVIEW CUSTOMER PROFILE
    # ----------------------------------------

    customer_info = customers[
        customers["customer_id"] == selected_user
    ]

    age = None

    if not customer_info.empty:
        age = customer_info.iloc[0]["age"]

    user_tx = transactions[
        transactions["customer_id"] == selected_user
    ]

    user_history = user_tx.merge(
        articles[
            [
                "article_id",
                "product_group_name",
                "colour_group_name",
                "product_type_name",
            ]
        ],
        on="article_id",
        how="left"
    )

    total_purchases = len(user_history)

    favorite_category = (
        user_history["product_group_name"]
        .mode()
        .iloc[0]
        if not user_history.empty
        else "-"
    )

    favorite_color = (
        user_history["colour_group_name"]
        .mode()
        .iloc[0]
        if not user_history.empty
        else "-"
    )

    favorite_product_type = (
        user_history["product_type_name"]
        .mode()
        .iloc[0]
        if not user_history.empty
        else "-"
    )

    avg_spend = (
        user_tx["price"].mean()
        if not user_tx.empty
        else 0
    )

    st.divider()

    st.subheader("Customer Preview")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Age", age)

    c2.metric(
        "Purchases",
        total_purchases
    )

    c3.metric(
        "Favourite Category",
        favorite_category
    )

    c4.metric(
        "Favourite Color",
        favorite_color
    )

    c5.metric(
        "Avg Purchase Price",
        f"{avg_spend:.2f} €"
    )

    st.caption(
        f"Favourite Product Type: {favorite_product_type}"
    )

    st.divider()

    if st.button(
        "Login",
        type="primary"
    ):
        st.session_state.customer_id = selected_user
        st.rerun()

# --------------------------------------------------
# HOME
# --------------------------------------------------

else:

    customer_id = st.session_state.customer_id

    st.title("🛍️ Business-Aware Fashion Store")

    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(
            f"Logged in as customer **{customer_id}**"
        )

    with col2:
        if st.button("Logout"):

            st.session_state.customer_id = None
            st.session_state.cart = []

            st.rerun()

    st.divider()

    # --------------------------------------------------
    # CUSTOMER PROFILE
    # --------------------------------------------------

    customer_info = customers[
        customers["customer_id"] == customer_id
    ]

    age = None

    if not customer_info.empty:
        age = customer_info.iloc[0]["age"]

    user_tx = transactions[
        transactions["customer_id"] == customer_id
    ]

    user_history = user_tx.merge(
        articles[
            [
                "article_id",
                "product_group_name",
                "colour_group_name",
                "product_type_name",
            ]
        ],
        on="article_id",
        how="left"
    )

    total_purchases = len(user_history)

    favorite_category = (
        user_history["product_group_name"]
        .mode()
        .iloc[0]
        if not user_history.empty
        else "-"
    )

    favorite_color = (
        user_history["colour_group_name"]
        .mode()
        .iloc[0]
        if not user_history.empty
        else "-"
    )

    favorite_product_type = (
        user_history["product_type_name"]
        .mode()
        .iloc[0]
        if not user_history.empty
        else "-"
    )

    st.subheader("Customer Profile")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Age", age)

    k2.metric(
        "Purchases",
        total_purchases
    )

    k3.metric(
        "Favourite Category",
        favorite_category
    )

    k4.metric(
        "Favourite Color",
        favorite_color
    )

    st.caption(
        f"Favourite Product Type: {favorite_product_type}"
    )

    st.divider()

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader("✨ Recommended For You")

    user_recommendations = recommendations[
        (recommendations["customer_id"] == customer_id)
        &
        (
            recommendations[
                "recommendation_type"
            ] == "BUSINESS_OPTIMIZED"
        )
    ].copy()

    user_recommendations = user_recommendations.head(10)

    if user_recommendations.empty:

        st.warning(
            "No recommendations available."
        )

    else:

        cols = st.columns(5)

        for i, (_, row) in enumerate(
            user_recommendations.iterrows()
        ):

            with cols[i % 5]:

                st.markdown(
                    f"### {row['prod_name']}"
                )

                st.write(
                    row["product_group_name"]
                )

                st.write(
                    f"Score: {row['score']:.3f}"
                )

                if st.button(
                    "Add to Cart",
                    key=f"rec_{row['article_id']}"
                ):

                    st.session_state.cart.append(
                        row["article_id"]
                    )

                    st.success(
                        "Added to cart"
                    )

    st.divider()

    st.subheader(
        "👥 Popular Among Similar Customers"
    )

    similar_users_recs = recommendations[
        (recommendations["customer_id"] == customer_id)
        &
        (
            recommendations["recommendation_type"]
            == "ALS"
        )
    ].head(10)

    if similar_users_recs.empty:

        st.warning(
            "No recommendations available."
        )

    else:

        cols = st.columns(5)

        for i, (_, row) in enumerate(
            similar_users_recs.iterrows()
        ):

            with cols[i % 5]:

                st.markdown(
                    f"### {row['prod_name']}"
                )

                st.write(
                    row["product_group_name"]
                )

                st.write(
                    f"Score: {row['score']:.3f}"
                )

                if st.button(
                    "Add to Cart",
                    key=f"rec_{row['article_id']}_similar"
                ):

                    st.session_state.cart.append(
                        row["article_id"]
                    )

                    st.success(
                        "Added to cart"
                    )

    st.divider()

    st.subheader("🛒 Cart Preview")

    if len(st.session_state.cart) == 0:

        st.info(
            "Your cart is empty."
        )

    else:

        cart_df = articles[
            articles["article_id"].isin(
                st.session_state.cart
            )
        ]

        st.dataframe(
            cart_df[
                [
                    "article_id",
                    "prod_name",
                    "product_group_name"
                ]
            ],
            use_container_width=True
        )

        last_product = st.session_state.cart[-1]

        also_bought = bought_together[
            bought_together["article_id"]
            == last_product
        ].head(5)

        st.divider()

        st.subheader(
            "🧺 Customers Also Bought"
        )

        if also_bought.empty:

            st.info(
                "No complementary recommendations available."
            )

        else:

            rec_cols = st.columns(
                min(len(also_bought), 5)
            )

            for idx, (_, row) in enumerate(
                also_bought.iterrows()
            ):

                with rec_cols[idx]:
                    st.markdown(
                        f"### {row['recommended_product_name']}"
                    )

                    st.write(
                        f"Lift: {row['lift']:.2f}"
                    )

                    st.write(
                        f"Confidence: {row['confidence']:.2%}"
                    )

                    recommended_id = row[
                        "recommended_article_id"
                    ]

                    if st.button(
                        "Add to Cart",
                        key=f"also_bought_{recommended_id}"
                    ):

                        st.session_state.cart.append(
                            recommended_id
                        )

                        st.rerun()
