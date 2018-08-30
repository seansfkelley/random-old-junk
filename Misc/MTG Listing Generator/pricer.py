# usage: pricer.py filename
#
# The input file is assumed to be a list of delimited values (separated by commas) that form tuples of the form
# (card_name, edition, quantity, condition, is_foil) where:
#     card_name is the name of the card; captialization and punctuation optional (including spaces). DO NOT INCLUDE COMMAS.
#     edition is the full name of the edition or one of the shorthands defined in SHORTHANDS
#     quantity is the number of cards that should be in a single listing and is optional (assumed 1 when missing)
#     condition is one of nm, nm-, sp, or hp and is optional (assumed nm when missing)
#     is_foil is the string 'f' or 'foil' (case insensitive) if the card is foil; any other value (or blank) otherwise
# 
# The program copies the price list from magictraders.com at least once a day, or on demand if the user deletes the
# cache file. The program will write out 4 files:
#     CACHE holds the most recent pricing information built from magictraders.com; this is rebuilt at least once a week
#         automatically but can be forcibly rebuild if it is deleted
#     INPUT-listed.csv is the output pricing information, configurable with variables described below
#     INPUT-cheap.csv is the list of cards that were deemed to cheap to list
#     INPUT-rejected.csv is the list of cards that were not found either because they were a typo of a card name, they
#         were not found to be similar to any known cards, they are foils for which no foil price was forund, or not 
#         enough information was supplied. The file is organized in the same order. CORRECTED CARDS WILL NEVER BE LISTED.
#         They are output to this file to be double-checked, and the file is formatted in the same manner as the input 
#         file for ease-of-use.
# where:
#     CACHE represents the name of the cache files chosen by the user in the variable CACHE_FILENAME
#     INPUT represents the input filename, stripped of its extension
#
# Cache files are written into the working directory of the python executable.
#
# Program variables are the all-caps constants below this description. They are defined as follows:
#
# PRICE_THRESHOLD          a price cutoff under which cards are not sold (applied before rounding; after condition modifiers)
# PRICE_BASE_MODIFIER      base factor by which to reduce the price of SCG list price (<1) (applied before rounding)
# PRICE_NM_MINUS_MODIFIER  factor by which to reduce the price of NM- cards, relative to NM (<1) (applied before rounding)
# PRICE_SP_MODIFIER        factor by which to reduce the price of SP cards, relative to NM (<1) (applied before rounding)
# PRICE_HP_MODIFIER        factor by which to reduce the price of HP cards, relative to NM (<1) (applied before rounding)
# WINDOWS                  whether this is being run on a Windows or Unix (inc. OS X) machine
# USE_EBAY_FORMAT          whether to output a .csv that can be read by eBay's Turbo Lister program
# EBAY_CARD_NAME           a function from a Card object to a listing title string
# EBAY_CARD_DESC           a function from a Card object to a listing description string
# EBAY_FORMAT_HEADER       the column header for eBay's Turbo Lister input .csv (change only when necessary)
# EBAY_FORMAT_ENTRY        the format string of a listing in eBay's Turbo Lister input .csv
# PRICE_LIST_URL           the format string for a page of card price listings on SCG
# CACHE_FILENAME           the base name for the cache file

# Program Variables -----------------------------------------------------------
PRICE_THRESHOLD = 0.8

PRICE_BASE_MODIFIER = 0.65

PRICE_NM_MINUS_MODIFIER = 0.9
PRICE_SP_MODIFIER = 0.8
PRICE_HP_MODIFIER = 0.5

# Use Windows- or Unix-style newlines.
WINDOWS = False

# Windows newlines are assumed with this option set, but ONLY FOR THE LISTING, not for corrected output .csv.
USE_EBAY_FORMAT = True

EBAY_CARD_NAME = lambda card: '%s%s %s Magic the Gathering MTG %s' % (('%dx ' % card.quantity if card.quantity > 1 else ''), ('FOIL ' if card.is_foil else '') + card.name.replace(',',''), card.edition, card.condition.upper())
EBAY_CARD_DESC = lambda card: '<P><FONT size=6>You are bidding on %s %s from %s. The card is in %s condition! Shipping is free within the US! Also, check out my other listings!! (This is a stock photo; if you want a scan feel free to ask).</FONT></P>' % (('%dx' % card.quantity if card.quantity > 1 else ('an' if card.name[0].lower() in 'aeiou' else 'a')), card.name.replace(',','') + (' FOIL' if card.is_foil else ''), card.edition, CONDITIONS[card.condition])

EBAY_FORMAT_HEADER = 'Action(CC=Cp1252),SiteID,Format,Title,Condition,SubTitle,Custom Label,Category,Category2,StoreCategory,StoreCategory2,Quantity,LotSize,Currency,StartPrice,BuyItNowPrice,ReservePrice,InsuranceOption,InsuranceFee,DomesticInsuranceOption,DomesticInsuranceFee,PackagingHandlingCosts,InternationalPackagingHandlingCosts,Duration,PrivateAuction,Country,ProductIDType,ProductIDValue,Product:ProductReferenceID,ItemID,Description,HitCounter,PicURL,BoldTitle,Featured,GalleryType,FeaturedFirstDuration,Highlight,Border,HomePageFeatured,Subtitle in search resutls,GiftIcon,GiftServices-1,GiftServices-2,GiftServices-3,SalesTaxPercent,SalesTaxState,ShippingInTax,UseTaxTable,PostalCode,ProxyItem,VATPercent,Location,ImmediatePayRequired,PayPalAccepted,PayPalEmailAddress,PaymentInstructions,PaymateAccepted,ProPayAccepted,MoneyBookersAccepted,StandardPayment,UPC,CCAccepted,AmEx,Discover,VisaMastercard,IntegratedMerchantCreditCard,COD,CODPrePayDelivery,PostalTransfer,MOCashiers,PersonalCheck,MoneyXferAccepted,MoneyXferAcceptedinCheckout,PaymentOther,OtherOnlinePayments,PaymentSeeDescription,Escrow,ShippingType,ShipFromZipCode,ShippingIrregular,ShippingPackage,WeightMajor,WeightMinor,WeightUnit,MeasurementUnit,ShippingDetails/CODCost,PackageLength,PackageWidth,PackageDepth,DomesticRateTable,InternationalRateTable,CharityID,CharityName,DonationPercent,ShippingService-1:Option,ShippingService-1:Cost,ShippingService-1:AdditionalCost,ShippingService-1:Priority,ShippingService-1:FreeShipping,ShippingService-1:ShippingSurcharge,ShippingService-2:Option,ShippingService-2:Cost,ShippingService-2:AdditionalCost,ShippingService-2:Priority,ShippingService-2:ShippingSurcharge,ShippingService-3:Option,ShippingService-3:Cost,ShippingService-3:AdditionalCost,ShippingService-3:Priority,ShippingService-3:ShippingSurcharge,ShippingService-4:Option,ShippingService-4:Cost,ShippingService-4:AdditionalCost,ShippingService-4:Priority,ShippingService-4:ShippingSurcharge,ShippingService-5:Option,ShippingService-5:Cost,ShippingService-5:AdditionalCost,ShippingService-5:Priority,ShippingService-5:ShippingSurcharge,GetItFast,DispatchTimeMax,IntlShippingService-1:Option,IntlShippingService-1:Cost,IntlShippingService-1:AdditionalCost,IntlShippingService-1:Locations,IntlShippingService-1:Priority,IntlShippingService-2:Option,IntlShippingService-2:Cost,IntlShippingService-2:AdditionalCost,IntlShippingService-2:Locations,IntlShippingService-2:Priority,IntlShippingService-3:Option,IntlShippingService-3:Cost,IntlShippingService-3:AdditionalCost,IntlShippingService-3:Locations,IntlShippingService-3:Priority,IntlShippingService-4:Option,IntlShippingService-4:Cost,IntlShippingService-4:AdditionalCost,IntlShippingService-4:Locations,IntlShippingService-4:Priority,IntlShippingService-5:Option,IntlShippingService-5:Cost,IntlShippingService-5:AdditionalCost,IntlShippingService-5:Locations,IntlShippingService-5:Priority,IntlAddnlShiptoLocations,PaisaPayAccepted,PaisaPay EMI payment,BasicUpgradePackBundle,ValuePackBundle,ProPackPlusBundle,BestOfferEnabled,AutoAccept,BestOfferAutoAcceptPrice,AutoDecline,MinimumBestOfferPrice,BestOfferRejectMessage,LocalOnlyChk,LocalListingDistance,BuyerRequirements:ShipToRegCountry,BuyerRequirements:ZeroFeedbackScore,BuyerRequirements:MinFeedbackScore,BuyerRequirements:MaxUnpaidItemsCount,BuyerRequirements:MaxUnpaidItemsPeriod,BuyerRequirements:MaxItemCount,BuyerRequirements:MaxItemMinFeedback,BuyerRequirements:LinkedPayPalAccount,BuyerRequirements:VerifiedUser,BuyerRequirements:VerifiedUserScore,BuyerRequirements:MaxViolationCount,BuyerRequirements:MaxViolationPeriod,SellerDetails:PrimaryPhone,SellerDetails:SecondaryPhone,ExtSellerDetails:Hours1Days,ExtSellerDetails:Hours1AnyTime,ExtSellerDetails:Hours1From,ExtSellerDetails:Hours1To,ExtSellerDetails:Hours2Days,ExtSellerDetails:Hours2AnyTime,ExtSellerDetails:Hours2From,ExtSellerDetails:Hours2To,ExtSellerDetails:TimeZoneID,ListingDesigner:LayoutID,ListingDesigner:ThemeID,ShippingDiscountProfileID,InternationalShippingDiscountProfileID,Apply Profile Domestic,Apply Profile International,PromoteCBT,ShipToLocations,CustomLabel,CashOnPickup,ReturnsAcceptedOption,ReturnsWithinOption,RefundOption,ShippingCostPaidBy,WarrantyOffered,WarrantyType,WarrantyDuration,AdditionalDetails,MarketplaceType,ProjectGoodCategory,ShortDescription,ProducerDescription,RegionOfOrigin,ProducerPhotoURL,Relationship,RelationshipDetails'
EBAY_FORMAT_ENTRY = 'Add,US,Auction,%s,%d,,,19115,,0,0,1,,USD,%.2f,,,,,,0,,,7,0,US,,,,,"%s",,%s,0,0,None,,0,0,0,0,0,,,,,,,,02155,,,,0,1,josh_blackborow@mindspring.com,None Specified,,,,,,,,,,,,,,,,,,,,0,,Flat,,,,,,,English,,,,,,,,,,ShippingMethodStandard,0,,1,1,,,,,,,,,,,,,,,,,,,,,,0,1,USPSFirstClassMailInternational,2,,Worldwide,1,,,,,,,,,,,,,,,,,,,,,,,,,0,,,,,,,,,,,,,,,,,0,,,,,,,,,,,,,,,,,,0||,0||,0,0,,,,,ReturnsAccepted,Days_14,MoneyBack,Buyer,,,,,,,,,,,,'

PRICE_LIST_URL = 'http://sales.starcitygames.com//spoiler/display.php?&s%%5Bcor2%%5D=1000&s%%5Bcor3%%5D=1001&s%%5Bcor4%%5D=1002&s%%5Bcor5%%5D=1003&s%%5Bcor6%%5D=1009&s%%5Brep17%%5D=1062&s%%5Bcor7%%5D=1015&s%%5Bcor8%%5D=1025&s%%5Bcor9%%5D=1037&s%%5Bcor10%%5D=1053&s%%5Bcor11%%5D=5023&s%%5Bcor12%%5D=5061&s%%5Bcor13%%5D=5137&s%%5Bcor14%%5D=5192&s%%5B5211%%5D=5211&s%%5Bear12%%5D=1004&s%%5Bear13%%5D=1005&s%%5Bear14%%5D=1006&s%%5Bear15%%5D=1007&s%%5Bear16%%5D=1008&s%%5Bice20%%5D=1011&s%%5Bice19%%5D=1010&s%%5Bice21%%5D=1012&s%%5Bice22%%5D=5040&s%%5Bice18%%5D=5057&s%%5Bmir23%%5D=1013&s%%5Bmir24%%5D=1014&s%%5Bmir25%%5D=1016&s%%5Btem26%%5D=1017&s%%5Btem27%%5D=1018&s%%5Btem28%%5D=1019&s%%5Bsag29%%5D=1020&s%%5Bsag30%%5D=1021&s%%5Bsag31%%5D=1023&s%%5Bmas32%%5D=1027&s%%5Bmas33%%5D=1029&s%%5Bmas34%%5D=1031&s%%5Binv35%%5D=1033&s%%5Binv36%%5D=1035&s%%5Binv37%%5D=1039&s%%5Body38%%5D=1041&s%%5Body39%%5D=1043&s%%5Body40%%5D=1045&s%%5Bons41%%5D=1047&s%%5Bons42%%5D=1049&s%%5Bons43%%5D=1051&s%%5Bmib44%%5D=1055&s%%5Bmib45%%5D=1057&s%%5Bmib46%%5D=5007&s%%5Bkam47%%5D=5005&s%%5Bkam48%%5D=5018&s%%5Bkam49%%5D=5020&s%%5Brav50%%5D=5026&s%%5Brav51%%5D=5035&s%%5Brav52%%5D=5037&s%%5Btim53%%5D=5042&s%%5Btim54%%5D=5049&s%%5Btim55%%5D=5055&s%%5Blor1%%5D=5064&s%%5Blor2%%5D=5083&s%%5Bsha1%%5D=5094&s%%5Bsha2%%5D=5096&s%%5Bala1%%5D=5106&s%%5Bala2%%5D=5116&s%%5Bala3%%5D=5131&s%%5B5172%%5D=5172&s%%5B5177%%5D=5177&s%%5B5187%%5D=5187&s%%5B5197%%5D=5197&s%%5B5202%%5D=5202&s%%5B5207%%5D=5207&s%%5B5215%%5D=5215&s%%5Bpor56%%5D=1059&s%%5Bpor57%%5D=1060&s%%5Bpor58%%5D=1061&s%%5Bpor59%%5D=1063&s%%5Bpor60%%5D=5014&s%%5Bbx64%%5D=1068&s%%5B5190%%5D=5190&s%%5B5191%%5D=5191&s%%5Bbx63%%5D=1069&s%%5Bbx65%%5D=1070&s%%5B5213%%5D=5213&s%%5B5214%%5D=5214&s%%5Bbx66%%5D=1071&s%%5B5217%%5D=5217&s%%5B5134%%5D=5134&s%%5B5195%%5D=5195&s%%5B205%%5D=5082&s%%5B5176%%5D=5176&s%%5B5115%%5D=5115&s%%5B5209%%5D=5209&s%%5B5189%%5D=5189&s%%5B5196%%5D=5196&s%%5B5108%%5D=5108&s%%5B5171%%5D=5171&s%%5B5219%%5D=5219&s%%5B5194%%5D=5194&s%%5B5174%%5D=5174&s%%5B5175%%5D=5175&s%%5B5201%%5D=5201&s%%5B5186%%5D=5186&foil=%s&for=no&r_all=All&t_all=All&g%%5BG1%%5D=NM/M&sort1=4&sort2=1&numpage=200&display=4&startnum=%d'

CACHE_FILENAME = 'magiccards.bak'

# Begin Program ---------------------------------------------------------------
import sys
import os
import time
import pickle
import urllib2
import re

c_succeeded_ct = c_total_ct = 0
c_cheap_ct = 0

filename_base = os.path.splitext(sys.argv[1])[0]

no_price_foils = []

NEWLINE = '\r\n' if WINDOWS else '\n'

# Accept corrections with edits/character below this threshold. These are autocorrected in the corrected output file;
# those above the threshold are left alone.
# INCORRECTLY SPELLED CARDS WILL NEVER BE LISTED. They are output to a file suitable for input for double-checking.
CORRECTION_THRESHOLD = 0.25

CONDITIONS = {
'nm' : 'Near Mint',
'nm-' : 'Near Mint minus',
'sp' : 'Some Play',
'hp' : 'Heavy Play'
}

# Because SCG puts thimeshifted cards in with the normal Time Spiral cards, TSB -> Time Spiral
SHORTHANDS = {
'10' : 'Tenth Edition',
'10e' : 'Tenth Edition',
'10th' : 'Tenth Edition',
'1999' : 'Starter 1999',
'2000' : 'Starter 2000',
'2010' : 'Magic 2010',
'2011' : 'Magic 2011',
'2012' : 'Magic 2012',
'2ed' : 'Revised Edition',
'3' : 'Revised Edition',
'3ed' : 'Unlimited Edition',
'3rd' : 'Revised Edition',
'4' : 'Fourth Edition',
'4ed' : 'Fourth Edition',
'4th' : 'Fourth Edition',
'5' : 'Fifth Edition',
'5dn' : 'Fifth Dawn',
'5ed' : 'Fifth Edition',
'5th' : 'Fifth Edition',
'6' : 'Classic Sixth Edition',
'6ed' : 'Classic Sixth Edition',
'6th' : 'Classic Sixth Edition',
'7' : 'Seventh Edition',
'7ed' : 'Seventh Edition',
'7th' : 'Seventh Edition',
'8' : 'Eighth Edition',
'8ed' : 'Eighth Edition',
'8th' : 'Eighth Edition',
'9' : 'Ninth Edition',
'9ed' : 'Ninth Edition',
'9th' : 'Ninth Edition',
'a' : 'Limited Edition Alpha',
'aen' : 'Zendikar',
'al' : 'Alliances',
'ala' : 'Shards of Alara',
'all' : 'Alliances',
'alli' : 'Alliances',
'alpha' : 'Limited Edition Alpha',
'an' : 'Arabian Nights',
'anth' : 'Anthologies',
'anti' : 'Antiquities',
'ap' : 'Apocalypse',
'apc' : 'Apocalypse',
'apoc' : 'Apocalypse',
'aq' : 'Antiquities',
'ar' : 'Alara Reborn',
'arb' : 'Alara Reborn',
'arc' : 'Archenemy',
'arch' : 'Archenemy',
'arn' : 'Arabian Nights',
'ath' : 'Anthologies',
'atq' : 'Antiquities',
'b' : 'Limited Edition Beta',
'batt' : 'Battle Royale',
'beat' : 'Beatdown',
'beta' : 'Limited Edition Beta',
'bk' : 'Betrayers of Kamigawa',
'bok' : 'Betrayers of Kamigawa',
'brb' : 'Battle Royale',
'btd' : 'Beatdown',
'cfx' : 'Conflux',
'ch' : 'Chronicles',
'chk' : 'Champions of Kamigawa',
'chr' : 'Chronicles',
'chro' : 'Chronicles',
'ck' : 'Champions of Kamigawa',
'cmd' : 'Commander',
'cold' : 'Coldsnap',
'comm' : 'Commander',
'con' : 'Conflux',
'conf' : 'Conflux',
'csp' : 'Coldsnap',
'dark' : 'The Dark',
'dd' : 'Duel Decks: Divine vs. Demonic',
'dd2' : 'Duel Decks: Jace vs. Chandra',
'ddc' : 'Duel Decks: Divine vs. Demonic',
'ddd' : 'Duel Decks: Garruk vs. Liliana',
'dde' : 'Duel Decks: Phyrexia vs. The Coalition',
'ddf' : 'Duel Decks: Elspeth vs. Tezzeret',
'ddg' : 'Duel Decks: Knights vs. Dragons',
'ddh' : 'Duel Decks: Ajani vs. Nicol Bolas',
'deck' : 'Deckmasters',
'dis' : 'Dissension',
'diss' : 'Dissension',
'dk' : 'The Dark',
'dka' : 'Dark Ascension',
'dkm' : 'Deckmasters',
'drag' : 'From the Vault: Dragons',
'drb' : 'From the Vault: Dragons',
'drk' : 'The Dark',
'ds' : 'Darksteel',
'dst' : 'Darksteel',
'eg' : 'Duel Decks: Elves vs. Goblins',
'eil' : 'From the Vault: Exiled',
'eve' : 'Eventide',
'even' : 'Eventide',
'evg' : 'Duel Decks: Elves vs. Goblins',
'ex' : 'Exodus',
'exo' : 'Exodus',
'exod' : 'Exodus',
'fd' : 'Fifth Dawn',
'fe' : 'Fallen Empires',
'fem' : 'Fallen Empires',
'fs' : 'Future Sight',
'fut' : 'Future Sight',
'gl' : 'Duel Decks: Garruk vs. Liliana',
'gp' : 'Guildpact',
'gpt' : 'Guildpact',
'h09' : 'Premium Deck Series: Slivers',
'hl' : 'Homelands',
'hml' : 'Homelands',
'home' : 'Homelands',
'hop' : 'Planechase',
'ia' : 'Ice Age',
'ice' : 'Ice Age',
'in' : 'Invasion',
'inni' : 'Innistrad',
'ins' : 'Innistrad',
'inv' : 'Invasion',
'inva' : 'Invasion',
'isd' : 'Innistrad',
'jc' : 'Duel Decks: Jace vs. Chandra',
'jud' : 'Judgment',
'judg' : 'Judgment',
'kd' : 'Duel Decks: Knights vs. Dragons',
'le' : 'Legends',
'lea' : 'Limited Edition Alpha',
'leb' : 'Limited Edition Beta',
'leg' : 'Legends',
'lege' : 'Legends',
'legi' : 'Legions',
'lgn' : 'Legions',
'lorw' : 'Lorwyn',
'lrw' : 'Lorwyn',
'm10' : 'Magic 2010',
'm11' : 'Magic 2011',
'm12' : 'Magic 2012',
'mb' : 'Mirrodin Besieged',
'mbs' : 'Mirrodin Besieged',
'mi' : 'Mirage',
'mir' : 'Mirage',
'mira' : 'Mirage',
'mirr' : 'Mirrodin',
'mm' : 'Mercadian Masques',
'mmq' : 'Mercadian Masques',
'mor' : 'Morningtide',
'morn' : 'Morningtide',
'mrd' : 'Mirrodin',
'ne' : 'Nemesis',
'neme' : 'Nemesis',
'nms' : 'Nemesis',
'np' : 'New Phyrexia',
'nph' : 'New Phyrexia',
'od' : 'Odyssey',
'ody' : 'Odyssey',
'odys' : 'Odyssey',
'ons' : 'Onslaught',
'onsl' : 'Onslaught',
'p02' : 'Portal II',
'p2' : 'Portal II',
'p3' : 'Portal: Three Kingdoms',
'pc' : 'Planar Chaos',
'pcy' : 'Prophecy',
'pd2' : 'Premium Deck Series: Fire and Lightning',
'plan' : 'Planeshift',
'plc' : 'Planar Chaos',
'pls' : 'Planeshift',
'por' : 'Portal I',
'port1' : 'Portal I',
'port2' : 'Portal II',
'port3' : 'Portal: Three Kingdoms',
'pr' : 'Prophecy',
'promo' : 'Promotional Cards',
'prop' : 'Prophecy',
'ps' : 'Planeshift',
'pt' : 'Portal I',
'ptk' : 'Portal: Three Kingdoms',
'rav' : 'Ravnica: City of Guilds',
'ravn' : 'Ravnica: City of Guilds',
'reli' : 'From the Vault: Relics',
'rev' : 'Revised Edition',
'revi' : 'Revised Edition',
'roe' : 'Rise of the Eldrazi',
'rv' : 'Revised Edition',
's00' : 'Starter 2000',
's99' : 'Starter 1999',
'sa' : 'Shards of Alara',
'scg' : 'Scourge',
'scou' : 'Scourge',
'shad' : 'Shadowmoor',
'shm' : 'Shadowmoor',
'sk' : 'Saviors of Kamigawa',
'sliv' : 'Premium Slivers',
'sm' : 'Scars of Mirrodin',
'sok' : 'Saviors of Kamigawa',
'som' : 'Scars of Mirrodin',
'st' : 'Stronghold',
'st1' : 'Starter 1999',
'st2' : 'Starter 2000',
'sth' : 'Stronghold',
'stro' : 'Stronghold',
'te' : 'Tempest',
'temp' : 'Tempest',
'tmp' : 'Tempest',
'tor' : 'Torment',
'torm' : 'Torment',
'tsb' : 'Time Spiral',
'tsp' : 'Time Spiral',
'u' : 'Unlimited',
'ud' : 'Urza\'s Destiny',
'uds' : 'Urza\'s Destiny',
'ug' : 'Unglued',
'ugl' : 'Unglued',
'uh' : 'Unhinged',
'ul' : 'Urza\'s Legacy',
'ulg' : 'Urza\'s Legacy',
'unh' : 'Unhinged',
'unli' : 'Unlimited',
'us' : 'Urza\'s Saga',
'usg' : 'Urza\'s Saga',
'uz' : 'Urza\'s Saga',
'v09' : 'From the Vault: Exiled',
'v10' : 'From the Vault: Relics',
'v11' : 'From the Vault: Legends',
'van' : 'Vanguard',
'vi' : 'Visions',
'vis' : 'Visions',
'wl' : 'Weatherlight',
'wth' : 'Weatherlight',
'ww' : 'Worldwake',
'wwk' : 'Worldwake',
'zen' : 'Zendikar'
}

SCG_TO_GATHERER = {
'DD: Ajani vs. Nicol Bolas' : 'Duel Decks: Ajani vs. Nicol Bolas',
'DD: Divine vs. Demonic' : 'Duel Decks: Divine vs. Demonic',
'DD: Elspeth vs. Tezzeret' : 'Duel Decks: Elspeth vs. Tezzeret',
'DD: Elves vs. Goblins' : 'Duel Decks: Elves vs. Goblins',
'DD: Garruk vs. Liliana' : 'Duel Decks: Garruk vs. Liliana',
'DD: Jace vs. Chandra' : 'Duel Decks: Jace vs. Chandra',
'DD: Knights vs. Dragons' : 'Duel Decks: Knights vs. Dragons',
'DD: Phyrexia vs. The Coalition' : 'Duel Decks: Phyrexia vs. The Coalition',
'3rd Edition/Revised' : 'Revised Edition',
'4th Edition' : 'Fourth Edition',
'5th Edition' : 'Fifth Edition',
'6th Edition' : 'Sixth Edition',
'7th Edition' : 'Seventh Edition',
'8th Edition' : 'Eighth Edition',
'9th Edition' : 'Ninth Edition',
'10th Edition' : 'Tenth Edition',
'2010 Core Set' : 'Magic 2010',
'2011 Core Set' : 'Magic 2011',
'2012 Core Set' : 'Magic 2012'
}

def format_card_name(name):
    return re.sub('[\W_]+', '', name.lower())

# prices is abbv_name : {edition : price}
# Returns (prefix_lists, name_map, image_urls, prices, foil_prices)
def build_cache():
    prefix_lists = dict(zip('abcdefghijklmnopqrstuvwxyz', [{} for i in xrange(26)]))
    name_map = {}
    image_urls = {}
    prices = {}
    foil_prices = {}
    
    # Non-foil prices ---------------------------------------------------------
    
    html = urllib2.urlopen(PRICE_LIST_URL % ('nonfoil', 0))
    text = html.read()
    html.close()
    
    l = text.rfind('> [')
    pages = text[l + 3:text.find(']', l)]
    
    print 'Downloading non-foil prices from %s pages.\nOn page... ' % pages
    
    offset = 200
    i = 1
    while 'Your query produced zero results.' not in text:
        print i, 
        sys.stdout.flush()
        i += 1
        
        # Find all cards on the page.
        l = text.find('http://static.starcitygames.com/sales/cardscans')
        while l != -1:
            image_url = text[l:text.find('jpg', l) + 3]
            
            l = text.find('tooltip', l)
            name = text[l + 9:text.find('>', l) - 1]
            
            l = text.find('>', text.find('category.php', l))
            edition = text[l + 1:text.find('<', l)]
            edition = SCG_TO_GATHERER.get(edition, edition)
            
            l = text.find('$', l)
            price = text[l + 1:text.find('<', l)]
            
            abbv_name = format_card_name(name)
            prefix_lists[abbv_name[0]][abbv_name] = None
            name_map[abbv_name] = name
            image_urls[abbv_name] = image_url
            
            if abbv_name not in prices:
                prices[abbv_name] = {}
            
            prices[abbv_name][edition] = float(price)
            
            l = text.find('http://static.starcitygames.com/sales/cardscans', l)
        
        html = urllib2.urlopen(PRICE_LIST_URL % ('nonfoil', offset))
        text = html.read()
        html.close()
                
        offset += 200
    
    print
    
    # Foil prices -------------------------------------------------------------
    
    html = urllib2.urlopen(PRICE_LIST_URL % ('foil', 0))
    text = html.read()
    html.close()
    
    l = text.rfind('> [')
    pages = text[l + 3:text.find(']', l)]
    
    print 'Downloading foil prices from %s pages.\nOn page... ' % pages
    
    offset = 200
    i = 1
    while 'Your query produced zero results.' not in text:
        print i, 
        sys.stdout.flush()
        i += 1
        
        # Find all cards on the page.
        l = text.find('tooltip')
        while l != -1:
            name = text[l + 9:text.find('>', l) - 1]
            
            l = text.find('>', text.find('category.php', l))
            edition = text[l + 1:text.find('(', l) - 1]
            edition = SCG_TO_GATHERER.get(edition, edition)
            
            l = text.find('$', l)
            price = text[l + 1:text.find('<', l)]
            
            abbv_name = format_card_name(name)
            
            if abbv_name not in foil_prices:
                foil_prices[abbv_name] = {}
            
            foil_prices[abbv_name][edition] = float(price)
            
            l = text.find('tooltip', l)
        
        html = urllib2.urlopen(PRICE_LIST_URL % ('foil', offset))
        text = html.read()
        html.close()
                
        offset += 200
    
    print
        
    return (prefix_lists, name_map, image_urls, prices, foil_prices)

def edit_distance(s1, s2):
    # Lehvenshtein distance from Wikipedia.
    m, n = len(s1), len(s2)
    d = [[0] * (n + 1) for i in xrange(m + 1)]
    
    for i in xrange(m + 1):
        d[i][0] = i
    for j in xrange(n + 1):
        d[0][j] = j
    
    for j in xrange(1, n + 1):
        for i in xrange(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j] + 1, # deletion
                              d[i][j - 1] + 1,  # insertion
                              d[i - 1][j - 1] + 1 # substitution
                              )
    return d[m][n]

def get_correction(abbv_name):
    # Simple metric: edits/character in the corrected string.
    return sorted([(candidate, float(edit_distance(candidate, abbv_name)) / len(candidate)) for candidate in prefix_lists[abbv_name[0]]], key = lambda x: x[1])[0]

# Non-fatal exception representing a problem retrieving the information for a card.
def get_list_price(price, card):
    price *= card.quantity * PRICE_BASE_MODIFIER
    
    if card.condition == 'nm-':
        price *= PRICE_NM_MINUS_MODIFIER
    elif card.condition == 'sp':
        price *= PRICE_SP_MODIFIER
    elif card.condition == 'hp':
        price *= PRICE_HP_MODIFIER
    
    if price <= PRICE_THRESHOLD:
        raise PriceError(price)
        
    price = round(price * 4) / 4.0
    
    if price <= 2:
        return .99
    if 10 <= price <= 12:
        return 9.99
    if 25 <= price <= 30:
        return 24.99
    
    return price

# Non-fatal exception representing some type of error finding or pricing a card.
class CardError(Exception):
    pass

# Non-fatal exception representing a card that is not valuable enough to sell. Raised only by get_list_price.
class PriceError(Exception):
    def __init__(self, price):
        self.price = float(price)
    

class Card:
    def __init__(self, card_info_list):
        self.name, self.edition, self.quantity, self.condition, self.is_foil = card_info_list
        self.quantity = int(self.quantity)
    
    def __str__(self):
        return '%dx %s%s (%s) @ %s' % (self.quantity, 'Foil ' if self.is_foil else '', self.name, self.edition, self.condition)
    
    # Returns a string suitable for reading this card back in as input.
    def as_input_string(self):
        return ', '.join(self.as_input_list())
    
    # Returns a list of strings suitable for being output and read back in as input.
    def as_input_list(self):
        return map(str, [self.name.replace(',', ''), self.edition, self.quantity, self.condition]) + (['f'] if self.is_foil else ['r'])
    


if len(sys.argv) == 1:
    print 'usage: %s filename' % sys.argv[0]
    sys.exit(0)

try:
    input_file = open(sys.argv[1], 'r')
except IOError:
    print 'Could not open file %s' % sys.argv[1]
    sys.exit(0)

cache_location = os.path.join(os.getcwd(), CACHE_FILENAME)
# Rebuild the cache if it doesn't exist or is older than a week.
if not os.path.exists(cache_location) or time.time() - os.stat(cache_location).st_mtime > 604800:
    print '--- Downloading and building cache...'
    
    prefix_lists, name_map, image_urls, prices, foil_prices = build_cache()
    
    print '--- Writing updated cache...'
    
    f = open(cache_location, 'w')
    pickle.dump((prefix_lists, name_map, image_urls, prices, foil_prices), f)
    f.close()
    
else:
    print '--- Found recent cache. Loading...'
    
    f = open(cache_location, 'r')
    prefix_lists, name_map, image_urls, prices, foil_prices = pickle.load(f)
    f.close()

print '--- Loading card list...' 
print

# Input cards are [full_name, edition, quantity, condition, is_foil] lists.
input_cards_unchecked = input_file.readlines()
input_file.close()
input_cards_unchecked = [c.strip().strip(',').split(',') for c in input_cards_unchecked]
not_enough_information_cards = map(lambda x: x[0].strip(), filter(lambda x: len(x) == 1, input_cards_unchecked)) # ''.strip() == [''], so len() == 1
input_cards_unchecked = filter(lambda x: len(x) >= 2, input_cards_unchecked)
input_cards_unchecked = [[c[0], SHORTHANDS.get(c[1].strip().lower(), c[1].strip()), c[2].strip() if len(c) > 2 else '1', c[3].lower().strip() if len(c) > 3 else 'nm', len(c) > 4 and c[4].strip().lower() in ['f', 'foil']] for c in input_cards_unchecked]

# Corrected cards in the same format as input cards, but with the corrected name.
corrected_cards = []
rejected_cards = []

c_total_ct = len(input_cards_unchecked)

if c_total_ct == 0:
    print '---- Listing Results ----'
    print 'No cards were suitable for listing. Check your input file.'
    sys.exit(0)

print '--- Verifying card validity...'
print '(Errors in file "%s")' % (filename_base + '-rejected.csv')
print

error_line = 1

# Convert tuples into Card objects.
input_cards = []
for card in input_cards_unchecked:
    try:
        abbv_name = format_card_name(card[0])
        if abbv_name not in name_map:
            corrected_name, norm_distance = get_correction(abbv_name)
            corrected_name = name_map[corrected_name].replace(',', '')
            if norm_distance <= CORRECTION_THRESHOLD:
                corrected_cards.append([corrected_name] + card[1:])
                raise CardError('Correcting %s to %s.' % (card[0], corrected_name))
            else:
                rejected_cards.append(card)
                raise CardError('Could not locate card %s.' % card[0])
        else:
            try:
                input_cards.append(Card([name_map[abbv_name]] + card[1:]))
            except ValueError:
                rejected_cards.append(card)
                raise CardError('Invalid quantity "%s" supplied for %s.' % (card[2], card[0]))
    
    except CardError as e:
        print ('%3d ' % error_line) + str(e)
        error_line += 1

print 
print '--- Checking card prices...'
print '(Errors in file "%s")' % (filename_base + '-rejected.csv')
print '(Cheap cards in file "%s")' % (filename_base + '-cheap.csv')
print '(Listings in file "%s")' % (filename_base + '-listed.csv')
print

listing = open(filename_base + '-listed.csv', 'w')
cheap = open(filename_base + '-cheap.csv', 'w')

if USE_EBAY_FORMAT:
    listing.write(EBAY_FORMAT_HEADER + '\r\n')

for c in input_cards:
    try:
        abbv_name = format_card_name(c.name)
        
        try:
            price = get_list_price((prices if not c.is_foil else foil_prices)[abbv_name][c.edition], c)
        except KeyError:
            rejected_cards.append(c.as_input_list())
            raise CardError(('No %s found in %s. Correct edition?' % (c.name, c.edition)) + (' Maybe no foil price?' if c.is_foil else ''))
        except PriceError as p:
            c_cheap_ct += 1
            cheap.write(c.as_input_string() + NEWLINE)
            raise CardError('%s%s too cheap at $%.2f.' % (('%dx ' % c.quantity) if c.quantity > 1 else '', c.name, p.price))
    
        # image_url = get_image_url(c)
    
        if USE_EBAY_FORMAT:
            listing.write(EBAY_FORMAT_ENTRY % (EBAY_CARD_NAME(c), 1000 if c.condition == 'nm' else 3000, price, EBAY_CARD_DESC(c), image_urls[abbv_name]) + '\r\n')
        else:
            listing.write(str(c) + NEWLINE)
        
        c_succeeded_ct += 1

    except CardError as e:
        print ('%3d ' % error_line) + str(e)
        error_line += 1
    
    except KeyError:
        print 'No image found for %s.' % c.name
        error_line += 1

listing.close()
cheap.close()

print 
print '--- Listing Results ---'
print '%d/%d cards listed (%.0f%%); %d/%d cards too cheap to list (%.0f%%).' % (c_succeeded_ct, c_total_ct, 100.0 * c_succeeded_ct / c_total_ct, c_cheap_ct, c_total_ct, 100.0 * c_cheap_ct / c_total_ct)

not_enough_information_cards = filter(lambda x: len(x) > 0, not_enough_information_cards)

if corrected_cards or rejected_cards or not_enough_information_cards or no_price_foils:
    corr, uncorr = len(corrected_cards), len(rejected_cards)
    print '%d/%d cards with errors (%.0f%%). %d had names automatically corrected.' % (corr + uncorr, c_total_ct, 100.0 * (corr + uncorr) / c_total_ct, corr)
    if len(not_enough_information_cards):
        print '%d cards were underspecified and no pricing was attempted.' % len(not_enough_information_cards)
    
    f = open(filename_base + '-rejected.csv', 'w')
    for c in corrected_cards:
        f.write(', '.join(c[:-1] + ['f' if c[-1] else '']) + NEWLINE)
        
    f.write(NEWLINE)
    
    for c in rejected_cards:
        f.write(', '.join(c[:-1] + ['f' if c[-1] else '']) + NEWLINE)
    
    f.write(NEWLINE)

    for c in not_enough_information_cards:
        f.write(c + NEWLINE)
    
    f.close()