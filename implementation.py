# REF - Note that certain sections of this code were adapted from (https://keras.io/examples/structured_data/collaborative_filtering_movielens/) and serve as an inspiration for the current implementation
# The above has been appropriately referenced in the report

#Imports
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tabulate import tabulate

def interface():
  model = keras.models.load_model("ncf-model")
  rating_df = pd.read_csv("goodreads_ratings.csv")
  rating_df, user_encode, book_encode, t_book_encode = preprocess(df)
  book_df = pd.read_csv("books.csv")
  
  print(" ------------------ Sign In ------------------")
  print("     ____                 __      __    __")
  print("    / __ \___  ____ _____/ /___ _/ /_  / /__  ")
  print("   / /_/ / _ \/ __ `/ __  / __ `/ __ \/ / _ \ ")
  print("  / _, _/  __/ /_/ / /_/ / /_/ / /_/ / /  __/ ")
  print(" /_/ |_|\___/\__,_/\__,_/\__,_/_.___/_/\___/  ")
  print("find your next great read")
  print('\n')
  tries = 0
  while True:
    user_id = input("userID: ")
    try:
      user_id = np.int64(user_id)
      if 0 <= user_id <= 227:
        print("Welcome Back, User {}! ".format(user_id))
        break
      else:
        tries += 1
        if tries >= 3:
          print("Multiple invalid attempts. Exiting...")
          return
          print("Invalid userID - Please try again")
    except ValueError:
      tries += 1
      if tries >= 3:
        print("Multiple invalid attempts. Exiting...")
        return
        print("Invalid userID - Please try again")
  while True:
    print('\n')
    print("*********  MAIN MENU  *********")
    print("[A] My Library       (view your previously rated books)")
    print("[B] Recommendations  (get book recommendations based on your rating history)")
    print("[C] Popular Picks    (view top trending books across our community)")
    print("[D] Logout           (securely sign out of your account)")
    print('\n')
    choice = input("Option: ")
    if choice == "A":
      get_profile(rating_df, book_df, user_id)
    elif choice == "B":
      get_recommendations(rating_df, book_df, user_id, user_encode, book_encode, t_book_encode)
    elif choice == "C":
      get_trending(book_df)
    elif choice == "D":
      print("Thank you for using Readable!")
      break
    else:
      print("Invalid choice. Please try again.")

def preprocess(rating_df):
  user_encode = {x: i for i, x in enumerate(df["user_id"].unique().tolist())}
  book_ids = rating_df["book_id"].unique().tolist()
  book_encode = {x: i for i, x in enumerate(book_ids)}
  t_book_encode = {i: x for i, x in enumerate(book_ids)}
  rating_df["user"] = rating_df["user_id"].map(user_encode)
  rating_df["book"] = rating_df["book_id"].map(book_encode)
  return rating_df, user_encode, book_encode, t_book_encode

def get_recommendations(rating_df, book_df, user_id, user_encode, book_encode, t_book_encode):
  valid_book_ids = set(book_df[~book_df["book_id"].isin(rating_df.loc[rating_df.user_id == user_id, :].book_id.values)]["book_id"]) & set(book_encode.keys())
  unread = [[book_encode.get(book_id)] for book_id in valid_book_ids]
  user_book_array = np.concatenate(([[user_encode.get(user_id)]] * len(unread), unread), axis=1)
  ratings = model.predict(user_book_array).flatten()
  recommended_book_ids = [t_book_encode.get(unread[x][0]) for x in np.argpartition(ratings, -10)[-10:]]
  recommended_books = book_df[book_df["book_id"].isin(recommended_book_ids)]
  print("  New reads we think you might like :)")
  print(tabulate(recommended_books.iloc[:, [0,1,2],], headers=["TITLE","RATINGS","LINK"], tablefmt='fancy_grid',showindex=False))
  print("\n")
  print("At Readable, we use cutting-edge technology to provide personalized book recommendations tailored to your unique reading preferences") 
  print("Based on your past rating history, our algorithms have generated suggestions we believe you may enjoy")
  print("We encourage you to approach these suggestions with an open mind and to thoroughly research each book before making a final decision.")
  print("While we stand behind the accuracy of our algorithms, ultimately the decision to read a book is yours")

def get_profile(rating_df, book_df, user_id):
  top_books = rating_df[rating_df['user_id'] == user_id].sort_values(by='rating', ascending=False).head(10)
  profile = book_df.loc[book_df['book_id'].isin(top_books['book_id'])].head(5)
  print('\n')
  print("Here are your highly rated books:")
  print(tabulate(profile.iloc[:, [0,1,2],], headers=["TITLE","RATINGS","LINK"], tablefmt='fancy_grid',showindex=False))

def get_trending(book_df):
  #Popularity recommender (non-personalised) - simply recommends the top 10 books in terms of # of ratings to each user 
  trending = book_df.sort_values(by="ratings", ascending=False).head(10)
  print('\n')
  print("Top 10 Trending Books")
  print(tabulate(trending.iloc[:, [0,1,2],], headers=["TITLE","RATINGS","LINK"], tablefmt='fancy_grid',showindex=False))

if __name__ == "__main__":
    interface()