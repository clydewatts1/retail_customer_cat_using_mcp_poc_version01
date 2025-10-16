# Normalized Product Hierarchy for Fuzzy Clustering Input
This table contains a large sample of the product lines, transformed from the retailer-specific nomenclature into a new, generic, and standardized four-level structure suitable for data analysis and neural network input.Key Fields in New Structure:Gender_Age: The computed primary segment (Woman, Man, Boy, Girl, Baby, Child, Adult, Unknown).Normalized_Department: High-level retail grouping (Apparel, Intimates & Swim, Home & Lifestyle, etc.).Normalized_Class: Mid-level product type (Knit & Jersey Tops, Outerwear, Skincare & Hygiene, etc.).Normalized_Subclass: Granular product detail (T-Shirts/Vests, Pajamas, Bags/Totes, etc.).Fixed-Format Data for Copy-PasteFor guaranteed integrity when pasting into code or analysis tools, the structure below is preserved by the encompassing code block. The pipe (|) characters act as column delimiters.
"""
| **Gender_Age** | **Normalized_Department** | **Normalized_Class** | **Normalized_Subclass** |
| :--- | :--- | :--- | :--- |
| Adult | Accessories & Footwear | Bags & Wallets | Backpacks/Luggage |
| Adult | Accessories & Footwear | Bags & Wallets | Handbags/Totes |
| Adult | Accessories & Footwear | Bags & Wallets | Purses/Wallets |
| Woman | Accessories & Footwear | Bags & Wallets | Clutch/Occasion Bags |
| Man | Accessories & Footwear | Soft & Hard Accessories | Gents Jewellery/Misc |
| Adult | Health & Wellness | Consumables | Confectionery/Snacks |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Basic Gloves |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Fashion/Novelty Gloves |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Hair Accessories/Tools |
| Child | Accessories & Footwear | Soft & Hard Accessories | Hair Accessories (Kids) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Basic Hats |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Fashion/Wool/Straw Hats |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Headbands & Earmuffs |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Scarves & Snoods (Heavy) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Scarves & Snoods (Light) |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Necklaces (Fashion/Allway) |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Earrings (Hoop/Drop/Stud) |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Bracelets/Bangles |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Rings/Body Jewellery |
| Child | Accessories & Footwear | Bags & Wallets | Kids Bags/Purses |
| Child | Accessories & Footwear | Soft & Hard Accessories | Kids Belts/Hats/Gloves |
| Baby | Accessories & Footwear | Soft & Hard Accessories | Baby Hats/Gloves/Sets |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Belts (Jean/Skinny/Waist) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Gloves (Leather/Knitted) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Scarves (Heavy Design/Plain) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Scarves (Light Design/Plain) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Sunglasses (Aviator/Cat Eye) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Umbrellas (Plain/Print) |
| Adult | Accessories & Footwear | Bags & Wallets | Travel/Luggage Accessories |
| Adult | Health & Wellness | Personal Care Tools | Make-up/Wash Bags |
| Man | Health & Wellness | Personal Care Tools | Mens Grooming Bags |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Reading Glasses |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Sunglasses (Basic/Fashion) |
| Adult | Non-Core Retail | Services/Other | Bag Levy |
| Unknown | Non-Core Retail | Services/Other | Concession - Beauty Services |
| Unknown | Non-Core Retail | Services/Other | Concession - Entertainment |
| Unknown | Non-Core Retail | Services/Other | Goods Not For Resale (GNR) |
| Adult | Health & Wellness | Personal Care Tools | Beauty Tools/Accessories |
| Adult | Health & Wellness | Consumables | Wipes/Cotton Wool/Tissues |
| Adult | Health & Wellness | Cosmetics & Fragrance | Branded Cosmetics (Face/Hair) |
| Adult | Health & Wellness | Cosmetics & Fragrance | Own Label/Value Cosmetics |
| Adult | Health & Wellness | Personal Care Tools | Electricals (Hair/Dental/Body) |
| Adult | Health & Wellness | Seasonal/Events | H&B Seasonal Gifts (Xmas/Valentine) |
| Adult | Health & Wellness | Cosmetics & Fragrance | False Nails & Lashes |
| Adult | Health & Wellness | Cosmetics & Fragrance | Fragrance (Branded/Own Label) |
| Adult | Health & Wellness | Personal Care | Hair Care (Shampoo/Styling) |
| Adult | Health & Wellness | Health & Wellbeing | Vitamins & Supplements |
| Adult | Health & Wellness | Personal Care | Hygiene (Deodorants/Bodywash) |
| Child | Health & Wellness | Kids H&B | Kids Accessories/Cosmetics |
| Man | Health & Wellness | Mens Grooming | Mens Accessories/Skincare |
| Adult | Health & Wellness | Personal Care | Skincare (Body/Face/Lip) |
| Adult | Health & Wellness | Personal Care | Tanning & Suncare |
| Adult | Home & Lifestyle | Bedding | Baby Bedding/Blankets |
| Adult | Home & Lifestyle | Bath & Laundry | Bathroom Accessories/Rugs |
| Adult | Home & Lifestyle | Decor & Furnishings | Candles & Home Fragrance |
| Adult | Home & Lifestyle | Soft Furnishings | Curtains |
| Adult | Home & Lifestyle | Soft Furnishings | Cushions (Bedroom/Living) |
| Adult | Home & Lifestyle | Bedding | Duvet Covers/Sets |
| Adult | Home & Lifestyle | Bedding | Pillows/Duvets/Protectors |
| Adult | Home & Lifestyle | Decor & Furnishings | Home Accessories/Wall Art |
| Child | Home & Lifestyle | Kids Home | Kids Home Accessories/Storage |
| Adult | Home & Lifestyle | Kitchen & Misc | Kitchenware & Table Top |
| Adult | Home & Lifestyle | Decor & Furnishings | Lighting/Lamp Shades |
| Adult | Home & Lifestyle | Kitchen & Misc | Lifestyle/Travel/Pets |
| Adult | Home & Lifestyle | Kitchen & Misc | Paper Products/Stationary |
| Adult | Home & Lifestyle | Bedding | Plain Dye Bedding (Sheets/Sets) |
| Adult | Home & Lifestyle | Seasonal/Events | Seasonal Decor/Lights/Gifts |
| Adult | Home & Lifestyle | Storage & Org | Storage Bins/Hangers |
| Adult | Home & Lifestyle | Soft Furnishings | Throws (Bedroom/Living) |
| Adult | Home & Lifestyle | Bath & Laundry | Towels (Beach/Value/Premium) |
| Child | Home & Lifestyle | Toys & Games | Soft Toys/Licensed Toys |
| Baby | Accessories & Footwear | Baby Accessories | Baby Essentials/Footwear |
| Boy | Accessories & Footwear | Footwear | Boys Boots/Shoes/Slippers |
| Boy | Intimates & Swim | Boys Underwear/Nightwear | Boys Boxers/Briefs/Vests |
| Boy | Intimates & Swim | Boys Underwear/Nightwear | Boys Sleepsuits/Gowns |
| Boy | Accessories & Footwear | Hosiery | Boys Socks/Heavy Socks |
| Girl | Accessories & Footwear | Footwear | Girls Boots/Shoes/Slippers |
| Girl | Intimates & Swim | Girls Underwear/Nightwear | Girls Briefs/Vests/Sets |
| Girl | Intimates & Swim | Girls Underwear/Nightwear | Girls Sleepsuits/Gowns |
| Girl | Accessories & Footwear | Hosiery | Girls Socks/Tights |
| Child | Accessories & Footwear | Kids Footwear/Hosiery | Licensed/Novelty Socks/Footwear |
| Boy | Apparel | Knit & Jersey Tops | Boys Tees/Leisure Tops (2-7yr) |
| Boy | Apparel | Trousers & Shorts | Boys Leisure Bottoms/Denim (2-7yr) |
| Girl | Apparel | Dresses & Skirts | Girls Dresses/Skirts (2-7yr) |
| Girl | Apparel | Knit & Jersey Tops | Girls Tees/Leisure Tops (2-7yr) |
| Boy | Apparel | Knit & Jersey Tops | Boys Tees/Leisure Tops (7+yr) |
| Girl | Apparel | Dresses & Skirts | Girls Dresses/Skirts (7+yr) |
| Girl | Apparel | Knit & Jersey Tops | Girls Tees/Leisure Tops (7+yr) |
| Baby | Apparel | Baby Basics | Bodysuits/Sleepsuits/Layette |
| Baby | Apparel | Baby Wear (Boy) | Denim/Outfits/Tops/Bottoms |
| Baby | Apparel | Baby Wear (Girl) | Dresses/Outfits/Tops/Bottoms |
| Child | Apparel | Schoolwear | Uniforms/Accessories |
| Baby | Apparel | Newborn | All-in-Ones/Knitwear/Sets (0-2yr) |
| Woman | Apparel | Knit & Jersey Tops | Basic Cotton Tees/Vests |
| Woman | Apparel | Knitwear | Cardigans (Fine/Heavy Gauge) |
| Woman | Apparel | Trousers & Shorts | Casual Leggings/Joggers/Shorts |
| Woman | Apparel | Outerwear | Casual Jackets/Gilets/Rainwear |
| Woman | Apparel | Dresses & Skirts | Co-ordinate Sets (Work/Casual) |
| Woman | Apparel | Outerwear | Formal/Fashion Coats & Macs |
| Woman | Apparel | Dresses & Skirts | Day/Sundresses (Jersey/Woven) |
| Woman | Apparel | Dresses & Skirts | Formal/Party Dresses/Jumpsuits |
| Woman | Apparel | Tops & Blouses | Smart Jersey Tops (Cami/Tee) |
| Woman | Apparel | Trousers & Shorts | Formal Trousers/Tailoring |
| Woman | Apparel | Knitwear | Jumpers (Wool Mix/Fine Gauge) |
| Woman | Apparel | Denimwear | Jeans (Skinny/Straight/Boyfriend) |
| Woman | Apparel | Denimwear | Denim Jackets/Skirts/Shorts |
| Woman | Apparel | Activewear | Performance Leggings/Tops/Sweats |
| Woman | Apparel | Trousers & Shorts | Soft Skirts/Skorts/Maxi Skirts |
| Man | Apparel | Activewear | Active Fleece/Joggers/Shorts |
| Man | Apparel | Knit & Jersey Tops | Basic Crew/Vee Tees/Polos |
| Man | Apparel | Tops & Blouses | Casual Shirts (Long/Short Sleeve) |
| Man | Apparel | Trousers & Shorts | Chino/Cargo/Linen Trousers |
| Man | Apparel | Denimwear | Jeans (Slim/Straight/Worker) |
| Man | Apparel | Knit & Jersey Tops | Fashion Prints/Licensed Tees/Polos |
| Man | Apparel | Outerwear | Formal/Suit Jackets & Trousers |
| Man | Apparel | Knitwear | Jumpers/Cardigans (Fine/Mid Gauge) |
| Man | Apparel | Outerwear | Casual Jackets/Puffers/Gilets |
| Man | Apparel | Activewear | Performance Joggers/Shorts/Tops |
| Man | Apparel | Trousers & Shorts | Chino/Denim/Cargo Shorts |
| Man | Apparel | Swim & Beachwear | Basic/Fashion Swim Shorts |
| Man | Accessories & Footwear | Soft & Hard Accessories | Ties/Cufflinks/Gifting |
| Woman | Accessories & Footwear | Footwear | Beach Flip Flops/Sliders |
| Woman | Accessories & Footwear | Footwear | Flats (Ballerinas/Loafers) |
| Woman | Accessories & Footwear | Footwear | Heels (Courts/Sandals) |
| Woman | Accessories & Footwear | Footwear | Boots (Casual/Formal/Welly) |
| Woman | Accessories & Footwear | Footwear | Canvas/Leisure Sneakers |
| Woman | Accessories & Footwear | Footwear | Wide Fit Footwear |
| Woman | Accessories & Footwear | Hosiery | Basic/Sheer/Opaque Tights |
| Woman | Accessories & Footwear | Hosiery | Fashion/Design Hosiery |
| Woman | Accessories & Footwear | Hosiery | Socks (Ankle/Knee High/Shoe Liners) |
| Woman | Accessories & Footwear | Hosiery | Slipper Socks/Booties |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Boxers/Briefs (Multipack/Fashion) |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Robes/Gowns |
| Man | Accessories & Footwear | Footwear | Mens Casual/Formal Shoes |
| Man | Accessories & Footwear | Footwear | Mens Boots/Canvas/Sports |
| Man | Accessories & Footwear | Footwear | Mens Slippers/Novelty |
| Man | Accessories & Footwear | Hosiery | Mens Socks (Formal/Casual/Sports) |
| Woman | Intimates & Swim | Underwear & Bras | Bras (T-Shirt/Sports/Lace) |
| Woman | Intimates & Swim | Underwear & Bras | Briefs/Thongs/Boxers (Multipack) |
| Woman | Intimates & Swim | Underwear & Bras | Co-ordinate Sets (Lace/Satin/Smooth) |
| Woman | Intimates & Swim | Sleep & Lounge | Folded/Hanging Pyjamas |
| Woman | Intimates & Swim | Sleep & Lounge | Nightshirts/Sleepsuits/Onesies |
| Woman | Intimates & Swim | Sleep & Lounge | Robes (Cotton/Fleece/Sherpa) |
| Woman | Intimates & Swim | Swim & Beachwear | Bikinis/Swimsuits/Cover Ups |
| Woman | Intimates & Swim | Shapewear | Shapewear Tops/Bottoms |
| Woman | Intimates & Swim | Underwear & Bras | Thermal Camis/Leggings |
| Adult | Non-Core Retail | Services/Other | Concession Services |
| Adult | Non-Core Retail | Services/Other | Gift Cards |
| Adult | Non-Core Retail | Services/Other | Goods Not For Resale (Equipment) |
| Adult | Home & Lifestyle | Kitchen & Misc | Entertainment (CD/DVD) |
| Adult | Home & Lifestyle | Kitchen & Misc | Pet Accessories |
| Adult | Home & Lifestyle | Kitchen & Misc | Stationery/Books |
| Adult | Home & Lifestyle | Kitchen & Misc | Technology/Accessories |
| Adult | Home & Lifestyle | Toys & Games | Inflatables/Toys |
| Woman | Apparel | Trousers & Shorts | Performance Jog Legs |
| Man | Apparel | Activewear | Thermo Layer Tops/Bottoms |
| Woman | Apparel | Activewear | Branded Activewear |
| Man | Apparel | Activewear | Branded Piques/Shorts |
| Unknown | Unknown | Unknown | Unknown/Unassigned Stock |
| Adult | Home & Lifestyle | Seasonal/Events | Xmas Shop Cards/Wrap/Lights |
| Adult | Home & Lifestyle | Toys & Games | Xmas Shop Soft Toys |
| Adult | Home & Lifestyle | Decor & Furnishings | Xmas Shop Tree Decorations |
| Adult | Health & Wellness | Consumables | Confectionery (Branded) |
| Adult | Health & Wellness | Consumables | Haribo/Novelty Sweets |
| Woman | Accessories & Footwear | Bags & Wallets | Clutch/Occasion |
| Man | Accessories & Footwear | Soft & Hard Accessories | Braces (Gents Belts) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Fashion Gloves (Leather) |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Fashion Hair Accessories |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Hair Brushes/Salon Tools |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Jewellery (Anklets/Toe Rings) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Ladies Watches |
| Child | Accessories & Footwear | Soft & Hard Accessories | Kids Licensed Accessories |
| Baby | Accessories & Footwear | Baby Accessories | Babies Fabric/Knitted Hats |
| Baby | Accessories & Footwear | Baby Footwear | Baby Footwear/Slippers |
| Child | Accessories & Footwear | Soft & Hard Accessories | Kids Earmuffs/Scarves/Sets |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Armwarmers/Fingerless Gloves |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Fabric/Knitted Ladies Hats |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Soft Unstructured Hats |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Body Jewellery (Ladies) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Key Rings/Charms |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Ladies Wristwear |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Ladies Sunglasses Cases |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Umbrellas (Licensed/LTD Ed) |
| Adult | Accessories & Footwear | Bags & Wallets | Hard/Soft Luggage |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Bandanas/Neckerchiefs |
| Adult | Health & Wellness | Personal Care Tools | Make-up Bags (Kids/Licensed) |
| Man | Accessories & Footwear | Soft & Hard Accessories | Mens Jewellery/Scarves |
| Woman | Accessories & Footwear | Bags & Wallets | Purses (Card Holders/Wallets) |
| Man | Accessories & Footwear | Soft & Hard Accessories | Sunglasses (Mens) |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Cases for Sunglasses |
| Adult | Accessories & Footwear | Bags & Wallets | Travel Umbrellas |
| Unknown | Unknown | Unknown | Department Sales / Soiled |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Ladies Watches |
| Man | Accessories & Footwear | Soft & Hard Accessories | Mens Watches |
| Woman | Apparel | Knit & Jersey Tops | Basic Camis/Vests |
| Woman | Apparel | Knitwear | Cashmere/Wool Mix Cardigans |
| Woman | Apparel | Trousers & Shorts | Chino/Poplin/Linen Shorts |
| Woman | Apparel | Outerwear | Heavyweight Padded/Parkas |
| Woman | Apparel | Outerwear | PU/Rainwear Jackets |
| Woman | Apparel | Dresses & Skirts | Maxi/Midi/Mini Skirts |
| Woman | Apparel | Outerwear | Fur/Textured/Trenches Coats |
| Woman | Apparel | Trousers & Shorts | Luxury Collection Trousers/Skirts |
| Woman | Apparel | Dresses & Skirts | Shirt/Tunic Dresses |
| Woman | Apparel | Tops & Blouses | Essentials Blouses/Woven Tops |
| Woman | Apparel | Outerwear | Item Jackets/Waistcoats (Formal) |
| Woman | Apparel | Trousers & Shorts | Formal Pencil/Mini Skirts |
| Woman | Apparel | Trousers & Shorts | Formal Core/Linen Trousers |
| Woman | Apparel | Knit & Jersey Tops | Long Sleeve Cotton/Stretch Tops |
| Woman | Apparel | Denimwear | Basic/Fashion Denim Jeans |
| Woman | Apparel | Licensed/Limited | Licensed/LTD Edition Apparel |
| Woman | Apparel | Activewear | Performance Crops/Jackets |
| Woman | Apparel | Swim & Beachwear | Swimwear Sets/Cover Ups |
| Woman | Apparel | Knit & Jersey Tops | Knit Dress Jumpers |
| Woman | Apparel | Trousers & Shorts | Wide Leg/Slim/Culotte Trousers |
| Woman | Apparel | Tops & Blouses | Woven Camis/Vests |
| Girl | Accessories & Footwear | Footwear | Older Girls Boots/Shoes/Canvas |
| Boy | Accessories & Footwear | Footwear | Older Boys Boots/Shoes/Canvas |
| Woman | Accessories & Footwear | Hosiery | Sheer Hold-ups/Ankle Highs |
| Man | Accessories & Footwear | Soft & Hard Accessories | Travel/Computer/Wash Bags |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Licensed/Novelty Boxers/Briefs |
| Man | Accessories & Footwear | Soft & Hard Accessories | Cufflinks/Wristwear |
| Man | Accessories & Footwear | Soft & Hard Accessories | Knitted/Woven Hats/Scarves |
| Man | Accessories & Footwear | Hosiery | Trainer/Invisible Socks |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Fleece/Velour Gowns |
| Man | Accessories & Footwear | Footwear | Beach/Formal/Sports Shoes |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Classic/Jersey Pyjamas |
| Man | Apparel | Knit & Jersey Tops | Long Sleeve Fashion/Plain Tees |
| Man | Apparel | Tops & Blouses | Formal Shirts (Slim/Regular) |
| Man | Apparel | Outerwear | Wool/Leather/PU Jackets |
| Man | Apparel | Trousers & Shorts | Premium/Worker Denim |
| Man | Apparel | Licensed/Limited | Licensed/LTD Edition Apparel |
| Man | Apparel | Knitwear | Heavy/Mid Gauge Knitwear |
| Woman | Intimates & Swim | Underwear & Bras | Fuller Figure Bras |
| Woman | Intimates & Swim | Underwear & Bras | Basic/Comfort Briefs (Multipack) |
| Woman | Intimates & Swim | Sleep & Lounge | Flannel/Microfleece Pyjamas |
| Woman | Intimates & Swim | Sleep & Lounge | Satin/Glamour Nightwear |
| Woman | Intimates & Swim | Swim & Beachwear | Bikini Separates/Swimsuits |
| Woman | Intimates & Swim | Underwear & Bras | Smoothline/Novelty Briefs |
| Woman | Intimates & Swim | Sleep & Lounge | Maternity/Maternity Bras |
| Adult | Home & Lifestyle | Kitchen & Misc | Licensed Food/Confectionery |
| Adult | Home & Lifestyle | Kitchen & Misc | Tech Accessories/Cases |
| Adult | Home & Lifestyle | Toys & Games | Outdoor/Plush Toys |
| Unknown | Unknown | Unknown | Sports Shop Unassigned |
| Woman | Apparel | Activewear | Branded Golf/Outdoor |
| Man | Apparel | Activewear | Branded Activewear/Golf |
| Woman | Apparel | Activewear | Performance Ski/Thermo Layer |
| Man | Apparel | Activewear | Performance Ski/Thermo Layer |
| Child | Apparel | Activewear | Kids Thermo Layer |
| Adult | Home & Lifestyle | Seasonal/Events | Xmas Shop Animated/Room Decor |
| Adult | Home & Lifestyle | Seasonal/Events | Xmas Shop Crackers/Gifts |
| Adult | Home & Lifestyle | Seasonal/Events | Xmas Shop Trees/Garlands |
| Adult | Home & Lifestyle | Seasonal/Events | Halloween Decor |
| Adult | Non-Core Retail | Services/Other | In-Store Charity |
| Woman | Apparel | Dresses & Skirts | Jersey/Woven 2-in-1 Dresses |
| Woman | Apparel | Trousers & Shorts | Corduroy/Velour Bottoms |
| Man | Apparel | Outerwear | MW/HW/LW Fashion Jackets |
| Man | Apparel | Licensed/Limited | Licensed Local Sports Apparel |
| Woman | Apparel | Tops & Blouses | Chiffon/Print Woven Blouses |
| Woman | Apparel | Outerwear | Item Jackets (Formal/Tailored) |
| Woman | Apparel | Dresses & Skirts | Kaftans/Beach Cover Ups |
| Man | Accessories & Footwear | Bags & Wallets | Licensed/Fashion Bags |
| Woman | Accessories & Footwear | Hosiery | Control/Support Hosiery |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Thermal Vests/Performance |
| Woman | Intimates & Swim | Underwear & Bras | Licensed Bras/Briefs |
| Woman | Apparel | Licensed/Limited | LTD Edition Trousers/Coats |
| Man | Apparel | Licensed/Limited | LTD Edition Knitwear/Shorts |
| Child | Accessories & Footwear | Baby Footwear | Licensed Baby Shoes |
| Child | Accessories & Footwear | Kids Footwear/Hosiery | Sports Events Hosiery/Footwear |
| Adult | Home & Lifestyle | Kitchen & Misc | Licensed Paper/Stationery |
| Adult | Health & Wellness | Seasonal/Events | Pre Launch Christmas H&B |
| Woman | Apparel | Dresses & Skirts | Ponte/Tailored Dresses |
| Man | Apparel | Outerwear | Preloved/Second Hand Clothing |
| Woman | Apparel | Outerwear | Preloved/Second Hand Clothing |
| Adult | Health & Wellness | Skincare & Hygiene | Teen Skincare |
| Woman | Apparel | Dresses & Skirts | Youth Denim/Knitwear |
| Man | Apparel | Denimwear | Cord/Twill Jeans |
| Man | Apparel | Trousers & Shorts | £X Value Casual Trousers |
| Man | Apparel | Knit & Jersey Tops | £X Value Tees/Polos |
| Woman | Intimates & Swim | Sleep & Lounge | Licensed Nightwear Sets |
| Woman | Intimates & Swim | Underwear & Bras | Special Price Point Briefs |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Single Fashion Boxers/Briefs |
| Woman | Apparel | Knit & Jersey Tops | Licensed/Character Tees |
| Woman | Apparel | Tops & Blouses | Casual Stripe/Check Blouses |
| Woman | Apparel | Denimwear | Boyfriend/High Waisted Jeans |
| Woman | Apparel | Knitwear | Embellished/Patterned Jumpers |
| Woman | Apparel | Outerwear | Gilet (Casual Outerwear) |
| Woman | Apparel | Trousers & Shorts | Harem/Cuff Leggings/Trousers |
| Woman | Apparel | Dresses & Skirts | Jersey/Woven Maxi Dresses |
| Woman | Apparel | Knit & Jersey Tops | Volume/Promo Basic Tees |
| Woman | Apparel | Trousers & Shorts | Skorts (Skirt/Shorts Hybrid) |
| Woman | Apparel | Activewear | Sports Tops (Hoodie/Zip Thru) |
| Woman | Accessories & Footwear | Footwear | Espadrilles/Mules/Toeposts |
| Woman | Accessories & Footwear | Hosiery | Multipack Plain/Pattern Socks |
| Man | Apparel | Knit & Jersey Tops | Fashion Hoodies/Crews |
| Man | Apparel | Tops & Blouses | Shirt & Tie Sets |
| Man | Apparel | Outerwear | Wool/Puffer Coats |
| Man | Accessories & Footwear | Soft & Hard Accessories | Belts (Jean/Formal/Fashion) |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Classic/Novelty Pyjamas |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Pyjama Separates (Jersey/Woven) |
| Man | Accessories & Footwear | Soft & Hard Accessories | Golf/Formal Umbrellas |
| Man | Apparel | Licensed/Limited | World Cup Branded Apparel |
| Woman | Intimates & Swim | Swim & Beachwear | Licensed Swimwear |
| Woman | Intimates & Swim | Underwear & Bras | Maternity Underwear |
| Woman | Intimates & Swim | Sleep & Lounge | Long/Short PJ Sets |
| Woman | Intimates & Swim | Sleep & Lounge | Licensed Pyjamas/Gowns |
| Woman | Intimates & Swim | Sleep & Lounge | Loungewear Tops/Bottoms |
| Woman | Intimates & Swim | Underwear & Bras | Smoothline Boxer/Briefs |
| Woman | Intimates & Swim | Underwear & Bras | Specialist/Novelty Briefs |
| Woman | Intimates & Swim | Sleep & Lounge | Sleepwear Separates (Tops/Legs) |
| Woman | Intimates & Swim | Underwear & Bras | T-Shirt Bras (Multifunction) |
| Woman | Intimates & Swim | Sleep & Lounge | Woven Pyjamas (Folded/Hanging) |
| Woman | Apparel | Licensed/Limited | Christmas Jumpers/Cardigans |
| Woman | Apparel | Trousers & Shorts | Performance Shorts |
| Woman | Apparel | Tops & Blouses | Woven Tops (Chiffon/Going Out) |
| Man | Apparel | Denimwear | Overdye Twills/Bedford Cord |
| Man | Apparel | Trousers & Shorts | Formal Trousers (Waistcoats) |
| Man | Apparel | Knit & Jersey Tops | Licensed L/S T-Shirts |
| Man | Apparel | Outerwear | Leather/Nylon Casual Jackets |
| Man | Apparel | Tops & Blouses | Long Sleeve Fashion/Print Tops |
| Man | Apparel | Tops & Blouses | Formal Shirts (Shirt & Tie Sets) |
| Man | Apparel | Activewear | Licensed Leisurewear |
| Man | Apparel | Trousers & Shorts | Premium/Worker Shorts |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Licensed/Novelty Gowns |
| Man | Intimates & Swim | Mens Underwear/Nightwear | Value/Fashion Hipster/Trunk |
| Adult | Home & Lifestyle | Bath & Laundry | Design Towel Bales/Gym Towels |
| Adult | Home & Lifestyle | Bedding | Brushed Cotton/Percale Bedding |
| Adult | Home & Lifestyle | Decor & Furnishings | Speciality Bedding/Travel Pillows |
| Adult | Home & Lifestyle | Kitchen & Misc | Licensed Kitchenware |
| Adult | Home & Lifestyle | Decor & Furnishings | String/Plug-in Lights |
| Adult | Home & Lifestyle | Kitchen & Misc | Lifestyle Healthy Living/Sports |
| Adult | Home & Lifestyle | Storage & Org | Storage Solutions/Hangers |
| Adult | Home & Lifestyle | Soft Furnishings | Licensed Throws |
| Adult | Home & Lifestyle | Toys & Games | Everyday Soft Toys |
| Woman | Intimates & Swim | Underwear & Bras | Glamour/Satin Sets |
| Woman | Intimates & Swim | Underwear & Bras | Body/Thermal Underwear |
| Woman | Intimates & Swim | Swim & Beachwear | Crochet/Embellished Bikinis |
| Woman | Intimates & Swim | Sleep & Lounge | Licensed Nightshirts |
| Man | Apparel | Knit & Jersey Tops | Muscle Fit/Slim Fit Tees |
| Man | Apparel | Knit & Jersey Tops | Semi Plain/Stripe Tees |
| Man | Apparel | Tops & Blouses | S/S Yarn Dye/Print Shirts |
| Man | Apparel | Licensed/Limited | Licensed T-Shirts (Flat/Hanging) |
| Man | Apparel | Swim & Beachwear | Premium/Licensed Swimwear |
| Man | Apparel | Tops & Blouses | Fashion Ties (Silk/Poly) |
| Man | Accessories & Footwear | Soft & Hard Accessories | Mens Watches/Wristwear |
| Man | Accessories & Footwear | Soft & Hard Accessories | Sports Sunglasses |
| Woman | Apparel | Dresses & Skirts | Mini/Midi/Maxi Skirts |
| Woman | Apparel | Dresses & Skirts | Formal Skirts (Bubble/Tulip) |
| Woman | Apparel | Trousers & Shorts | Performance Jog/Woven Shorts |
| Woman | Apparel | Tops & Blouses | Fashion Blouses/Key Basics |
| Woman | Accessories & Footwear | Footwear | Fashion/Value Canvas |
| Woman | Accessories & Footwear | Footwear | Flat/Heeled Sandals |
| Man | Apparel | Knitwear | Lambswool/Luxury Knitwear |
| Man | Apparel | Knit & Jersey Tops | Basic/Fashion Fleece Sweats |
| Man | Apparel | Outerwear | Basic/Fashion Casual Jackets |
| Adult | Health & Wellness | Consumables | Branded/Own Label Confectionery |
| Adult | Health & Wellness | Skincare & Hygiene | Branded/Own Label Dental Care |
| Adult | Health & Wellness | Personal Care | Body/Face/Sun Care |
| Adult | Health & Wellness | Skincare & Hygiene | Feminine Hygiene/Batteries |
| Adult | Health & Wellness | Skincare & Hygiene | Soap/Liquid/Bar |
| Adult | Home & Lifestyle | Bath & Laundry | Licensed Towels/Bath Sets |
| Adult | Home & Lifestyle | Bedding | Luxury/Value Duvets |
| Adult | Home & Lifestyle | Kitchen & Misc | Seasonal/Xmas Kitchenware |
| Adult | Home & Lifestyle | Toys & Games | Licensed/Everyday Toys |
| Woman | Intimates & Swim | Sleep & Lounge | Pyjama Separates (Jersey/Woven) |
| Woman | Intimates & Swim | Sleep & Lounge | Sleepwear (World Cup) |
| Man | Apparel | Tops & Blouses | Formal Shirts (L/S Premium) |
| Man | Apparel | Tops & Blouses | Formal Shirts (S/S Value) |
| Woman | Apparel | Tops & Blouses | Fashion Print/Christmas Tees |
| Man | Apparel | Trousers & Shorts | 3/4 Length Shorts |
| Man | Apparel | Swim & Beachwear | Cargo Plain/Design Swimwear |
| Man | Apparel | Swim & Beachwear | Short Design/Plain Swimwear |
| Man | Apparel | Knit & Jersey Tops | S/S Sweats/Zip Thru |
| Woman | Apparel | Trousers & Shorts | Casual Performancewear |
| Woman | Apparel | Dresses & Skirts | Knit/Ponte Dresses |
| Man | Apparel | Knitwear | Novelty/Licensed Knitwear |
| Man | Apparel | Tops & Blouses | Formal Shirts (Yarn Dye) |
| Woman | Apparel | Tops & Blouses | Fashion Vest/Cami (Lace) |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Licensed Hats/Jewellery |
| Woman | Accessories & Footwear | Footwear | Licensed/LTD Edition Footwear |
| Woman | Accessories & Footwear | Hosiery | Licensed Socks/Slipper Socks |
| Woman | Intimates & Swim | Sleep & Lounge | All Over Print Nightwear |
| Woman | Intimates & Swim | Underwear & Bras | Non-Cotton/Non-Padded Sets |
| Woman | Intimates & Swim | Swim & Beachwear | Licensed Swimwear |
| Man | Accessories & Footwear | Bags & Wallets | Licensed Bags/Wallets |
| Man | Apparel | Licensed/Limited | Licensed Leisure Bottoms |
| Man | Apparel | Tops & Blouses | Licensed T-Shirts |
| Man | Apparel | Licensed/Limited | Licensed Outerwear |
| Man | Accessories & Footwear | Soft & Hard Accessories | Licensed Watches |
| Man | Accessories & Footwear | Hosiery | Licensed Socks/Gift Sets |
| Child | Apparel | Licensed/Limited | Licensed Kids Apparel |
| Child | Accessories & Footwear | Soft & Hard Accessories | Licensed Kids Accessories |
| Child | Accessories & Footwear | Kids Footwear/Hosiery | Licensed Kids Slippers |
| Baby | Apparel | Licensed/Limited | Licensed Babywear |
| Adult | Home & Lifestyle | Licensed/Limited | Licensed Home Decor/Bedding |
| Adult | Home & Lifestyle | Toys & Games | Licensed Toys |
| Adult | Health & Wellness | Licensed/Limited | Licensed H&B Products |
| Adult | Health & Wellness | Consumables | Licensed Confectionery |
| Adult | Home & Lifestyle | Kitchen & Misc | Licensed Paper/Cards |
| Adult | Accessories & Footwear | Bags & Wallets | Licensed Luggage |
| Adult | Accessories & Footwear | Soft & Hard Accessories | Licensed Umbrellas/Sunglasses |
| Woman | Apparel | Licensed/Limited | World Cup Apparel |
| Man | Apparel | Licensed/Limited | World Cup Apparel |
| Child | Apparel | Licensed/Limited | World Cup Kids Apparel |
| Woman | Intimates & Swim | Licensed/Limited | World Cup Intimates/Swim |
| Man | Intimates & Swim | Licensed/Limited | World Cup Underwear |
| Woman | Apparel | Tops & Blouses | Long Sleeve Woven Tops |
| Woman | Apparel | Dresses & Skirts | Formal Woven Dresses |
| Woman | Apparel | Trousers & Shorts | Linen Skirts/Shorts |
| Woman | Apparel | Knitwear | Viscose/Cotton Fashion Knit |
| Man | Apparel | Knit & Jersey Tops | Fashion Polo Shirts (Stripe) |
| Man | Apparel | Tops & Blouses | Long Sleeve Fashion Tees |
| Man | Apparel | Tops & Blouses | S/S Casual Shirts (Design/Print) |
| Man | Apparel | Trousers & Shorts | Cargo Pants/Worker Cargos |
| Man | Apparel | Denimwear | Stretch Skinny/Slim Denim |
| Man | Apparel | Outerwear | Basic Casual Gilet |
| Woman | Health & Wellness | Personal Care | Branded/Own Label Wipes |
| Adult | Health & Wellness | Personal Care | Dental Accessories/Sets |
| Adult | Home & Lifestyle | Bedding | Specialty Bedding Protectors |
| Adult | Home & Lifestyle | Bath & Laundry | Shower Curtains/Mats |
| Adult | Home & Lifestyle | Kitchen & Misc | Travel Accessories |
| Adult | Home & Lifestyle | Kitchen & Misc | All Year Round Paper/Cards |
| Woman | Accessories & Footwear | Footwear | Heeled/Formal Day Sandals |
| Woman | Accessories & Footwear | Footwear | Limited Edition Boots/Heels |
| Woman | Accessories & Footwear | Hosiery | Multipack Hold-ups/Tights |
| Woman | Apparel | Knit & Jersey Tops | Smart Jersey SS Plain/Print |
| Woman | Apparel | Activewear | Sports Tops Fleece/Sweats |
| Man | Apparel | Knit & Jersey Tops | Pique Polos (Basic/Fashion) |
| Man | Apparel | Knitwear | Fine Gauge Plain/Design |
| Man | Apparel | Tops & Blouses | Formal Shirts (Premium/Value) |
| Man | Apparel | Outerwear | Parkas/Wool Coats |
| Man | Accessories & Footwear | Hosiery | Formal/Luxury Socks |
| Woman | Intimates & Swim | Underwear & Bras | Co-ords (Microfibre/Satin/Lace) |
| Woman | Intimates & Swim | Sleep & Lounge | Chemise/Glamour Wraps |
| Woman | Intimates & Swim | Underwear & Bras | Smoothline Boxer/Briefs |
| Woman | Apparel | Trousers & Shorts | Limited Edition Shorts |
| Man | Apparel | Denimwear | Basic Bootcut/Straight Denim |
| Man | Apparel | Activewear | Fashion Leisure Bottoms/Jackets |
| Adult | Health & Wellness | Cosmetics & Fragrance | Value/Branded Lip Care |
| Adult | Home & Lifestyle | Kitchen & Misc | Drinking Glasses/Teatowels |
| Adult | Home & Lifestyle | Decor & Furnishings | Christmas Gifts/Decorations |
| Adult | Home & Lifestyle | Bath & Laundry | Value/Premium Towels |
| Baby | Apparel | Baby Wear (Boy) | Licensed Shirts/Shorts/Swim |
| Baby | Apparel | Baby Wear (Girl) | Licensed Dresses/Sets/Swim |
| Child | Apparel | Trousers & Shorts | Kids Licensed Bottoms |
| Child | Apparel | Outerwear | Kids Licensed Outerwear |
| Child | Apparel | Licensed/Limited | Kids Licensed Swimwear |
| Girl | Apparel | Knit & Jersey Tops | Girls Licensed Tees |
| Boy | Apparel | Knit & Jersey Tops | Boys Licensed Tees |
| Girl | Apparel | Dresses & Skirts | Girls Licensed Dresses |
| Woman | Apparel | Denimwear | Licensed Denim Tops/Dresses |
| Man | Apparel | Tops & Blouses | Licensed Shirts |
| Man | Apparel | Activewear | Licensed Swimwear |
| Woman | Apparel | Trousers & Shorts | Performance Jog Legs |
| Man | Apparel | Knit & Jersey Tops | Long Sleeve Stretch Tees |
| Man | Apparel | Tops & Blouses | Short Sleeve Value Shirts |
| Woman | Apparel | Trousers & Shorts | Casual Chino/Linen Trousers |
| Woman | Apparel | Knit & Jersey Tops | Fashion Tees (Embellished) |
| Woman | Apparel | Outerwear | Lightweight Trench/Mac |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Basic/Fashion Hats |
| Woman | Accessories & Footwear | Soft & Hard Accessories | Sunglasses (Novelty/Round) |
| Woman | Accessories & Footwear | Footwear | Casual/Sports Canvas |
| Woman | Accessories & Footwear | Footwear | Flats (Lace Ups) |
| Woman | Accessories & Footwear | Hosiery | Sheer Tights (Control) |
| Woman | Intimates & Swim | Underwear & Bras | Basic/Stretch Camisoles |
| Woman | Intimates & Swim | Underwear & Bras | Thermal Tops/Bottoms |
| Man | Apparel | Tops & Blouses | Formal Shirts (Slim Fit) |
| Man | Apparel | Outerwear | Basic Casual Jackets |
| Man | Apparel | Denimwear | Cord Jeans/Twill |
| Man | Apparel | Activewear | Fashion Leisure Sweat Tops |
| Man | Accessories & Footwear | Hosiery | Sports Crew/Technical Socks |
| Man | Accessories & Footwear | Bags & Wallets | Backpacks/Duffle Bags |
| Man | Accessories & Footwear | Soft & Hard Accessories | Knitted/Woven Gloves |
| Man | Accessories & Footwear | Footwear | Sports/Leisure Footwear |
| Adult | Health & Wellness | Skincare & Hygiene | Branded/Own Label Hair Removal |
| Adult | Health & Wellness | Skincare & Hygiene | Men's Grooming Skincare |
| Adult | Health & Wellness | Cosmetics & Fragrance | Premium Cosmetics/Sets |
| Adult | Home & Lifestyle | Decor & Furnishings | Rugs/Frames/Wall Art |
| Adult | Home & Lifestyle | Toys & Games | Everyday Christmas Toys |
"""