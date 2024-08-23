import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import requests

# DummyJSON API configuration
DUMMYJSON_API_BASE_URL = 'https://dummyjson.com/products'

# Function to search DummyJSON products
def search_dummyjson_products(query, limit=20):
  url = f"{DUMMYJSON_API_BASE_URL}/search"
  params = {
      'q': query,
      'limit': limit
  }
  response = requests.get(url, params=params)
  if response.status_code == 200:
      return response.json()['products']
  else:
      st.error(f"Error fetching data from DummyJSON API: {response.status_code}")
      return []

# Function to process DummyJSON product data
def process_dummyjson_data(products):
  processed_products = []
  for product in products:
      processed_products.append({
          'product_id': product['id'],
          'product_name': product['title'],
          'description': product['description'],
          'price': product['price'],
          'image_url': product['thumbnail'],
          'category': product['category']
      })
  return pd.DataFrame(processed_products)

# Content-based filtering recommendation system
class ContentBasedRecommender:
  def __init__(self, products):
      self.products = products
      self.products['content'] = self.products['description'] + ' ' + self.products['category']
      self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
      self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.products['content'])
      self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

  def get_recommendations(self, product_name, n=5):
      idx = self.products.index[self.products['product_name'] == product_name].tolist()[0]
      sim_scores = list(enumerate(self.cosine_sim[idx]))
      sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
      sim_scores = sim_scores[1:n+1]
      product_indices = [i[0] for i in sim_scores]
      recommendations = self.products.iloc[product_indices].copy()
      recommendations['similarity_score'] = [score for _, score in sim_scores]
      return recommendations

# Streamlit App
def main():
  st.title('Product Recommendations')

  search_query = st.text_input('Search for a product:')
  
  if st.button('Get Recommendations'):
      if search_query:
          with st.spinner('Searching products and generating recommendations...'):
              # Search DummyJSON products
              dummyjson_products = search_dummyjson_products(search_query)
              if dummyjson_products:
                  # Process DummyJSON data
                  products_df = process_dummyjson_data(dummyjson_products)
                  
                  # Initialize recommender
                  recommender = ContentBasedRecommender(products_df)

                  # Display search results
                  st.subheader("Search Results")
                  for _, product in products_df.head().iterrows():
                      col1, col2 = st.columns([1, 3])
                      with col1:
                          st.image(product['image_url'], width=150)
                      with col2:
                          st.subheader(product['product_name'])
                          st.write(f"Price: ${product['price']:.2f}")
                          st.write(f"Category: {product['category']}")
                      st.write("---")

                  # Get recommendations for the first search result
                  first_product = products_df.iloc[0]
                  recommendations = recommender.get_recommendations(first_product['product_name'])
                  
                  st.subheader(f"Recommendations based on: {first_product['product_name']}")
                  for _, product in recommendations.iterrows():
                      col1, col2 = st.columns([1, 3])
                      with col1:
                          st.image(product['image_url'], width=150)
                      with col2:
                          st.subheader(product['product_name'])
                          st.write(f"Price: ${product['price']:.2f}")
                          st.write(f"Category: {product['category']}")
                          st.write(f"Similarity Score: {product['similarity_score']:.2f}")
                      st.write("---")
              else:
                  st.write("No products found. Please try a different search term.")
      else:
          st.write("Please enter a search term.")

if __name__ == "__main__":
  main()