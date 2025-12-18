# 🔗 URL Shortener Using Hashing (Separate Chaining)

A GUI-based URL Shortener implemented in Python (Tkinter) that demonstrates hashing with separate chaining, collision handling, and dynamic rehashing.  
This project is designed to showcase Data Structures concepts in a practical and interactive way.

---

## 📌 Overview

This application converts long URLs into short, unique URLs using a custom hash function and stores them in a hash table with separate chaining.  
Users can:

- Shorten a URL
- Expand a short URL back to the original
- Delete a stored URL
- Visualize the hash table structure and load factor

The project also includes dynamic rehashing when the load factor exceeds a threshold (0.7).

---

## ✨ Features

- **Custom Hash Function**
  - Converts URLs into a Base-62 encoded short key
- **Separate Chaining**
  - Handles collisions using linked-list style buckets
- **Dynamic Rehashing**
  - Hash table size doubles when load factor > 0.7
- **URL Expansion**
  - Retrieves original URLs from short links
- **Deletion Support**
  - Removes URL mappings safely
- **Hash Table Visualization**
  - Displays index, hash key, stored URLs, and load factor
- **Tkinter GUI**
  - Clean and interactive desktop interface

---

## 🛠️ Tech Stack

- **Language:** Python  
- **GUI Library:** Tkinter  
- **Data Structures Used:**
  - Hash Table
  - Separate Chaining (Lists)
- **Encoding:** Base-62

---

## 🚀 Future Enhancements

- Persistent storage (File/Database)
- URL expiration feature
- Custom aliases for short URLs
- Click tracking & analytics
- Web-based version (Flask/Django)

