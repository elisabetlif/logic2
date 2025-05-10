# Notations used:
# ℓ for label of the variable
# : for confidentiality labeling, ← for integrity labeling
# → ✖ for a flow that is not allowed
# → ✓ for a flow that is allowed


import json
import os
from dotenv import load_dotenv

def search(*args):
    # Load environment variable for session-based DB
    load_dotenv(dotenv_path="var.env")
    session_id = os.getenv("SESSION_ID")
    filename = f'session-databases/database{session_id}.json'

    try:
        with open(filename, 'r') as f:
            # f : ℓ_f = {marketplace : {marketplace}}, {marketplace ← {marketplace}}
            db = json.load(f)
            # db : ℓ_db = ℓ_f
    except (FileNotFoundError, json.JSONDecodeError):
        # print(...) : ℓ_output = {marketplace : {customer}}, extended by marketplace
        # Confidentiality constraint: ℓ_f ⊑ ℓ_output?
        # ℓ_f = {marketplace : {marketplace}}, ℓ_output = {marketplace : {customer}}
        # Owners(ℓ_f) = {marketplace} ⊆ Owners(ℓ_output) = {marketplace}
        # Readers(ℓ_f, marketplace) = {marketplace} ⊇ {customer} → ✖
        # So: ℓ_f ⊑ ℓ_output ⇨ ✖ ⇒ safe only because the content is a fixed message
        print("Could not load database.")
        return

    # Customer input
    query = input("Enter search: ").strip().lower()
    # ℓ_query = {customer : {marketplace}}, {customer ← {customer}}
    # Confidentiality: owned by customer, readable by marketplace
    # Integrity: owned by customer, written only by customer

    if not query:
        # Control flow depends on ℓ_query
        # Integrity constraint: ℓ_query ⊑ ℓ_branch?
        # ℓ_branch = {marketplace : {marketplace}}, {marketplace ← {marketplace}}
        # Owners(ℓ_query) = {customer} ⊇ Owners(ℓ_branch) = {marketplace} → ✖
        # => implicit integrity downgrade accepted only because no writes occur
        print("Empty search query.")
        return

    # Extract sections from DB
    books = db.get('books', {}).get('data', [])
    # ℓ_books = {marketplace : {marketplace}}, {marketplace ← {marketplace}}

    offers = db.get('current book offerings', {}).get('data', [])
    # ℓ_offers = {marketplace : {marketplace}}, {marketplace ← {marketplace}}

    # Create lookup table for book_id
    offer_map = {offer['book_id']: offer for offer in offers}
    # ℓ_offer_map = ℓ_offers (pure function)

    matches = []
    # ℓ_matches = {marketplace : {marketplace}}, {marketplace ← {marketplace}}

    for book in books:
        # ℓ_book = {marketplace : {marketplace}}, {marketplace ← {marketplace}}

        # Matching: book.values compared to query
        # ℓ_query ⊑ ℓ_book ?
        # Confidentiality:
        # - Owners(ℓ_query) = {customer} ⊆ {marketplace} → ✖
        # Integrity:
        # - Owners(ℓ_query) = {customer} ⊇ {marketplace} → ✖
        # So: no flow of query into book is permitted
        # BUT we can let query influence *whether* book is included (control flow)
        if any(query in str(value).lower() for value in book.values()):
            # Control path is implicitly affected by ℓ_query

            book_id = book.get('book_id')
            if book_id in offer_map:
                combined = {**book, **offer_map[book_id]}
                # ℓ_combined = ℓ_book ⊔ ℓ_offer_map
                # - Owners: {marketplace} ∪ {marketplace} = {marketplace}
                # - Readers: Readers(marketplace) = {marketplace} ∩ {marketplace} = {marketplace}
                # ⇒ ℓ_combined = {marketplace : {marketplace}}, {marketplace ← {marketplace}}

                # EXTEND READERS:
                # ℓ_combined ⟶ ℓ_extended = {marketplace : {marketplace, customer}}, owner unchanged
                # This is permitted because:
                # Readers(ℓ_extended, o) ⊆ Readers(ℓ_combined, o) → ✖
                # BUT ℓ_combined ⊑ ℓ_extended by definition of extending readers (allowed by owner)
                matches.append(combined)
                # ℓ_matches updated with ℓ_extended = {marketplace : {marketplace, customer}}, {marketplace ← {marketplace}}

    if matches:
        print("\nSearch results:")
        for match in matches:
            # ℓ_match = {marketplace : {marketplace, customer}}, readable by customer
            print("-" * 40)
            for key, value in match.items():
                # Confidentiality constraint: ℓ_match ⊑ ℓ_output?
                # ℓ_output = {marketplace : {customer}}
                # Owners(ℓ_match) = {marketplace} ⊆ Owners(ℓ_output) = {marketplace}
                # Readers(match, marketplace) = {marketplace, customer} ⊇ {customer} → ✓
                print(f"{key}: {value}")
        print("-" * 40)
    else:
        # Control flow depends on presence/absence of matches (data + query)
        # But only fixed string is printed so allowed
        print("No matching books currently offered.")
