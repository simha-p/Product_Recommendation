# E-commerce Product Recommender


A Streamlit-based e-commerce product recommendation system using content-based filtering and the API to simulate real-world product data and provide personalized product suggestions.

[Live Demo](https://simhagoud.streamlit.app/)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Product search functionality
- Display of search results with product details
- Content-based filtering for generating recommendations
- Similarity scores for recommended products
- Responsive web interface

## Technologies Used

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Requests

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/ecommerce-recommender.git
cd ecommerce-recommender


2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate


3. Install the required packages:
pip install -r requirements.txt


## Usage

To run the application locally:

streamlit run app.py


Then, open your web browser and go to `http://localhost:8501`.

## Deployment

This application is deployed using Streamlit Sharing.

## Project Structure

- `app.py`: Main application file containing the Streamlit app and recommendation system logic
- `requirements.txt`: List of Python dependencies

## How It Works

1. The user enters a search query for a product.
2. The application fetches product data from the API based on the search query.
3. The search results are displayed to the user.
4. A content-based filtering algorithm is applied to generate recommendations based on the top search result.
5. Recommended products are displayed along with their similarity scores.
