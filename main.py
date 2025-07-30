import os
import time 
import requests # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore


keywords = [
    "Megi", "Oil", "Rice 1KG", "Sugar", "Salt", "Wheat Flour 5KG", "Maida 1KG" ,  "Toothpaste", "Toothbrush", 
    "Soap", "Shampoo", "Hair Oil", "Face Wash", "Body Lotion","Hand Sanitizer", "Talcum Powder", "Cotton", "Razor", 
    "Shaving Cream", "Lip Balm", "Face Cream",
    "Comb", "Sanitary Pads", "Diapers", "Baby Oil", "Baby Lotion" , "Phenyl", "Toilet Cleaner", "Floor Cleaner", 
    "Detergent Powder", "Detergent Liquid",
    "Dishwash Bar", "Dishwash Liquid", "Scrubber", "Room Freshener", "Garbage Bags", "Bathroom Cleaner", 
    "Washing Soap", "Hand Wash", "Mop", "Cleaning Cloth", "Tissue Paper" ,  "Baby Food", 
    "Cerelac", "Lactogen", "Baby Diapers", 
    "Baby Wipes", "Feeding Bottle",
    "Thermometer", "Pain Balm", "Paracetamol", "ORS Sachet", "First Aid Box", "Bandage" , "Megi", "Oil",
      "Rice 1KG", "Sugar", "Salt", "Wheat Flour 5KG", "Maida 1KG", "Turmeric Powder 200g",
    "Chili Powder 100g", "Coriander Powder 500g", "Cumin Seeds", "Mustard Seeds", "Sunflower Oil 1L",
    "Groundnut Oil 1L", "Butter", "Ghee 500g", "Milk 1L", "Curd 500g", "Paneer 200g", "Green Tea",
    "Tea Powder 250g", "Coffee 200g", "Pasta", "Macaroni", "Vermicelli 500g", "Bread", "Jam 500g",
    "Honey 250g", "Peanut Butter", "Tomato Ketchup", "Mayonnaise", "White Vinegar 500ml",
    "Soya Sauce 250ml", "Oats 1KG", "Cornflakes 500g", "Muesli 1KG", "Poha 1KG", "Sabudana",
    "Toor Dal 1KG", "Urad Dal 1KG", "Chana Dal", "Moong Dal", "Masoor Dal", "Rajma 1KG",
    "Chickpeas 1KG", "Black Beans", "Soybeans", "Lobia", "Green Gram", "Dry Fruits Mix", "Almonds 250g",
    "Cashews 250g", "Pistachios 100g", "Raisins 100g", "Walnuts 100g", "Dates 500g", "Coconut", 
    "Desiccated Coconut 250g", "Baking Powder", "Baking Soda", "Custard Powder", "Cocoa Powder 100g",
    "Corn Flour", "Besan 1KG", "Ajwain", "Hing", "Bay Leaf", "Cinnamon", "Cloves", "Cardamom 50g",
    "Star Anise", "Jaggery", "Brown Sugar", "Ice Cream", "Frozen Peas 1KG", "Paneer Cubes",
    "Tofu 200g", "Soy Chunks", "Pickle 1KG", "Papad", "Instant Soup", "Chips", "Cream Biscuits",
    "Cookies", "Chocolate", "Cakes", "Soft Drinks", "Juice 1L", "Energy Drink", "Mineral Water",
    "Soda", "Lemon Juice", "Tamarind", "Imli", "Kokum", "Amchur Powder", "Mango Pulp", "Canned Beans",
    "Mixed Herbs", "Black Pepper", "Red Chili Flakes", "Oregano", "Cooking Spray", "Green Peas 500g"
]




base_path = r"C:\ImageDown"


options = Options()
options.add_argument("--start-maximized")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for keyword in keywords:
    try:
        print(f"🔍 Searching: {keyword}")
        driver.get("https://www.amazon.in/")
        time.sleep(2)

        
        search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.submit()

       
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.s-image"))
        )
        time.sleep(2)

        
        folder_name = keyword.replace(" ", "_")
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        
        images = driver.find_elements(By.CSS_SELECTOR, "img.s-image")
        count = 0
        for img in images:
            if count >= 3:
                break
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                file_path = os.path.join(folder_path, f"{folder_name}_{count}.jpg")
                try:
                    r = requests.get(src, stream=True, timeout=10)
                    with open(file_path, "wb") as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    print(f"Downloaded: {file_path}")
                    count += 1
                except Exception as e:
                    print(f"Failed to download image: {e}")
    except Exception as e:
        print(f"Error with keyword '{keyword}': {e}")

driver.quit()
print("...mission completed...😂")
