"""
Parse PROJECT_VISION product hierarchy into structured format.
Extracts Department -> Classes mapping from the 394-row table.
"""
import yaml
from collections import defaultdict

# Full hierarchy from PROJECT_VISION.md (394 rows)
raw_hierarchy = """
Accessories|Accessories:Bags
Accessories|Accessories:BELTS
Accessories|Accessories:CONFECTIONERY
Accessories|Accessories:DUMMY
Accessories|Accessories:GENTS ACCESSORIES
Accessories|Accessories:Gloves
Accessories|Accessories:Hair
Accessories|Accessories:HAIR ACCESSORIES
Accessories|Accessories:Hats
Accessories|Accessories:HW Scarves
Accessories|Accessories:JEWELLERY AND GIFTS
Accessories|Accessories:Kids
Accessories|Accessories:KIDS ACCESSORIES
Accessories|Accessories:KIDS BAGS
Accessories|Accessories:Ladies Belts
Accessories|Accessories:LADIES GLOVES
Accessories|Accessories:LADIES HATS
Accessories|Accessories:LADIES HW SCARVES
Accessories|Accessories:Ladies Jewellery
Accessories|Accessories:Ladies Scarves
Accessories|Accessories:Ladies Sunglasses
Accessories|Accessories:Ladies Umbrellas
Accessories|Accessories:Luggage
Accessories|Accessories:LW SCARVES
Accessories|Accessories:MAKE-UP BAGS
Accessories|Accessories:Mens Accessories
Accessories|Accessories:Purses
Accessories|Accessories:READING GLASSES
Accessories|Accessories:Sports Events D1
Accessories|Accessories:SUNGLASSES
Accessories|Accessories:UMBRELLAS
Accessories|Accessories:UNASSIGNED D1
Accessories|Accessories:Unknown
Accessories|Accessories:WATCHES
Accessories|Accessories:WORLD CUP
Bag Levy|Bag Levy:Paper Bags
Bag Levy|Bag Levy:UNASSIGNED D30
Concessions|Concessions:Barbers
Concessions|Concessions:Beauty Salon
Concessions|Concessions:DUMMY
Concessions|Concessions:Entertainment
Concessions|Concessions:Pop-up Shop
Concessions|Concessions:UNASSIGNED D28
Dummy|Dummy:Dummy
Dummy Dept for TBC order|Dummy Dept for TBC order:Dummy Clas for TBC order
Gift Cards|Gift Cards:Gift Cards
Gift Cards|Gift Cards:UNASSIGNED D32
Goods Not For Resale|Goods Not For Resale:Bags D31
Goods Not For Resale|Goods Not For Resale:Baskets
Goods Not For Resale|Goods Not For Resale:Consumables
Goods Not For Resale|Goods Not For Resale:Epic Merch
Goods Not For Resale|Goods Not For Resale:FSDU
Goods Not For Resale|Goods Not For Resale:Mannequins
Goods Not For Resale|Goods Not For Resale:Till Rolls
Goods Not For Resale|Goods Not For Resale:UNASSIGNED D31
Goods Not For Resale|Goods Not For Resale:Unknown
Health & Beauty|Health & Beauty:Accessories
Health & Beauty|Health & Beauty:Beauty Essentials
Health & Beauty|Health & Beauty:Branded Cosmetics
Health & Beauty|Health & Beauty:Confectionery
Health & Beauty|Health & Beauty:Cosmetics
Health & Beauty|Health & Beauty:DUMMY
Health & Beauty|Health & Beauty:EDB ACCESSORIES
Health & Beauty|Health & Beauty:EDB COSMETICS
Health & Beauty|Health & Beauty:EDB TOILETRIES
Health & Beauty|Health & Beauty:Electricals
Health & Beauty|Health & Beauty:Events
Health & Beauty|Health & Beauty:False Nails and Lashes
Health & Beauty|Health & Beauty:Fragrance
Health & Beauty|Health & Beauty:GIFTS
Health & Beauty|Health & Beauty:Hair
Health & Beauty|Health & Beauty:Health & Wellbeing
Health & Beauty|Health & Beauty:Hygiene
Health & Beauty|Health & Beauty:Kids Health and Beauty
Health & Beauty|Health & Beauty:Love Beauty
Health & Beauty|Health & Beauty:MAKE UP
Health & Beauty|Health & Beauty:Mens Grooming
Health & Beauty|Health & Beauty:SKIN CARE
Health & Beauty|Health & Beauty:Skincare
Health & Beauty|Health & Beauty:SPECIAL OFFERS
Health & Beauty|Health & Beauty:Tanning
Health & Beauty|Health & Beauty:TISSUES
Health & Beauty|Health & Beauty:Toiletries
Health & Beauty|Health & Beauty:UNASSIGNED D23
Health & Beauty|Health & Beauty:Unknown
Health & Beauty|Health & Beauty:XMAS GIFTS
Home|Home:Baby Bedding
Home|Home:Baby Blankets
Home|Home:Bathroom
Home|Home:Candles
Home|Home:Curtains
Home|Home:CUSHIONS
Home|Home:DUMMY
Home|Home:DUVET COVERS
Home|Home:Duvets
Home|Home:Filled Product
Home|Home:Home Accessories
Home|Home:Kids Home
Home|Home:KITCHEN
Home|Home:Licensed Home
Home|Home:Lifestyle
Home|Home:Lights
Home|Home:Living Cushions
Home|Home:Living Throws
Home|Home:LUGGAGE
Home|Home:Paper
Home|Home:Paper Products
Home|Home:Pillows
Home|Home:Plain Bedding
Home|Home:Promotions
Home|Home:Seasonal
Home|Home:Speciality Bedding
Home|Home:Sports Events D11
Home|Home:Storage
Home|Home:Throws
Home|Home:Towels
Home|Home:Toys
Home|Home:Transfers
Home|Home:UNASSIGNED D11
Home|Home:Unknown
In-Store Charity|In-Store Charity:UNASSIGNED D33
Kids Accessories|Kids Accessories:Baby Accessories
Kids Accessories|Kids Accessories:Baby Footwear
Kids Accessories|Kids Accessories:Baby Socks
Kids Accessories|Kids Accessories:Boys Accessories
Kids Accessories|Kids Accessories:Boys Footwear
Kids Accessories|Kids Accessories:Boys Nightwear
Kids Accessories|Kids Accessories:Boys Socks
Kids Accessories|Kids Accessories:Boys Underwear
Kids Accessories|Kids Accessories:Girls Accessories
Kids Accessories|Kids Accessories:Girls Footwear
Kids Accessories|Kids Accessories:Girls Hosiery
Kids Accessories|Kids Accessories:Girls Nightwear
Kids Accessories|Kids Accessories:Girls Underwear
Kids Accessories|Kids Accessories:Kids Accessories
Kids Accessories|Kids Accessories:Kids Accessories Sports Events
Kids Accessories|Kids Accessories:Kids Footwear
Kids Accessories|Kids Accessories:Kids Hosiery
Kids Accessories|Kids Accessories:Kids Nightwear
Kids Accessories|Kids Accessories:Kids Underwear
Kids Accessories|Kids Accessories:UNASSIGNED D15
Kids Accessories|Kids Accessories:Unknown
Kids Clothing|Kids Clothing:2-7 Boyswear
Kids Clothing|Kids Clothing:2-7 Girlswear
Kids Clothing|Kids Clothing:7+ Boyswear
Kids Clothing|Kids Clothing:7+ Girlswear
Kids Clothing|Kids Clothing:Baby Basics
Kids Clothing|Kids Clothing:Baby Boy
Kids Clothing|Kids Clothing:Baby Girl
Kids Clothing|Kids Clothing:Babywear
Kids Clothing|Kids Clothing:CHILDRENS HOSIERY
Kids Clothing|Kids Clothing:DUMMY
Kids Clothing|Kids Clothing:Kids Hosiery
Kids Clothing|Kids Clothing:Kids Nightwear
Kids Clothing|Kids Clothing:Kids Sports Events
Kids Clothing|Kids Clothing:Kids Underwear
Kids Clothing|Kids Clothing:MISC
Kids Clothing|Kids Clothing:Newborn Boy
Kids Clothing|Kids Clothing:Newborn Girl
Kids Clothing|Kids Clothing:OUTERWEAR
Kids Clothing|Kids Clothing:SCHOOLWEAR
Kids Clothing|Kids Clothing:UNASSIGNED D5
Kids Clothing|Kids Clothing:UNDERWEAR
Kids Clothing|Kids Clothing:Unknown
Ladies Clothing|Ladies Clothing:Basic T Shirts
Ladies Clothing|Ladies Clothing:Cardigans
Ladies Clothing|Ladies Clothing:Casual Bottoms
Ladies Clothing|Ladies Clothing:CASUAL JERSEY BOTTOMS
Ladies Clothing|Ladies Clothing:CASUAL OUTERWEAR
Ladies Clothing|Ladies Clothing:Casual Shorts
Ladies Clothing|Ladies Clothing:Co-ordinates
Ladies Clothing|Ladies Clothing:Coats
Ladies Clothing|Ladies Clothing:Contemporary Collections
Ladies Clothing|Ladies Clothing:Dresses & Skirts
Ladies Clothing|Ladies Clothing:DUMMY
Ladies Clothing|Ladies Clothing:Edit
Ladies Clothing|Ladies Clothing:Essential Jersey
Ladies Clothing|Ladies Clothing:Fashion Jersey
Ladies Clothing|Ladies Clothing:Formal Jackets
Ladies Clothing|Ladies Clothing:FORMAL SKIRTS
Ladies Clothing|Ladies Clothing:Formal Trousers
Ladies Clothing|Ladies Clothing:IRISH
Ladies Clothing|Ladies Clothing:Jersey Tops Table
Ladies Clothing|Ladies Clothing:Jumpers
Ladies Clothing|Ladies Clothing:Ladies Denim
Ladies Clothing|Ladies Clothing:Ladies Limited Edition
Ladies Clothing|Ladies Clothing:Ladies Performancewear
Ladies Clothing|Ladies Clothing:Ladies Shorts
Ladies Clothing|Ladies Clothing:Licensed Womens
Ladies Clothing|Ladies Clothing:LS Cotton Tops
Ladies Clothing|Ladies Clothing:Maternity
Ladies Clothing|Ladies Clothing:Outerwear/Coats
Ladies Clothing|Ladies Clothing:Preloved
Ladies Clothing|Ladies Clothing:Shorts
Ladies Clothing|Ladies Clothing:Skirts
Ladies Clothing|Ladies Clothing:Smart Jersey Tops
Ladies Clothing|Ladies Clothing:Soft Skirts
Ladies Clothing|Ladies Clothing:SPARE
Ladies Clothing|Ladies Clothing:Sports Tops
Ladies Clothing|Ladies Clothing:SPORTSWEAR
Ladies Clothing|Ladies Clothing:Swim & Beach
Ladies Clothing|Ladies Clothing:Tops
Ladies Clothing|Ladies Clothing:Trousers and Formal Jkts
Ladies Clothing|Ladies Clothing:UNASSIGNED D8
Ladies Clothing|Ladies Clothing:Unknown
Ladies Clothing|Ladies Clothing:Woven Tops & Bottoms
Ladies Clothing|Ladies Clothing:Youth
Ladies Footwear|Ladies Footwear:Babies
Ladies Footwear|Ladies Footwear:Beach
Ladies Footwear|Ladies Footwear:Casual Footwear
Ladies Footwear|Ladies Footwear:DUMMY
Ladies Footwear|Ladies Footwear:Flats
Ladies Footwear|Ladies Footwear:Footwear Accessories
Ladies Footwear|Ladies Footwear:Heels
Ladies Footwear|Ladies Footwear:KIDS SHOES
Ladies Footwear|Ladies Footwear:Kids Slippers
Ladies Footwear|Ladies Footwear:Ladies Boots
Ladies Footwear|Ladies Footwear:LADIES CANVAS
Ladies Footwear|Ladies Footwear:Ladies Leisure
Ladies Footwear|Ladies Footwear:LADIES SANDALS
Ladies Footwear|Ladies Footwear:Ladies Slippers
Ladies Footwear|Ladies Footwear:LADIES SPORTS & LEISURE
Ladies Footwear|Ladies Footwear:Ladies Wide Fit
Ladies Footwear|Ladies Footwear:MENS SLIPPERS
Ladies Footwear|Ladies Footwear:Older Boys
Ladies Footwear|Ladies Footwear:Older Girls
Ladies Footwear|Ladies Footwear:Sandals
Ladies Footwear|Ladies Footwear:Sports Events D7
Ladies Footwear|Ladies Footwear:UNASSIGNED D7
Ladies Footwear|Ladies Footwear:Unknown
Ladies Footwear|Ladies Footwear:WIDE FIT
Ladies Footwear|Ladies Footwear:Younger Boys
Ladies Footwear|Ladies Footwear:Younger Girls
Ladies Hosiery|Ladies Hosiery:Broadfolds
Ladies Hosiery|Ladies Hosiery:Control and Support
Ladies Hosiery|Ladies Hosiery:DESIGN AND FASHION HOSIERY
Ladies Hosiery|Ladies Hosiery:DUMMY
Ladies Hosiery|Ladies Hosiery:Fashion Hosiery
Ladies Hosiery|Ladies Hosiery:Fashion Socks
Ladies Hosiery|Ladies Hosiery:KNEEHIGHS AND FOOTIES
Ladies Hosiery|Ladies Hosiery:Ladies Socks
Ladies Hosiery|Ladies Hosiery:Licensed Product
Ladies Hosiery|Ladies Hosiery:MULTIPACKS
Ladies Hosiery|Ladies Hosiery:Opaques
Ladies Hosiery|Ladies Hosiery:OTHERS
Ladies Hosiery|Ladies Hosiery:Patterned Socks
Ladies Hosiery|Ladies Hosiery:Plain Socks
Ladies Hosiery|Ladies Hosiery:Sheer Tights
Ladies Hosiery|Ladies Hosiery:Shoe Liners
Ladies Hosiery|Ladies Hosiery:Slipper Socks
Ladies Hosiery|Ladies Hosiery:Sports Events D2
Ladies Hosiery|Ladies Hosiery:Sports Socks
Ladies Hosiery|Ladies Hosiery:UNASSIGNED D2
Ladies Hosiery|Ladies Hosiery:Unknown
Mens Accessories|Mens Accessories:Bags/Wallets
Mens Accessories|Mens Accessories:BELTS
Mens Accessories|Mens Accessories:BOXERS
Mens Accessories|Mens Accessories:BRIEFS
Mens Accessories|Mens Accessories:Entertainment
Mens Accessories|Mens Accessories:GIFTS
Mens Accessories|Mens Accessories:GOWNS
Mens Accessories|Mens Accessories:Mens Gifts
Mens Accessories|Mens Accessories:Mens Jewellery
Mens Accessories|Mens Accessories:Mens Non-Seasonal Access
Mens Accessories|Mens Accessories:Mens Seasonal Accessories
Mens Accessories|Mens Accessories:Mens Sunglasses
Mens Accessories|Mens Accessories:Mens Umbrellas
Mens Accessories|Mens Accessories:Mens Underwear
Mens Accessories|Mens Accessories:PYJAMAS
Mens Accessories|Mens Accessories:Robes
Mens Accessories|Mens Accessories:SHOES
Mens Accessories|Mens Accessories:Slippers
Mens Accessories|Mens Accessories:Socks
Mens Accessories|Mens Accessories:Sports Events D16
Mens Accessories|Mens Accessories:SUNGLASSES
Mens Accessories|Mens Accessories:UMBRELLAS
Mens Accessories|Mens Accessories:UNASSIGNED D16
Mens Accessories|Mens Accessories:Unknown
Mens Accessories|Mens Accessories:Vests
Mens Accessories|Mens Accessories:VESTS/THERMALS
Mens Accessories|Mens Accessories:WORLD CUP
Mens Clothing|Mens Clothing:Basic Leisurewear
Mens Clothing|Mens Clothing:BASIC T-SHIRTS
Mens Clothing|Mens Clothing:BOXERS
Mens Clothing|Mens Clothing:Casual Shirts
Mens Clothing|Mens Clothing:CASUAL TROUSERS
Mens Clothing|Mens Clothing:DENIM
Mens Clothing|Mens Clothing:DUMMY
Mens Clothing|Mens Clothing:FASHION LEISURE
Mens Clothing|Mens Clothing:FASHION LEISUREWEAR
Mens Clothing|Mens Clothing:FASHION T-SHIRTS
Mens Clothing|Mens Clothing:FORMAL JACKETS & TROUSERS
Mens Clothing|Mens Clothing:FORMAL SHIRTS
Mens Clothing|Mens Clothing:Formal Shirts & Ties
Mens Clothing|Mens Clothing:JACKETS
Mens Clothing|Mens Clothing:Knitwear
Mens Clothing|Mens Clothing:L/S T-Shirts
Mens Clothing|Mens Clothing:Licensed Local Sports
Mens Clothing|Mens Clothing:Licensed T-Shirts
Mens Clothing|Mens Clothing:LONG-SLEEVE T-SHIRTS
Mens Clothing|Mens Clothing:Mens Casual Trousers
Mens Clothing|Mens Clothing:Mens Denim
Mens Clothing|Mens Clothing:Mens Formalwear
Mens Clothing|Mens Clothing:Mens Leisurewear
Mens Clothing|Mens Clothing:Mens Limited Edition
Mens Clothing|Mens Clothing:Mens Performancewear
Mens Clothing|Mens Clothing:Mens Shorts
Mens Clothing|Mens Clothing:Mens Swimwear
Mens Clothing|Mens Clothing:Outerwear
Mens Clothing|Mens Clothing:Preloved
Mens Clothing|Mens Clothing:SHORTS
Mens Clothing|Mens Clothing:Ties
Mens Clothing|Mens Clothing:UNASSIGNED D6
Mens Clothing|Mens Clothing:Unknown
Mens Clothing|Mens Clothing:WORLD CUP
Primarket|Primarket:DUMMY
Primarket|Primarket:Entertainment
Primarket|Primarket:Events
Primarket|Primarket:Experiences
Primarket|Primarket:Food
Primarket|Primarket:Gifts
Primarket|Primarket:Inflatables
Primarket|Primarket:Paper
Primarket|Primarket:Pet
Primarket|Primarket:Stationery
Primarket|Primarket:Technology
Primarket|Primarket:Toys
Primarket|Primarket:Travel
Primarket|Primarket:UNASSIGNED D25
Primarket|Primarket:Unknown
Sports Shop|Sports Shop:DUMMY
Sports Shop|Sports Shop:Kids
Sports Shop|Sports Shop:Ladies
Sports Shop|Sports Shop:LADIES BRANDED
Sports Shop|Sports Shop:LADIES PERFORMANCE
Sports Shop|Sports Shop:Mens
Sports Shop|Sports Shop:MENS BRANDED
Sports Shop|Sports Shop:MENS PERFORMANCE
Sports Shop|Sports Shop:Socks
Sports Shop|Sports Shop:UNASSIGNED
Sports Shop|Sports Shop:Unknown
Uwear & Nwear|Uwear & Nwear:Beachwear
Uwear & Nwear|Uwear & Nwear:BRA ACCESSORIES
Uwear & Nwear|Uwear & Nwear:Bras
Uwear & Nwear|Uwear & Nwear:Camisoles
Uwear & Nwear|Uwear & Nwear:Co-ordinates D4
Uwear & Nwear|Uwear & Nwear:CO-ORDS
Uwear & Nwear|Uwear & Nwear:Comfort Briefs
Uwear & Nwear|Uwear & Nwear:DUMMY
Uwear & Nwear|Uwear & Nwear:Folded Pyjamas
Uwear & Nwear|Uwear & Nwear:GLAMOUR
Uwear & Nwear|Uwear & Nwear:Glamour Nightwear
Uwear & Nwear|Uwear & Nwear:HANGING PYJAMAS
Uwear & Nwear|Uwear & Nwear:Ladies Swimwear
Uwear & Nwear|Uwear & Nwear:Licensed Nightwear
Uwear & Nwear|Uwear & Nwear:LOUNGEWEAR
Uwear & Nwear|Uwear & Nwear:Maternity
Uwear & Nwear|Uwear & Nwear:Nightshirts
Uwear & Nwear|Uwear & Nwear:Onesies & Twosies
Uwear & Nwear|Uwear & Nwear:Packed Briefs
Uwear & Nwear|Uwear & Nwear:PJ Separates
Uwear & Nwear|Uwear & Nwear:ROBES
Uwear & Nwear|Uwear & Nwear:SEPARATES
Uwear & Nwear|Uwear & Nwear:Sets
Uwear & Nwear|Uwear & Nwear:Shapewear
Uwear & Nwear|Uwear & Nwear:SHAPEWEAR SOLUTIONS-SHAPEWEAR
Uwear & Nwear|Uwear & Nwear:SLEEPSUITS
Uwear & Nwear|Uwear & Nwear:SMOOTHLINE
Uwear & Nwear|Uwear & Nwear:SPECIALIST BRIEFS
Uwear & Nwear|Uwear & Nwear:Sports Events D4
Uwear & Nwear|Uwear & Nwear:SWIMWEAR
Uwear & Nwear|Uwear & Nwear:Table Briefs
Uwear & Nwear|Uwear & Nwear:THERMAL
Uwear & Nwear|Uwear & Nwear:UK DISCONTINUED
Uwear & Nwear|Uwear & Nwear:UNASSIGNED D4
Uwear & Nwear|Uwear & Nwear:Unknown
Uwear & Nwear|Uwear & Nwear:WORLD CUP
Xmas Shop|Xmas Shop:All Year Around
Xmas Shop|Xmas Shop:Books
Xmas Shop|Xmas Shop:Candles/Holders
Xmas Shop|Xmas Shop:CARDS
Xmas Shop|Xmas Shop:CHRISTMAS GIFTS
Xmas Shop|Xmas Shop:CRACKERS
Xmas Shop|Xmas Shop:DUMMY
Xmas Shop|Xmas Shop:Halloween
Xmas Shop|Xmas Shop:Lights
Xmas Shop|Xmas Shop:Room Theme
Xmas Shop|Xmas Shop:Soft Toys
Xmas Shop|Xmas Shop:Toys
Xmas Shop|Xmas Shop:TREE DECORATIONS
Xmas Shop|Xmas Shop:Trees/Garlands
Xmas Shop|Xmas Shop:UNASSIGNED
Xmas Shop|Xmas Shop:Unknown
Xmas Shop|Xmas Shop:Wrapping/Bags
"""

def parse_hierarchy():
    """Parse raw hierarchy into structured dictionary."""
    hierarchy = defaultdict(list)
    
    for line in raw_hierarchy.strip().split('\n'):
        if not line:
            continue
        dept, class_name = line.split('|')
        # Extract just the class part after the colon
        class_short = class_name.split(':')[1] if ':' in class_name else class_name
        if class_short not in hierarchy[dept]:
            hierarchy[dept].append(class_short)
    
    return dict(hierarchy)

def print_summary(hierarchy):
    """Print summary statistics."""
    print(f"\n{'='*60}")
    print(f"PRODUCT HIERARCHY SUMMARY")
    print(f"{'='*60}")
    print(f"Total Departments: {len(hierarchy)}")
    print(f"Total Classes: {sum(len(classes) for classes in hierarchy.values())}")
    print(f"\nDepartments:")
    for dept in sorted(hierarchy.keys()):
        print(f"  - {dept}: {len(hierarchy[dept])} classes")

def save_to_yaml(hierarchy, output_path='hierarchy_parsed.yml'):
    """Save parsed hierarchy to YAML file."""
    with open(output_path, 'w') as f:
        yaml.dump({'departments': hierarchy}, f, default_flow_style=False, sort_keys=False)
    print(f"\n✅ Saved to {output_path}")

if __name__ == "__main__":
    hierarchy = parse_hierarchy()
    print_summary(hierarchy)
    save_to_yaml(hierarchy)
    
    # Print first 3 departments as example
    print(f"\nExample (first 3 departments):")
    for dept in list(hierarchy.keys())[:3]:
        print(f"\n{dept}:")
        for cls in hierarchy[dept][:5]:
            print(f"  - {cls}")
        if len(hierarchy[dept]) > 5:
            print(f"  ... and {len(hierarchy[dept]) - 5} more")
