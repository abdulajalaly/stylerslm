# cli_stylist.py
import sys
from ontology import OCCASIONS, TEMPERATURE, STYLES, FITS
from generate_outfits import generate_outfits

# A sample "User Wardrobe" - in a real app, this would come from a database
USER_WARDROBE = [
    {"category": "shirt", "color": "white", "subtype": "oxford"},
    {"category": "shirt", "color": "navy", "subtype": "polo"},
    {"category": "shirt", "color": "black", "subtype": "tee"},
    {"category": "shirt", "color": "beige", "subtype": "henley"},
    
    {"category": "pants", "color": "black", "subtype": "jeans"},
    {"category": "pants", "color": "beige", "subtype": "chinos"},
    {"category": "pants", "color": "grey", "subtype": "trousers"},
    
    {"category": "shoes", "color": "white", "subtype": "sneakers"},
    {"category": "shoes", "color": "black", "subtype": "loafers"},
    {"category": "shoes", "color": "brown", "subtype": "boots"},
]

def get_user_choice(prompt, options):
    """Helper to ask user to pick from a list."""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    
    while True:
        try:
            choice = int(input("Enter number: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

def main():
    print("--- Welcome to StylerSLM ---")
    print("I will design an outfit for you based on your needs.\n")

    # 1. Collect Inputs
    occasion = get_user_choice("What is the occasion?", OCCASIONS)
    temp = get_user_choice("What is the weather like?", TEMPERATURE)
    style = get_user_choice("What style are you aiming for?", STYLES)
    
    # Optional: You could add 'Fit' or 'Outerwear' logic here too
    context = {
        "occasion": occasion,
        "temperature": temp,
        "style": style,
        "fit": "regular",      # Default
        "outerwear": "none"    # Default
    }

    print(f"\nAnalyzing wardrobe for a {temp} {occasion} ({style} style)...")

    # 2. Generate Recommendations
    # We catch errors in case the model hasn't been trained yet
    try:
        recommendations = generate_outfits(USER_WARDROBE, context, top_k=3)
    except FileNotFoundError:
        print("\nError: Model not found!")
        print("Please run 'python train.py' first to train your StylerSLM.")
        return

    if not recommendations:
        print("No matching outfits found in your wardrobe!")
        return

    # 3. Output Results
    print("\nHere are my top recommendations:")
    for i, (score, outfit) in enumerate(recommendations, 1):
        s = outfit['shirt']
        p = outfit['pants']
        sh = outfit['shoes']
        
        print(f"\nOption {i} (Score: {score:.2f})")
        print(f"  👕 {s['color'].title()} {s['subtype'].title()}")
        print(f"  👖 {p['color'].title()} {p['subtype'].title()}")
        print(f"  👟 {sh['color'].title()} {sh['subtype'].title()}")

if __name__ == "__main__":
    main()