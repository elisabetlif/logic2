import json

def search(*args):
    try:
        with open('database.json', 'r') as f:
            # f : {marketplace:marketplace}
            db = json.load(f)
            # db : {marketplace:marketplace}
    except (FileNotFoundError, json.JSONDecodeError):
        # control flow depends on error condition (implicit flow)
        # error msg : {marketplace:customer} (safe to reveal)
        print("Could not load database.")
        return

    # Prompt user for search input
    query = input("Enter search: ").strip().lower()
    # query : {customer:marketplace}
    # explicitly flows into filter logic
    # This label must be handled carefully due to later control flow

    if not query:
        # control flow depends on query (implicit flow)
        print("Empty search query.")
        return

    # Load books and offers from database
    books = db.get('books', {}).get('data', [])
    # books : {marketplace:marketplace}
    offers = db.get('current book offerings', {}).get('data', [])
    # offers : {marketplace:marketplace}

    # Build map from book_id to offer
    offer_map = {offer['book_id']: offer for offer in offers}
    # offer_map : {marketplace:marketplace}
    # derived from internal marketplace data

    matches = []
    # matches : {marketplace:marketplace}

    for book in books:
        # book : {marketplace:marketplace}

        # control depends on query (implicit flow)
        if any(query in str(value).lower() for value in book.values()):
            # query : {customer:marketplace}
            # value from book : {marketplace:marketplace}
            # constraint: query ⊑ marketplace
            # => not always satisfied ⇒ must treat match result as {marketplace:marketplace}

            book_id = book.get('book_id')
            if book_id in offer_map:
                # offer_map : {marketplace:marketplace}

                # explicit flow: book + offer ⟶ match
                combined = {**book, **offer_map[book_id]}
                # combined : {marketplace:marketplace}

                matches.append(combined)
                # matches updated with marketplace-owned data

    # print results — requires declassification
    if matches:
        # implicit flow: control depends on query + marketplace data
        # branch must be treated at {marketplace:marketplace}
        print("\nSearch results:")
        for match in matches:
            # match : {marketplace:marketplace}
            # ↓ declassification is logically required here:
            # {marketplace:marketplace} ⟶ {marketplace:customer}
            print("-" * 40)
            for key, value in match.items():
                print(f"{key}: {value}")  # output : {marketplace:customer}
        print("-" * 40)
    else:
        # also safe to show (public no-match)
        print("No matching books currently offered.")
