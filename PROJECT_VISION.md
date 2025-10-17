# 🎯 Project Vision & Strategic Goals

## Project Name
**Retail Customer Segmentation using Machine Learning POC**

---

## 🎯 Current Branch Goal

**Branch Focus**: **Expand Synthetic Data Generation**

**Objective**: Enhance the `RetailDataGenerator` to create more realistic, comprehensive, and varied customer purchase datasets that better represent real-world retail scenarios.

**Target Enhancements**:
- 📊 More sophisticated customer behavior patterns
- 🏬 Extended product hierarchies (Department → Class )
- 🎨 Additional product attributes (Size, Color, Brand, Style)
- 📈 Realistic statistical distributions for all features
- 🎯 Configurable data scenarios to symulate customer behavior
        Example: Female shoppers favoring Apparel and Beauty products during holiday seasons,
                : Female shopper who buys childres clothing during back-to-school periods
                : Female teenager who buys trendy clothes and accessories
        - Configuration , must be based at either department level or department-class level , if it as a department level then the classes are randomly selected within that department , multiple classes can be assigned , with the number configurable
- Add the customer profile to the generated data but it must not be used in clustering
- Department and Department Class hierarchies will be fully implemented in this branch to enable richer customer   profiles and segmentation analysis. 
- Ensure seamless integration with existing clustering and visualization modules
- The data must include a department level summary for each customer , total spend and units purchased per department.
- the must be two sets of data generated 
   1. Basic data with core features only for clustering
   2. Enriched data with full features and department summaries level for analysis
   3. Enriched data with full features including department and class level breakdowns for in-depth analysis 

IMPORTANT use dos terminal for development

### Product Hierarchy Reference

| # | Department Name | Department Class Name |
|---|-----------------|----------------------|
| 1 | Accessories | Accessories:Bags |
| 2 | Accessories | Accessories:BELTS |
| 3 | Accessories | Accessories:CONFECTIONERY |
| 4 | Accessories | Accessories:DUMMY |
| 5 | Accessories | Accessories:GENTS ACCESSORIES |
| 6 | Accessories | Accessories:Gloves |
| 7 | Accessories | Accessories:Hair |
| 8 | Accessories | Accessories:HAIR ACCESSORIES |
| 9 | Accessories | Accessories:Hats |
| 10 | Accessories | Accessories:HW Scarves |
| 11 | Accessories | Accessories:JEWELLERY AND GIFTS |
| 12 | Accessories | Accessories:Kids |
| 13 | Accessories | Accessories:KIDS ACCESSORIES |
| 14 | Accessories | Accessories:KIDS BAGS |
| 15 | Accessories | Accessories:Ladies Belts |
| 16 | Accessories | Accessories:LADIES GLOVES |
| 17 | Accessories | Accessories:LADIES HATS |
| 18 | Accessories | Accessories:LADIES HW SCARVES |
| 19 | Accessories | Accessories:Ladies Jewellery |
| 20 | Accessories | Accessories:Ladies Scarves |
| 21 | Accessories | Accessories:Ladies Sunglasses |
| 22 | Accessories | Accessories:Ladies Umbrellas |
| 23 | Accessories | Accessories:Luggage |
| 24 | Accessories | Accessories:LW SCARVES |
| 25 | Accessories | Accessories:MAKE-UP BAGS |
| 26 | Accessories | Accessories:Mens Accessories |
| 27 | Accessories | Accessories:Purses |
| 28 | Accessories | Accessories:READING GLASSES |
| 29 | Accessories | Accessories:Sports Events D1 |
| 30 | Accessories | Accessories:SUNGLASSES |
| 31 | Accessories | Accessories:UMBRELLAS |
| 32 | Accessories | Accessories:UNASSIGNED D1 |
| 33 | Accessories | Accessories:Unknown |
| 34 | Accessories | Accessories:WATCHES |
| 35 | Accessories | Accessories:WORLD CUP |
| 36 | Bag Levy | Bag Levy:Paper Bags |
| 37 | Bag Levy | Bag Levy:UNASSIGNED D30 |
| 38 | Concessions | Concessions:Barbers |
| 39 | Concessions | Concessions:Beauty Salon |
| 40 | Concessions | Concessions:DUMMY |
| 41 | Concessions | Concessions:Entertainment |
| 42 | Concessions | Concessions:Pop-up Shop |
| 43 | Concessions | Concessions:UNASSIGNED D28 |
| 44 | Dummy | Dummy:Dummy |
| 45 | Dummy Dept for TBC order | Dummy Dept for TBC order:Dummy Clas for TBC order |
| 46 | Gift Cards | Gift Cards:Gift Cards |
| 47 | Gift Cards | Gift Cards:UNASSIGNED D32 |
| 48 | Goods Not For Resale | Goods Not For Resale:Bags D31 |
| 49 | Goods Not For Resale | Goods Not For Resale:Baskets |
| 50 | Goods Not For Resale | Goods Not For Resale:Consumables |
| 51 | Goods Not For Resale | Goods Not For Resale:Epic Merch |
| 52 | Goods Not For Resale | Goods Not For Resale:FSDU |
| 53 | Goods Not For Resale | Goods Not For Resale:Mannequins |
| 54 | Goods Not For Resale | Goods Not For Resale:Till Rolls |
| 55 | Goods Not For Resale | Goods Not For Resale:UNASSIGNED D31 |
| 56 | Goods Not For Resale | Goods Not For Resale:Unknown |
| 57 | Health & Beauty | Health & Beauty:Accessories |
| 58 | Health & Beauty | Health & Beauty:Beauty Essentials |
| 59 | Health & Beauty | Health & Beauty:Branded Cosmetics |
| 60 | Health & Beauty | Health & Beauty:Confectionery |
| 61 | Health & Beauty | Health & Beauty:Cosmetics |
| 62 | Health & Beauty | Health & Beauty:DUMMY |
| 63 | Health & Beauty | Health & Beauty:EDB ACCESSORIES |
| 64 | Health & Beauty | Health & Beauty:EDB COSMETICS |
| 65 | Health & Beauty | Health & Beauty:EDB TOILETRIES |
| 66 | Health & Beauty | Health & Beauty:Electricals |
| 67 | Health & Beauty | Health & Beauty:Events |
| 68 | Health & Beauty | Health & Beauty:False Nails and Lashes |
| 69 | Health & Beauty | Health & Beauty:Fragrance |
| 70 | Health & Beauty | Health & Beauty:GIFTS |
| 71 | Health & Beauty | Health & Beauty:Hair |
| 72 | Health & Beauty | Health & Beauty:Health & Wellbeing |
| 73 | Health & Beauty | Health & Beauty:Hygiene |
| 74 | Health & Beauty | Health & Beauty:Kids Health and Beauty |
| 75 | Health & Beauty | Health & Beauty:Love Beauty |
| 76 | Health & Beauty | Health & Beauty:MAKE UP |
| 77 | Health & Beauty | Health & Beauty:Mens Grooming |
| 78 | Health & Beauty | Health & Beauty:SKIN CARE |
| 79 | Health & Beauty | Health & Beauty:Skincare |
| 80 | Health & Beauty | Health & Beauty:SPECIAL OFFERS |
| 81 | Health & Beauty | Health & Beauty:Tanning |
| 82 | Health & Beauty | Health & Beauty:TISSUES |
| 83 | Health & Beauty | Health & Beauty:Toiletries |
| 84 | Health & Beauty | Health & Beauty:UNASSIGNED D23 |
| 85 | Health & Beauty | Health & Beauty:Unknown |
| 86 | Health & Beauty | Health & Beauty:XMAS GIFTS |
| 87 | Home | Home:Baby Bedding |
| 88 | Home | Home:Baby Blankets |
| 89 | Home | Home:Bathroom |
| 90 | Home | Home:Candles |
| 91 | Home | Home:Curtains |
| 92 | Home | Home:CUSHIONS |
| 93 | Home | Home:DUMMY |
| 94 | Home | Home:DUVET COVERS |
| 95 | Home | Home:Duvets |
| 96 | Home | Home:Filled Product |
| 97 | Home | Home:Home Accessories |
| 98 | Home | Home:Kids Home |
| 99 | Home | Home:KITCHEN |
| 100 | Home | Home:Licensed Home |
| 101 | Home | Home:Lifestyle |
| 102 | Home | Home:Lights |
| 103 | Home | Home:Living Cushions |
| 104 | Home | Home:Living Throws |
| 105 | Home | Home:LUGGAGE |
| 106 | Home | Home:Paper |
| 107 | Home | Home:Paper Products |
| 108 | Home | Home:Pillows |
| 109 | Home | Home:Plain Bedding |
| 110 | Home | Home:Promotions |
| 111 | Home | Home:Seasonal |
| 112 | Home | Home:Speciality Bedding |
| 113 | Home | Home:Sports Events D11 |
| 114 | Home | Home:Storage |
| 115 | Home | Home:Throws |
| 116 | Home | Home:Towels |
| 117 | Home | Home:Toys |
| 118 | Home | Home:Transfers |
| 119 | Home | Home:UNASSIGNED D11 |
| 120 | Home | Home:Unknown |
| 121 | In-Store Charity | In-Store Charity:UNASSIGNED D33 |
| 122 | Kids Accessories | Kids Accessories:Baby Accessories |
| 123 | Kids Accessories | Kids Accessories:Baby Footwear |
| 124 | Kids Accessories | Kids Accessories:Baby Socks |
| 125 | Kids Accessories | Kids Accessories:Boys Accessories |
| 126 | Kids Accessories | Kids Accessories:Boys Footwear |
| 127 | Kids Accessories | Kids Accessories:Boys Nightwear |
| 128 | Kids Accessories | Kids Accessories:Boys Socks |
| 129 | Kids Accessories | Kids Accessories:Boys Underwear |
| 130 | Kids Accessories | Kids Accessories:Girls Accessories |
| 131 | Kids Accessories | Kids Accessories:Girls Footwear |
| 132 | Kids Accessories | Kids Accessories:Girls Hosiery |
| 133 | Kids Accessories | Kids Accessories:Girls Nightwear |
| 134 | Kids Accessories | Kids Accessories:Girls Underwear |
| 135 | Kids Accessories | Kids Accessories:Kids Accessories |
| 136 | Kids Accessories | Kids Accessories:Kids Accessories Sports Events |
| 137 | Kids Accessories | Kids Accessories:Kids Footwear |
| 138 | Kids Accessories | Kids Accessories:Kids Hosiery |
| 139 | Kids Accessories | Kids Accessories:Kids Nightwear |
| 140 | Kids Accessories | Kids Accessories:Kids Underwear |
| 141 | Kids Accessories | Kids Accessories:UNASSIGNED D15 |
| 142 | Kids Accessories | Kids Accessories:Unknown |
| 143 | Kids Clothing | Kids Clothing:2-7 Boyswear |
| 144 | Kids Clothing | Kids Clothing:2-7 Girlswear |
| 145 | Kids Clothing | Kids Clothing:7+ Boyswear |
| 146 | Kids Clothing | Kids Clothing:7+ Girlswear |
| 147 | Kids Clothing | Kids Clothing:Baby Basics |
| 148 | Kids Clothing | Kids Clothing:Baby Boy |
| 149 | Kids Clothing | Kids Clothing:Baby Girl |
| 150 | Kids Clothing | Kids Clothing:Babywear |
| 151 | Kids Clothing | Kids Clothing:CHILDRENS HOSIERY |
| 152 | Kids Clothing | Kids Clothing:DUMMY |
| 153 | Kids Clothing | Kids Clothing:Kids Hosiery |
| 154 | Kids Clothing | Kids Clothing:Kids Nightwear |
| 155 | Kids Clothing | Kids Clothing:Kids Sports Events |
| 156 | Kids Clothing | Kids Clothing:Kids Underwear |
| 157 | Kids Clothing | Kids Clothing:MISC |
| 158 | Kids Clothing | Kids Clothing:Newborn Boy |
| 159 | Kids Clothing | Kids Clothing:Newborn Girl |
| 160 | Kids Clothing | Kids Clothing:OUTERWEAR |
| 161 | Kids Clothing | Kids Clothing:SCHOOLWEAR |
| 162 | Kids Clothing | Kids Clothing:UNASSIGNED D5 |
| 163 | Kids Clothing | Kids Clothing:UNDERWEAR |
| 164 | Kids Clothing | Kids Clothing:Unknown |
| 165 | Ladies Clothing | Ladies Clothing:Basic T Shirts |
| 166 | Ladies Clothing | Ladies Clothing:Cardigans |
| 167 | Ladies Clothing | Ladies Clothing:Casual Bottoms |
| 168 | Ladies Clothing | Ladies Clothing:CASUAL JERSEY BOTTOMS |
| 169 | Ladies Clothing | Ladies Clothing:CASUAL OUTERWEAR |
| 170 | Ladies Clothing | Ladies Clothing:Casual Shorts |
| 171 | Ladies Clothing | Ladies Clothing:Co-ordinates |
| 172 | Ladies Clothing | Ladies Clothing:Coats |
| 173 | Ladies Clothing | Ladies Clothing:Contemporary Collections |
| 174 | Ladies Clothing | Ladies Clothing:Dresses & Skirts |
| 175 | Ladies Clothing | Ladies Clothing:DUMMY |
| 176 | Ladies Clothing | Ladies Clothing:Edit |
| 177 | Ladies Clothing | Ladies Clothing:Essential Jersey |
| 178 | Ladies Clothing | Ladies Clothing:Fashion Jersey |
| 179 | Ladies Clothing | Ladies Clothing:Formal Jackets |
| 180 | Ladies Clothing | Ladies Clothing:FORMAL SKIRTS |
| 181 | Ladies Clothing | Ladies Clothing:Formal Trousers |
| 182 | Ladies Clothing | Ladies Clothing:IRISH |
| 183 | Ladies Clothing | Ladies Clothing:Jersey Tops Table |
| 184 | Ladies Clothing | Ladies Clothing:Jumpers |
| 185 | Ladies Clothing | Ladies Clothing:Ladies Denim |
| 186 | Ladies Clothing | Ladies Clothing:Ladies Limited Edition |
| 187 | Ladies Clothing | Ladies Clothing:Ladies Performancewear |
| 188 | Ladies Clothing | Ladies Clothing:Ladies Shorts |
| 189 | Ladies Clothing | Ladies Clothing:Licensed Womens |
| 190 | Ladies Clothing | Ladies Clothing:LS Cotton Tops |
| 191 | Ladies Clothing | Ladies Clothing:Maternity |
| 192 | Ladies Clothing | Ladies Clothing:Outerwear/Coats |
| 193 | Ladies Clothing | Ladies Clothing:Preloved |
| 194 | Ladies Clothing | Ladies Clothing:Shorts |
| 195 | Ladies Clothing | Ladies Clothing:Skirts |
| 196 | Ladies Clothing | Ladies Clothing:Smart Jersey Tops |
| 197 | Ladies Clothing | Ladies Clothing:Soft Skirts |
| 198 | Ladies Clothing | Ladies Clothing:SPARE |
| 199 | Ladies Clothing | Ladies Clothing:Sports Tops |
| 200 | Ladies Clothing | Ladies Clothing:SPORTSWEAR |
| 201 | Ladies Clothing | Ladies Clothing:Swim & Beach |
| 202 | Ladies Clothing | Ladies Clothing:Tops |
| 203 | Ladies Clothing | Ladies Clothing:Trousers and Formal Jkts |
| 204 | Ladies Clothing | Ladies Clothing:UNASSIGNED D8 |
| 205 | Ladies Clothing | Ladies Clothing:Unknown |
| 206 | Ladies Clothing | Ladies Clothing:Woven Tops & Bottoms |
| 207 | Ladies Clothing | Ladies Clothing:Youth |
| 208 | Ladies Footwear | Ladies Footwear:Babies |
| 209 | Ladies Footwear | Ladies Footwear:Beach |
| 210 | Ladies Footwear | Ladies Footwear:Casual Footwear |
| 211 | Ladies Footwear | Ladies Footwear:DUMMY |
| 212 | Ladies Footwear | Ladies Footwear:Flats |
| 213 | Ladies Footwear | Ladies Footwear:Footwear Accessories |
| 214 | Ladies Footwear | Ladies Footwear:Heels |
| 215 | Ladies Footwear | Ladies Footwear:KIDS SHOES |
| 216 | Ladies Footwear | Ladies Footwear:Kids Slippers |
| 217 | Ladies Footwear | Ladies Footwear:Ladies Boots |
| 218 | Ladies Footwear | Ladies Footwear:LADIES CANVAS |
| 219 | Ladies Footwear | Ladies Footwear:Ladies Leisure |
| 220 | Ladies Footwear | Ladies Footwear:LADIES SANDALS |
| 221 | Ladies Footwear | Ladies Footwear:Ladies Slippers |
| 222 | Ladies Footwear | Ladies Footwear:LADIES SPORTS & LEISURE |
| 223 | Ladies Footwear | Ladies Footwear:Ladies Wide Fit |
| 224 | Ladies Footwear | Ladies Footwear:MENS SLIPPERS |
| 225 | Ladies Footwear | Ladies Footwear:Older Boys |
| 226 | Ladies Footwear | Ladies Footwear:Older Girls |
| 227 | Ladies Footwear | Ladies Footwear:Sandals |
| 228 | Ladies Footwear | Ladies Footwear:Sports Events D7 |
| 229 | Ladies Footwear | Ladies Footwear:UNASSIGNED D7 |
| 230 | Ladies Footwear | Ladies Footwear:Unknown |
| 231 | Ladies Footwear | Ladies Footwear:WIDE FIT |
| 232 | Ladies Footwear | Ladies Footwear:Younger Boys |
| 233 | Ladies Footwear | Ladies Footwear:Younger Girls |
| 234 | Ladies Hosiery | Ladies Hosiery:Broadfolds |
| 235 | Ladies Hosiery | Ladies Hosiery:Control and Support |
| 236 | Ladies Hosiery | Ladies Hosiery:DESIGN AND FASHION HOSIERY |
| 237 | Ladies Hosiery | Ladies Hosiery:DUMMY |
| 238 | Ladies Hosiery | Ladies Hosiery:Fashion Hosiery |
| 239 | Ladies Hosiery | Ladies Hosiery:Fashion Socks |
| 240 | Ladies Hosiery | Ladies Hosiery:KNEEHIGHS AND FOOTIES |
| 241 | Ladies Hosiery | Ladies Hosiery:Ladies Socks |
| 242 | Ladies Hosiery | Ladies Hosiery:Licensed Product |
| 243 | Ladies Hosiery | Ladies Hosiery:MULTIPACKS |
| 244 | Ladies Hosiery | Ladies Hosiery:Opaques |
| 245 | Ladies Hosiery | Ladies Hosiery:OTHERS |
| 246 | Ladies Hosiery | Ladies Hosiery:Patterned Socks |
| 247 | Ladies Hosiery | Ladies Hosiery:Plain Socks |
| 248 | Ladies Hosiery | Ladies Hosiery:Sheer Tights |
| 249 | Ladies Hosiery | Ladies Hosiery:Shoe Liners |
| 250 | Ladies Hosiery | Ladies Hosiery:Slipper Socks |
| 251 | Ladies Hosiery | Ladies Hosiery:Sports Events D2 |
| 252 | Ladies Hosiery | Ladies Hosiery:Sports Socks |
| 253 | Ladies Hosiery | Ladies Hosiery:UNASSIGNED D2 |
| 254 | Ladies Hosiery | Ladies Hosiery:Unknown |
| 255 | Mens Accessories | Mens Accessories:Bags/Wallets |
| 256 | Mens Accessories | Mens Accessories:BELTS |
| 257 | Mens Accessories | Mens Accessories:BOXERS |
| 258 | Mens Accessories | Mens Accessories:BRIEFS |
| 259 | Mens Accessories | Mens Accessories:Entertainment |
| 260 | Mens Accessories | Mens Accessories:GIFTS |
| 261 | Mens Accessories | Mens Accessories:GOWNS |
| 262 | Mens Accessories | Mens Accessories:Mens Gifts |
| 263 | Mens Accessories | Mens Accessories:Mens Jewellery |
| 264 | Mens Accessories | Mens Accessories:Mens Non-Seasonal Access |
| 265 | Mens Accessories | Mens Accessories:Mens Seasonal Accessories |
| 266 | Mens Accessories | Mens Accessories:Mens Sunglasses |
| 267 | Mens Accessories | Mens Accessories:Mens Umbrellas |
| 268 | Mens Accessories | Mens Accessories:Mens Underwear |
| 269 | Mens Accessories | Mens Accessories:PYJAMAS |
| 270 | Mens Accessories | Mens Accessories:Robes |
| 271 | Mens Accessories | Mens Accessories:SHOES |
| 272 | Mens Accessories | Mens Accessories:Slippers |
| 273 | Mens Accessories | Mens Accessories:Socks |
| 274 | Mens Accessories | Mens Accessories:Sports Events D16 |
| 275 | Mens Accessories | Mens Accessories:SUNGLASSES |
| 276 | Mens Accessories | Mens Accessories:UMBRELLAS |
| 277 | Mens Accessories | Mens Accessories:UNASSIGNED D16 |
| 278 | Mens Accessories | Mens Accessories:Unknown |
| 279 | Mens Accessories | Mens Accessories:Vests |
| 280 | Mens Accessories | Mens Accessories:VESTS/THERMALS |
| 281 | Mens Accessories | Mens Accessories:WORLD CUP |
| 282 | Mens Clothing | Mens Clothing:Basic Leisurewear |
| 283 | Mens Clothing | Mens Clothing:BASIC T-SHIRTS |
| 284 | Mens Clothing | Mens Clothing:BOXERS |
| 285 | Mens Clothing | Mens Clothing:Casual Shirts |
| 286 | Mens Clothing | Mens Clothing:CASUAL TROUSERS |
| 287 | Mens Clothing | Mens Clothing:DENIM |
| 288 | Mens Clothing | Mens Clothing:DUMMY |
| 289 | Mens Clothing | Mens Clothing:FASHION LEISURE |
| 290 | Mens Clothing | Mens Clothing:FASHION LEISUREWEAR |
| 291 | Mens Clothing | Mens Clothing:FASHION T-SHIRTS |
| 292 | Mens Clothing | Mens Clothing:FORMAL JACKETS & TROUSERS |
| 293 | Mens Clothing | Mens Clothing:FORMAL SHIRTS |
| 294 | Mens Clothing | Mens Clothing:Formal Shirts & Ties |
| 295 | Mens Clothing | Mens Clothing:JACKETS |
| 296 | Mens Clothing | Mens Clothing:Knitwear |
| 297 | Mens Clothing | Mens Clothing:L/S T-Shirts |
| 298 | Mens Clothing | Mens Clothing:Licensed Local Sports |
| 299 | Mens Clothing | Mens Clothing:Licensed T-Shirts |
| 300 | Mens Clothing | Mens Clothing:LONG-SLEEVE T-SHIRTS |
| 301 | Mens Clothing | Mens Clothing:Mens Casual Trousers |
| 302 | Mens Clothing | Mens Clothing:Mens Denim |
| 303 | Mens Clothing | Mens Clothing:Mens Formalwear |
| 304 | Mens Clothing | Mens Clothing:Mens Leisurewear |
| 305 | Mens Clothing | Mens Clothing:Mens Limited Edition |
| 306 | Mens Clothing | Mens Clothing:Mens Performancewear |
| 307 | Mens Clothing | Mens Clothing:Mens Shorts |
| 308 | Mens Clothing | Mens Clothing:Mens Swimwear |
| 309 | Mens Clothing | Mens Clothing:Outerwear |
| 310 | Mens Clothing | Mens Clothing:Preloved |
| 311 | Mens Clothing | Mens Clothing:SHORTS |
| 312 | Mens Clothing | Mens Clothing:Ties |
| 313 | Mens Clothing | Mens Clothing:UNASSIGNED D6 |
| 314 | Mens Clothing | Mens Clothing:Unknown |
| 315 | Mens Clothing | Mens Clothing:WORLD CUP |
| 316 | Primarket | Primarket:DUMMY |
| 317 | Primarket | Primarket:Entertainment |
| 318 | Primarket | Primarket:Events |
| 319 | Primarket | Primarket:Experiences |
| 320 | Primarket | Primarket:Food |
| 321 | Primarket | Primarket:Gifts |
| 322 | Primarket | Primarket:Inflatables |
| 323 | Primarket | Primarket:Paper |
| 324 | Primarket | Primarket:Pet |
| 325 | Primarket | Primarket:Stationery |
| 326 | Primarket | Primarket:Technology |
| 327 | Primarket | Primarket:Toys |
| 328 | Primarket | Primarket:Travel |
| 329 | Primarket | Primarket:UNASSIGNED D25 |
| 330 | Primarket | Primarket:Unknown |
| 331 | Sports Shop | Sports Shop:DUMMY |
| 332 | Sports Shop | Sports Shop:Kids |
| 333 | Sports Shop | Sports Shop:Ladies |
| 334 | Sports Shop | Sports Shop:LADIES BRANDED |
| 335 | Sports Shop | Sports Shop:LADIES PERFORMANCE |
| 336 | Sports Shop | Sports Shop:Mens |
| 337 | Sports Shop | Sports Shop:MENS BRANDED |
| 338 | Sports Shop | Sports Shop:MENS PERFORMANCE |
| 339 | Sports Shop | Sports Shop:Socks |
| 340 | Sports Shop | Sports Shop:UNASSIGNED |
| 341 | Sports Shop | Sports Shop:Unknown |
| 342 | Uwear & Nwear | Uwear & Nwear:Beachwear |
| 343 | Uwear & Nwear | Uwear & Nwear:BRA ACCESSORIES |
| 344 | Uwear & Nwear | Uwear & Nwear:Bras |
| 345 | Uwear & Nwear | Uwear & Nwear:Camisoles |
| 346 | Uwear & Nwear | Uwear & Nwear:Co-ordinates D4 |
| 347 | Uwear & Nwear | Uwear & Nwear:CO-ORDS |
| 348 | Uwear & Nwear | Uwear & Nwear:Comfort Briefs |
| 349 | Uwear & Nwear | Uwear & Nwear:DUMMY |
| 350 | Uwear & Nwear | Uwear & Nwear:Folded Pyjamas |
| 351 | Uwear & Nwear | Uwear & Nwear:GLAMOUR |
| 352 | Uwear & Nwear | Uwear & Nwear:Glamour Nightwear |
| 353 | Uwear & Nwear | Uwear & Nwear:HANGING PYJAMAS |
| 354 | Uwear & Nwear | Uwear & Nwear:Ladies Swimwear |
| 355 | Uwear & Nwear | Uwear & Nwear:Licensed Nightwear |
| 356 | Uwear & Nwear | Uwear & Nwear:LOUNGEWEAR |
| 357 | Uwear & Nwear | Uwear & Nwear:Maternity |
| 358 | Uwear & Nwear | Uwear & Nwear:Nightshirts |
| 359 | Uwear & Nwear | Uwear & Nwear:Onesies & Twosies |
| 360 | Uwear & Nwear | Uwear & Nwear:Packed Briefs |
| 361 | Uwear & Nwear | Uwear & Nwear:PJ Separates |
| 362 | Uwear & Nwear | Uwear & Nwear:ROBES |
| 363 | Uwear & Nwear | Uwear & Nwear:SEPARATES |
| 364 | Uwear & Nwear | Uwear & Nwear:Sets |
| 365 | Uwear & Nwear | Uwear & Nwear:Shapewear |
| 366 | Uwear & Nwear | Uwear & Nwear:SHAPEWEAR SOLUTIONS-SHAPEWEAR |
| 367 | Uwear & Nwear | Uwear & Nwear:SLEEPSUITS |
| 368 | Uwear & Nwear | Uwear & Nwear:SMOOTHLINE |
| 369 | Uwear & Nwear | Uwear & Nwear:SPECIALIST BRIEFS |
| 370 | Uwear & Nwear | Uwear & Nwear:Sports Events D4 |
| 371 | Uwear & Nwear | Uwear & Nwear:SWIMWEAR |
| 372 | Uwear & Nwear | Uwear & Nwear:Table Briefs |
| 373 | Uwear & Nwear | Uwear & Nwear:THERMAL |
| 374 | Uwear & Nwear | Uwear & Nwear:UK DISCONTINUED |
| 375 | Uwear & Nwear | Uwear & Nwear:UNASSIGNED D4 |
| 376 | Uwear & Nwear | Uwear & Nwear:Unknown |
| 377 | Uwear & Nwear | Uwear & Nwear:WORLD CUP |
| 378 | Xmas Shop | Xmas Shop:All Year Around |
| 379 | Xmas Shop | Xmas Shop:Books |
| 380 | Xmas Shop | Xmas Shop:Candles/Holders |
| 381 | Xmas Shop | Xmas Shop:CARDS |
| 382 | Xmas Shop | Xmas Shop:CHRISTMAS GIFTS |
| 383 | Xmas Shop | Xmas Shop:CRACKERS |
| 384 | Xmas Shop | Xmas Shop:DUMMY |
| 385 | Xmas Shop | Xmas Shop:Halloween |
| 386 | Xmas Shop | Xmas Shop:Lights |
| 387 | Xmas Shop | Xmas Shop:Room Theme |
| 388 | Xmas Shop | Xmas Shop:Soft Toys |
| 389 | Xmas Shop | Xmas Shop:Toys |
| 390 | Xmas Shop | Xmas Shop:TREE DECORATIONS |
| 391 | Xmas Shop | Xmas Shop:Trees/Garlands |
| 392 | Xmas Shop | Xmas Shop:UNASSIGNED |
| 393 | Xmas Shop | Xmas Shop:Unknown |
| 394 | Xmas Shop | Xmas Shop:Wrapping/Bags |



---

## 🌟 Primary Goal

Build an **AI-powered customer segmentation platform** that enables retail businesses to:
1. Automatically discover meaningful customer segments using advanced ML techniques
2. Generate actionable insights and strategies for each segment
3. Enable AI agents to conduct personalized customer interactions based on segment profiles
4. Export structured cluster profiles for LLM analysis and business intelligence

---

## 🚀 Long-Term Vision

Create a **production-ready, extensible framework** that serves as the foundation for:

### Phase 1: Core Segmentation Engine (✅ Current)
- Multiple clustering algorithms (Fuzzy C-Means, Neural Networks, GMM)
- Synthetic data generation for testing and demos
- Comprehensive cluster profiling and export (JSON/YAML)
- Hierarchical product preference analysis (Department → Class → Subclass)
- Additional product enrichment  ( Size , Color)

### Phase 2: AI Agent Integration (🔄 In Progress)
- LLM-ready cluster profiles for automated analysis
- AI-generated segment names, personas, and strategies
- Automated marketing campaign recommendations
- Customer journey mapping and prediction

### Phase 3: Production Deployment (🔮 Future)
- Real-time customer segmentation pipeline
- Integration with CRM systems (Salesforce, HubSpot)
- API for external systems to query customer segments
- Automated A/B testing framework
- Continuous model retraining and monitoring

### Phase 4: Advanced Analytics (🔮 Future)
- Predictive customer lifetime value (CLV)
- Churn prediction and prevention
- Next-best-action recommendations
- Dynamic segment migration tracking
- Multi-channel attribution modeling

---

## 🎨 Design Philosophy

### 1. **Flexibility First**
- Support multiple clustering algorithms with consistent interfaces
- Configurable features through YAML config files
- Pluggable architecture for new clustering methods

### 2. **AI-Native Design**
- Structured exports designed for LLM consumption
- Comprehensive metadata for AI context understanding
- Human-readable (YAML) + machine-readable (JSON) formats

### 3. **Business-Focused**
- Actionable insights over pure technical metrics
- Clear segment descriptions and marketing strategies
- ROI-driven feature development

### 4. **Production-Ready Code**
- Modular, testable, maintainable architecture
- Comprehensive documentation and examples
- Configuration-driven behavior (no hardcoded values)

---

## 🧩 Core Components

### 1. Data Layer
- **RetailDataGenerator**: Synthetic data with realistic patterns
- **Future**: Connectors for real data sources (CSV, SQL, APIs)
- **Future**: Data validation and quality checks

### 2. Clustering Engine
- **FuzzyCustomerSegmentation**: Soft clustering with membership degrees
- **NeuralCustomerSegmentation**: Deep learning with autoencoders
- **GMMCustomerSegmentation**: Probabilistic clustering with uncertainty
- **Future**: Hierarchical clustering, DBSCAN, spectral clustering

### 3. Analytics & Export
- **ClusterEnrichment**: Descriptive names and interaction strategies
- **Profile Export**: JSON/YAML generation for LLM integration
- **Future**: Interactive dashboards and visualizations

### 4. AI Integration
- **Current**: Structured profiles ready for LLM analysis
- **Future**: Direct API integration with OpenAI, Anthropic, etc.
- **Future**: Automated persona generation and campaign creation

---

## 🎯 Key Use Cases

### 1. Marketing Segmentation
**Goal**: Identify customer segments for targeted marketing campaigns

**Workflow**:
1. Run clustering on customer purchase history
2. Export cluster profiles to JSON
3. Feed to LLM for segment naming and persona generation
4. Generate marketing strategies per segment
5. Deploy personalized campaigns

### 2. Product Recommendations
**Goal**: Understand product preferences by customer segment

**Workflow**:
1. Analyze hierarchical preferences (Department → Class → Size)
2. Identify cross-sell opportunities within segments
3. Generate personalized product recommendations
4. Optimize inventory based on segment trends

### 3. Customer Retention
**Goal**: Identify at-risk customers and prevent churn

**Workflow**:
1. Segment by recency and engagement metrics
2. Detect "declining engagement" clusters
3. Generate retention strategies per segment
4. Deploy automated win-back campaigns

### 4. AI Agent Interactions
**Goal**: Enable AI chatbots to provide personalized experiences

**Workflow**:
1. Customer interacts with AI agent
2. Agent retrieves customer's segment profile
3. Agent tailors tone, offers, and recommendations
4. Agent follows segment-specific interaction strategy

---

## 📊 Success Metrics

### Technical Excellence
- ✅ 3+ clustering algorithms implemented
- ✅ Comprehensive profile export (JSON/YAML)
- 🎯 80%+ test coverage
- 🎯 < 5 seconds clustering time for 10k customers
- 🎯 API response time < 100ms

### Business Impact
- 🎯 20%+ improvement in campaign conversion rates
- 🎯 15%+ increase in customer lifetime value
- 🎯 50%+ reduction in manual segmentation time
- 🎯 10%+ reduction in customer churn

### AI Integration
- ✅ LLM-ready exports with comprehensive metadata
- 🎯 Automated persona generation with 90%+ accuracy
- 🎯 AI-generated strategies adopted by 80%+ of marketing team
- 🎯 < 30 seconds for full LLM analysis pipeline

---

## 🔧 Technology Strategy

### Current Stack
- **Language**: Python 3.8+
- **ML**: scikit-learn, scikit-fuzzy, PyTorch
- **Data**: pandas, numpy
- **Config**: YAML
- **Export**: JSON, YAML

### Future Additions
- **API**: FastAPI for REST endpoints
- **Database**: PostgreSQL for customer data
- **Cache**: Redis for real-time segment lookup
- **Queue**: Celery for async clustering jobs
- **Deploy**: Docker, Kubernetes
- **Monitor**: Prometheus, Grafana
- **LLM**: OpenAI API, Anthropic Claude, local LLMs

---

## 🛣️ Development Roadmap

### ✅ Completed (Q4 2024 - Q1 2025)
- [x] Fuzzy C-Means clustering implementation
- [x] Neural network clustering with autoencoders
- [x] GMM clustering with probabilistic assignments
- [x] Synthetic data generator with hierarchical features
- [x] Cluster profile export (JSON/YAML)
- [x] Comprehensive documentation

### 🔄 In Progress (Q2 2025)
- [ ] LLM integration examples (OpenAI, Claude)
- [ ] Automated persona generation
- [ ] Interactive visualization dashboard
- [ ] Profile comparison tools

### 🎯 Planned (Q3 2025)
- [ ] Real data connectors (CSV, SQL)
- [ ] REST API for segment queries
- [ ] Real-time clustering pipeline
- [ ] A/B testing framework

### 🔮 Future (Q4 2025+)
- [ ] CRM integrations (Salesforce, HubSpot)
- [ ] Predictive analytics (CLV, churn)
- [ ] Multi-channel attribution
- [ ] Automated campaign orchestration

---

## 🎓 Guiding Principles for AI Coding

### When Adding Features:
1. **Always maintain backwards compatibility** with existing exports
2. **Follow the existing pattern**: Each clustering method is a class with `fit_predict()` and `export_cluster_profile()`
3. **Update all three methods** when adding shared functionality
4. **Configuration over code**: Add new parameters to `config.yml`, not hardcoded
5. **Document comprehensively**: Update README.md and create specific docs
6. **Test thoroughly**: Run all clustering methods after changes

### Code Style:
- **Docstrings**: Every class and method needs comprehensive docstrings
- **Type hints**: Use type annotations for all parameters and returns
- **Error handling**: Graceful degradation with informative error messages
- **Logging**: Use print statements for user feedback, not silent failures
- **Modularity**: Keep classes focused on single responsibility

### Architecture Decisions:
- **Consistent interfaces**: All clustering classes follow the same API
- **Separation of concerns**: Data generation, clustering, enrichment, export are separate modules
- **Config-driven**: Behavior controlled by YAML, not code changes
- **Export-first**: Always think about how LLMs will consume the data

---

## 💡 Innovation Opportunities

### 1. Hybrid Clustering
Combine multiple algorithms for ensemble segmentation:
- Vote on cluster assignments across methods
- Weighted confidence scoring
- Meta-clustering on clustering results

### 2. Explainable AI
Add interpretability features:
- SHAP values for feature importance
- Decision tree approximations of clusters
- Natural language explanations of why customer is in segment

### 3. Active Learning
Let marketers refine segments:
- Label examples as good/bad segment fits
- Retrain models with feedback
- Continuous improvement loop

### 4. Time-Series Segmentation
Track customer evolution:
- Segment migration over time
- Lifecycle stage transitions
- Predict next segment move

---

## 📝 Notes for AI Agents

### When I Ask to Add Features:
- Check if it fits the **long-term vision** (production-ready, LLM-integrated)
- Maintain **consistency** across all three clustering methods
- Update **documentation** alongside code
- Think about **scalability** and **real-world usage**

### When Debugging:
- Always validate against **current config.yml** structure
- Check that exports remain **LLM-compatible**
- Ensure **all three methods** still work after changes

### When Refactoring:
- Keep the **public API stable** (methods, return values)
- Improve **internal organization** without breaking examples
- Add **deprecation warnings** before removing features

---

## 🤝 Contributing Philosophy

This is a **POC evolving toward production**. Contributions should:
- Advance toward the long-term vision
- Maintain code quality and documentation standards
- Include examples demonstrating new features
- Consider real-world retail business needs

---

**Last Updated**: October 17, 2025  
**Version**: 0.1.0  
**Status**: Active Development - AI Agent Integration Phase
