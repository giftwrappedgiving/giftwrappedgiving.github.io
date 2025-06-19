import os

from data_helpers import read_json_as_dict


def read_all_guides():
    guides = []
    for filename in os.listdir("data/guides/"):
        if filename.endswith(".json"):
            guides.append(read_json_as_dict(os.path.join("data/guides/", filename)))
    return guides


# check there are no duplicate gifts in each guide
def check_guides():
    guides = read_all_guides()
    guides_with_duplicates = 0
    total_duplicates = 0

    for guide in guides:
        gift_names = set()
        duplicate_gifts = []
        print(f"\nChecking guide: {guide['name']}\n--------")
        for gift in guide.get("gifts", []):
            # should probably do it on id but name for now
            if gift["name"].lower() in gift_names:
                duplicate_gifts.append((guide["name"], gift["name"]))
            else:
                gift_names.add(gift["name"].lower())

        if len(duplicate_gifts) > 0:
            guides_with_duplicates += 1
            total_duplicates += len(duplicate_gifts)
            print("Duplicate gifts found:")
            for guide_name, gift_name in duplicate_gifts:
                print(f"Guide: {guide_name} - Duplicate Gift: {gift_name}")
        else:
            print(f"No duplicate gifts found in guide: {guide['name']}.")

    print("\n=== Summary ===")
    print(f"Total guides checked: {len(guides)}")
    print(f"Guides with duplicates: {guides_with_duplicates}")
    print(f"Total duplicate gifts found: {total_duplicates}")
    print("==============")


if __name__ == "__main__":
    check_guides()
    print("Finished checking guides.")
