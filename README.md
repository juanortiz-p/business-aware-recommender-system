# Business-Aware Recommender System

https://business-aware-recommender-system-juanortiz-p.streamlit.app/

An end-to-end e-commerce recommendation platform that combines **Collaborative Filtering**, **Association Rule Mining**, and **Mathematical Optimization** to generate personalized product recommendations that balance customer relevance with business objectives.

## 🚀 Why This Project?

Most portfolio recommender systems stop at:

> "Users who liked X also liked Y."

This project goes further by combining three complementary recommendation approaches commonly used in production environments:

### 1. Collaborative Filtering (Implicit ALS)

Learns customer preferences from historical purchases and recommends products based on latent user-item relationships.

**Goal:** Predict what a customer is most likely to buy next.

### 2. Market Basket Analysis (FP-Growth + Association Rules)

Discovers products that are frequently purchased together.

**Goal:** Generate cross-selling recommendations such as:

```text
Running Shoes
    ↓
Sports Socks
```

### 3. Business-Aware Recommendation Optimization (OR-Tools)

Re-ranks recommendations by considering business objectives beyond user relevance.

Optimizes:

- Purchase probability
- Product margins
- Inventory exposure
- Product diversity
- Promotion priorities

**Goal:** Select the recommendations that maximize both customer satisfaction and business value.

---

# 🏗️ Project Architecture

```text
Customer Transactions
          │
          ▼
     ALS Recommender
          │
          ▼
 Candidate Products
          │
          ▼
 Optimization Layer
          │
          ▼
Recommended Products

          +

Market Basket Analysis
(Frequently Bought Together)

          ▼

Cross-Selling Recommendations
```

---

# 🧠 Algorithms Used

## Collaborative Filtering

Library:

```python
implicit
```

Model:

```text
Alternating Least Squares (ALS)
```

Input:

```text
Customer purchases
```

Output:

```text
Top-N personalized recommendations
```

---

## Market Basket Analysis

Library:

```python
mlxtend
```

Algorithm:

```text
FP-Growth
```

Metrics:

```text
Support
Confidence
Lift
```

Output:

```text
Frequently Bought Together
```

---

## Optimization

Library:

```python
OR-Tools
```

Approach:

```text
Constrained Optimization
```

Objective:

```text
Maximize:
    Relevance
    + Margin
    + Inventory Exposure
    + Promotion Priority

Subject to:
    Category Diversity
    Product Limits
```

---

# 📊 Dataset

The project uses the **H&M Personalized Fashion Recommendations** dataset.

Download:

https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data

Required files:

```text
articles.csv
customers.csv
transactions_train.csv
```

---

# 📁 Project Structure

```text
business-aware-recommender-system/

│
├── data/
│   ├── raw/
│   │   ├── articles.csv
│   │   ├── customers.csv
│   │   └── transactions_train.csv
│   │
│   └── processed/
│
├── notebooks/
│   ├── 01_data_loading_and_preprocessing.ipynb
│   ├── 02_als_recommender.ipynb
│   ├── 03_market_basket_analysis.ipynb
│   └── 04_business_optimization.ipynb
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repo-url>

cd business-aware-recommender-system
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 📂 Data Setup

Create:

```text
data/raw
```

and place the Kaggle files inside:

```text
data/raw/
├── articles.csv
├── customers.csv
└── transactions_train.csv
```

---

# 🔄 Data Processing Pipeline

Run notebooks in the following order:

### Notebook 01

```text
01_data_loading_and_preprocessing.ipynb
```

Creates:

```text
articles.parquet
customers.parquet
transactions.parquet
interactions.parquet
business_features.parquet
```

---

### Notebook 02

```text
02_als_recommender.ipynb
```

Creates:

```text
candidate_recommendations.parquet
als_model.pkl
demo_users.parquet
```

---

### Notebook 03

```text
03_market_basket_analysis.ipynb
```

Creates:

```text
bought_together.parquet
```

---

### Notebook 04

```text
04_business_optimization.ipynb
```

Creates:

```text
optimized_recommendations.parquet
```

---

# 🖥️ Launch the Application

Start Streamlit:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🎯 Features

### Customer Login Simulation

Choose a customer profile and explore a personalized shopping experience.

### Customer Analytics

View customer KPIs:

- Age
- Favorite category
- Favorite color
- Purchase history
- Product preferences

### Personalized Recommendations

Powered by:

```text
ALS + Optimization
```

### Frequently Bought Together

Powered by:

```text
Association Rules
```

### Shopping Cart Simulation

Add products to a cart and receive cross-selling recommendations.

---

# 📈 Business Optimization

This project demonstrates how recommendation systems can be optimized beyond click probability.

Example trade-offs:

```text
Higher Margin Products
Higher Inventory Exposure
More Category Diversity

vs

Pure Relevance Maximization
```

This mirrors real-world recommendation challenges faced by:

- Amazon
- Zalando
- Booking
- Carrefour
- Retail and Marketplace Platforms

---

# 🛠️ Tech Stack

```text
Python
Pandas
NumPy
Scipy
Implicit ALS
MLxtend
OR-Tools
Streamlit
PyArrow
Jupyter
```

---

# 👨‍💻 Author

**Juan Ortiz**
juan.ortiz1alonso@gmail.com

Senior Data Scientist / Data Engineer

Specialized in:

- Recommendation Systems
- Mathematical Optimization
- Forecasting
- Machine Learning
- GenAI
- Data Engineering