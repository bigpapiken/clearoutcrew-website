"""Copy for the service and borough pages. Built by tools/build_pages.py.

Rules for this file:
- Only claims the business already makes on its homepage, or facts checked against
  NYC Department of Sanitation pages (nyc.gov/site/dsny, read 2026-10-25).
- No prices, timelines, licenses, insurance, donation/recycling or same-day claims
  until Jack confirms them (see qa/QUESTIONS-FOR-JACK.md).
- Plain voice to match the homepage: short sentences, contractions, no em dashes.
"""

DSNY = {
    'large': 'https://www.nyc.gov/site/dsny/collection/get-rid-of/large-items.page',
    'furniture': 'https://www.nyc.gov/site/dsny/collection/get-rid-of/furniture-mattresses.page',
    'appliances': 'https://www.nyc.gov/site/dsny/collection/get-rid-of/appliances.page',
    'construction': 'https://www.nyc.gov/site/dsny/collection/get-rid-of/construction-debris.page',
    'electronics': 'https://www.nyc.gov/site/dsny/collection/get-rid-of/electronics.page',
}
WIKI = {'Brooklyn': 'https://en.wikipedia.org/wiki/Brooklyn', 'Queens': 'https://en.wikipedia.org/wiki/Queens',
        'Manhattan': 'https://en.wikipedia.org/wiki/Manhattan', 'the Bronx': 'https://en.wikipedia.org/wiki/The_Bronx',
        'Staten Island': 'https://en.wikipedia.org/wiki/Staten_Island'}
ALL_BOROS = [{"@type": "AdministrativeArea", "name": f"{b}, NY", "sameAs": w} for b, w in WIKI.items()]

SERVICES = [  # slug, label
    ('furniture-appliance-removal', 'Furniture &amp; appliance removal'),
    ('apartment-cleanouts', 'Apartment &amp; house cleanouts'),
    ('estate-cleanouts', 'Estate cleanouts'),
    ('storage-unit-cleanouts', 'Storage unit cleanouts'),
    ('commercial-junk-removal', 'Commercial junk removal'),
    ('construction-debris-removal', 'Construction debris removal'),
    ('property-management-cleanouts', 'Property &amp; real estate cleanouts'),
]
BOROS = [('brooklyn-junk-removal', 'Brooklyn'), ('queens-junk-removal', 'Queens'), ('manhattan-junk-removal', 'Manhattan'),
         ('bronx-junk-removal', 'The Bronx'), ('staten-island-junk-removal', 'Staten Island')]
NAV_404 = [(s, l.replace('&amp;', '&')) for s, l in SERVICES] + [(s, f'Junk removal in {b.replace("The Bronx", "the Bronx")}') for s, b in BOROS]


# ---------- small HTML helpers (homepage components) ----------
def head(hid, title, lede):
    return f'<div class="head"><h2 id="{hid}">{title}</h2><p class="lede">{lede}</p></div>'

def band(sid, label_id, inner, dark=False, style=''):
    cls = 'band dark' if dark else 'band'
    st = f' style="{style}"' if style else ''
    return f'\n  <section class="{cls}" id="{sid}" aria-labelledby="{label_id}"{st}>\n    <div class="wrap">\n      {inner}\n    </div>\n  </section>\n'

def svc_list(items):
    li = []
    for it in items:
        name, desc = it[0], it[1]
        href = it[2] if len(it) > 2 else None
        n = f'<a href="{href}">{name}</a>' if href else name
        li.append(f'<li><b>{n}</b><p>{desc}</p></li>')
    return '<ul class="svc">' + ''.join(li) + '</ul>'

def svc_groups(*groups):
    out = []
    for g in groups:
        title, sub, items = g[0], g[1], g[2]
        gid = f' id="{g[3]}"' if len(g) > 3 else ''
        out.append(f'<div class="svc-group"{gid}><h3>{title} <span>{sub}</span></h3>{svc_list(items)}</div>')
    return '<div class="svc-groups">' + ''.join(out) + '</div>'

def caps(items):
    li = []
    for it in items:
        name, desc = it[0], it[1]
        href = it[2] if len(it) > 2 else None
        n = f'<a href="{href}">{name}</a>' if href else name
        li.append(f'<li><b>{n}</b><span>{desc}</span></li>')
    return '<ul class="caps">' + ''.join(li) + '</ul>'

def steps(items):
    return '<ol class="steps">' + ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in items) + '</ol>'

def links(exclude):
    return '<ul class="links">' + ''.join(f'<li><a href="/{s}/">{l}</a></li>' for s, l in SERVICES if s != exclude) + '</ul>'

def boro_list(exclude=None):
    return f'<ul class="boros{" four" if exclude else ""}">' + ''.join(f'<li><a href="/{s}/">{b}</a></li>' for s, b in BOROS if s != exclude) + '</ul>'

def chips(names):
    return '<ul class="who">' + ''.join(f'<li>{n}</li>' for n in names) + '</ul>'

def source(*keys, note='Rules from the NYC Department of Sanitation (DSNY), checked October 2026.'):
    names = {'large': 'large items', 'furniture': 'furniture and mattresses', 'appliances': 'appliances',
             'construction': 'construction debris', 'electronics': 'electronics'}
    ls = ', '.join(f'<a href="{DSNY[k]}" rel="noopener" target="_blank">{names[k]}</a>' for k in keys)
    return f'<p class="src">{note} DSNY pages: {ls}.</p>'

def hero_pair():
    return ('<div class="hero-photos">'
            '<figure class="ph before" style="margin:0" tabindex="0" data-side="before"><img src="/img/apt-before-1200.webp" srcset="/img/apt-before-640.webp 640w, /img/apt-before-800.webp 800w, /img/apt-before-1200.webp 1200w" sizes="(max-width:860px) 86vw, 44vw" alt="Apartment room before a Clear Out Crew cleanout, stacked with moving boxes, a shopping cart and furniture" width="1200" height="953" fetchpriority="high"><span class="tag tag-before">Before</span></figure>'
            '<figure class="ph after" style="margin:0" tabindex="0" data-side="after"><img src="/img/apt-after-640.webp" alt="The same apartment after the cleanout, empty with clean parquet floors" width="640" height="472"><span class="tag tag-after">After</span></figure>'
            '</div>')

def hero_storage():
    return ('<figure class="shot tall" style="margin:0;max-width:440px"><img src="/img/storage-1200.webp" srcset="/img/storage-640.webp 640w, /img/storage-800.webp 800w, /img/storage-1200.webp 1200w" sizes="(max-width:860px) 92vw, 440px" alt="Storage unit filled with chairs, boxes, bags and a filing cabinet, ready to be cleared out" width="1200" height="1588" fetchpriority="high" style="object-position:50% 60%"></figure>')

def related(exclude, boro_exclude=None, title='More ways we help', lede='Other jobs we handle across the five boroughs.'):
    return band('related', 'related-title',
                f'<div class="split"><div><h2 id="related-title">{title}</h2><p class="lede" style="margin-top:20px">{lede}</p></div>{links(exclude)}</div>'
                f'<div style="margin-top:clamp(48px,6vw,72px)"><h2 style="font-size:clamp(2rem,4vw,3rem);margin-bottom:24px">Where we work</h2>{boro_list(boro_exclude)}'
                f'<p class="areas-note">We also take jobs in surrounding areas outside the city. Send your ZIP code with your quote request.</p></div>')

PHOTO_STEPS = [
    ('Send photos or call', 'Upload a few pictures of what needs to go, or call and describe the job. Tell us where it is and when works for you.'),
    ('Get a free estimate', "We'll get back to you with a price. No obligation, so you can decide when you're ready."),
    ('We haul it away', 'Our crew shows up, does the heavy lifting and loads the truck. You get your space back.'),
]

PAGES = []

# =====================================================================
# SERVICE PAGES
# =====================================================================
PAGES.append(dict(
    slug='furniture-appliance-removal', crumb='Furniture & appliance removal',
    title='Furniture &amp; Appliance Removal NYC | The Clear Out Crew',
    desc="Couch, mattress, fridge and washer removal across NYC's five boroughs. We do the lifting and haul it away. Send photos for a free estimate.",
    service_name='Furniture and appliance removal', service_type='Furniture removal', area_served=ALL_BOROS,
    h1='Furniture &amp; appliance <span class="y">removal</span>',
    lede="Couches, mattresses, dressers, fridges, washers and anything else that won't fit in a trash bag. Our crew does the heavy lifting, loads the truck and takes it away.",
    proof=['Free estimates', 'One piece or a full load', 'All five boroughs'],
    hero_right=caps([
        ('Couches &amp; sectionals', 'Sofas, sleepers, recliners and sectionals, including the ones that barely fit through the door.'),
        ('Mattresses &amp; box springs', "We carry them out, so there's no bagging them up for the curb."),
        ('Fridges &amp; washers', 'Big appliances out of kitchens, basements and laundry rooms.'),
        ('Dressers, desks &amp; bed frames', 'Heavy wood furniture, metal frames and everything in between.'),
    ]),
    sections=[
        band('take', 'take-title', head('take-title', 'What we take', "If it's furniture or a household appliance, we can probably haul it. Not sure about something? Send a photo and ask.") + svc_groups(
            ('Furniture', 'Every room in the house', [
                ('Couches, sofas &amp; sectionals', 'Including sleeper sofas and recliners.'),
                ('Mattresses &amp; box springs', 'Any size, from a crib mattress to a king.'),
                ('Bed frames, dressers &amp; wardrobes', 'Wood and metal, assembled or in pieces.'),
                ('Tables, chairs &amp; desks', 'Dining sets, office chairs, home office desks.'),
                ('Bookcases, shelving &amp; TV stands', 'Plus the smaller clutter around them.'),
            ]),
            ('Appliances', 'Kitchen, laundry and more', [
                ('Refrigerators &amp; freezers', 'Upright fridges, chest freezers and mini fridges.'),
                ('Washers &amp; dryers', 'Out of the apartment, basement or laundry room.'),
                ('Stoves &amp; other large appliances', 'Tell us what you have when you send photos.'),
                ('Not sure about an item?', 'Paint, chemicals and other hazardous waste need special handling. Ask before your job.'),
            ]),
        )),
        band('curb', 'curb-title',
             '<div class="split"><h2 id="curb-title">Why not just leave it at the curb?</h2><div class="prose">'
             '<p>NYC Sanitation does pick up large items for free. The catch is the rules:</p>'
             '<ul><li>You can set out up to 6 large items per collection day, and bulk pickup appointments are no longer offered.</li>'
             '<li>Mattresses and box springs have to be sealed in plastic bags. Skipping that can mean a fine of up to $300.</li>'
             "<li>Fridges, freezers and air conditioners need their Freon removed by DSNY before they're collected. Newer units with R600a or R32 refrigerant aren't collected by DSNY at all.</li>"
             '<li>Metal and rigid plastic go out with recycling. Wood furniture goes out on your trash-only day.</li>'
             '<li>You still have to get everything down the stairs and out to the curb yourself.</li></ul>'
             "<p>If that works for you, great. If it doesn't, send us photos and we'll take it from inside your home.</p>"
             + source('large', 'furniture', 'appliances') + '</div></div>', dark=True),
        band('how', 'how-title', head('how-title', 'How it works', 'Most furniture jobs start with a couple of photos.') + steps([
            ('Send photos', 'Snap the pieces that need to go and send them with your ZIP code. Mention stairs, elevators or tight hallways.'),
            ('Get a free estimate', "We'll get back to you with a price. No obligation."),
            ('We carry it out', 'Our crew lifts it, carries it out and loads the truck. Nothing gets left on the curb.'),
        ])),
        related('furniture-appliance-removal'),
    ],
    faq=[
        ('Will you take just one item?', 'Yes. We take jobs from a single couch to a full apartment. Send a photo of the piece and we\'ll quote it.'),
        ('Can you get a couch out of a walk-up?', 'Carrying furniture down the stairs is part of the job. Tell us the floor and whether there\'s an elevator so the estimate covers it.'),
        ('Do I need to bag my mattress?', 'Not for us. Bagging is a DSNY rule for mattresses set out at the curb. If we\'re hauling it, just tell us it\'s on the list.'),
        ('Do you take refrigerators and air conditioners?', 'We take fridges and other large appliances. Mention air conditioners and anything else with refrigerant in your request so we can confirm before the job.'),
        ('Do you take TVs and computers?', 'Electronics like TVs, computers and monitors can\'t legally go out with NYC trash or recycling. List them in your quote request and we\'ll tell you how we can handle them.'),
        ('How much does furniture removal cost?', 'It depends on how many pieces there are, how big they are and how hard they are to get out. Send photos for a free estimate before anything is scheduled.'),
    ],
))

PAGES.append(dict(
    slug='apartment-cleanouts', crumb='Apartment & house cleanouts',
    title='Apartment &amp; House Cleanouts NYC | The Clear Out Crew',
    desc='Full or partial apartment and house cleanouts in all five boroughs: move-outs, rentals, walk-ups, basements and yards. Send photos for a free estimate.',
    service_name='Apartment and house cleanouts', service_type='Apartment cleanout', area_served=ALL_BOROS,
    h1='Apartment &amp; house <span class="y">cleanouts</span>',
    lede='Moving out, clearing a rental or finally dealing with the basement? We clear out whole apartments and houses, or just the rooms you pick, across all five boroughs.',
    proof=['Full or partial', 'Walk-ups &amp; elevator buildings', 'Free estimates'],
    hero_right=hero_pair(),
    sections=[
        band('covers', 'covers-title', head('covers-title', 'What a cleanout covers', "You decide what stays. We take the rest, from one packed closet to every room in the house.") + svc_groups(
            ('Apartments', 'Studios to family-size units', [
                ('Move-out cleanouts', 'Everything that isn\'t coming with you to the new place.'),
                ('Rental unit cleanouts', 'What tenants leave behind, cleared for the next lease.', '/property-management-cleanouts/'),
                ('Partial cleanouts', 'One room, one closet or everything but the bed.'),
                ('Walk-up apartments', 'Stairs are part of the job. Tell us the floor.'),
            ]),
            ('Houses', 'Rooms, basements, yards', [
                ('Whole-house cleanouts', 'Every room, top to bottom.'),
                ('Basements &amp; attics', 'Years of boxes, old furniture and things nobody remembers buying.'),
                ('Yards &amp; outdoor areas', 'Bags, bins, old cabinets and debris piled along the house.'),
                ('Family &amp; estate homes', 'Clearing a loved one\'s house after the family has taken what it wants.', '/estate-cleanouts/'),
            ]),
        )),
        band('planning', 'planning-title',
             '<div class="split"><h2 id="planning-title">Planning a cleanout in an NYC building</h2><div class="prose">'
             '<p>A little prep with your building keeps cleanout day simple.</p>'
             '<h3>Ask about the elevator</h3><p>Many buildings make you reserve the service elevator and only allow move-outs during set hours. Ask your super or management office early.</p>'
             '<h3>Check what vendors need</h3><p>Some co-ops and condos ask for paperwork, like a certificate of insurance, before a crew can work in the building. Find out what yours requires and put it in your quote request.</p>'
             '<h3>Walk-up? Tell us the floor</h3><p>Stairs change how long a job takes, so they belong in the estimate.</p>'
             '<h3>Pull out what you\'re keeping</h3><p>Set aside documents, valuables and anything you\'re not sure about before we arrive. Anything that goes on the truck is gone.</p>'
             '</div></div>', dark=True),
        band('how', 'how-title', head('how-title', 'How it works', 'Getting a price takes a few minutes. Most people just send photos.') + steps(PHOTO_STEPS)),
        related('apartment-cleanouts'),
    ],
    faq=[
        ('Can you clear out just part of an apartment?', 'Yes. Partial cleanouts are fine. Point out what goes and what stays, and we\'ll leave the rest alone.'),
        ('Do you clean out houses too?', 'Yes. We clear out houses, basements, attics and yards, not just apartments.'),
        ('Do you work with landlords after a tenant moves out?', 'Yes. We clear rental turnovers and vacant units for <a href="/property-management-cleanouts/">property managers and landlords</a>.'),
        ('How long does an apartment cleanout take?', 'It depends on how much is there, the floor and how easy the building is to work in. Ask when you get your estimate.'),
        ('How much does an apartment cleanout cost?', 'It depends on the amount, the type of items and access. Send photos of each room for a free estimate.'),
    ],
))

PAGES.append(dict(
    slug='estate-cleanouts', crumb='Estate cleanouts',
    title='Estate Cleanouts in NYC | The Clear Out Crew',
    desc='Estate cleanouts for families, estate representatives and real estate pros in all five boroughs. Houses and apartments emptied. Free estimates.',
    service_name='Estate cleanouts', service_type='Estate cleanout', area_served=ALL_BOROS,
    h1='Estate <span class="y">cleanouts</span>',
    lede="Clearing out a parent's apartment or a family house is a lot. Once your family has taken what it wants to keep, we handle the heavy part and empty the property.",
    proof=['Families &amp; executors', 'Houses &amp; apartments', 'Free estimates'],
    hero_right=caps([
        ('Family homes', 'Houses with years of furniture, basements and attics to clear.'),
        ('Apartments &amp; co-ops', 'Including walk-ups and buildings with elevator rules.'),
        ('Before a sale or closing', 'Empty the property so it can be listed, sold or renovated.', '/property-management-cleanouts/#real-estate'),
        ('For estate representatives', 'Executors and real estate professionals managing the property.'),
    ]),
    sections=[
        band('how', 'how-title', head('how-title', 'How an estate cleanout works', 'Your family sets the pace. We come in once you\'re ready.') + steps([
            ('Go through it first', 'Most families walk the home and set aside what they\'re keeping before calling us. Take the time you need.'),
            ('Send photos or call', "Show us what's left, room by room. We'll get back to you with a free estimate."),
            ('We empty the property', 'Our crew clears the rooms and loads the truck, so the property is ready for what comes next.'),
        ])),
        band('before', 'before-title',
             '<div class="split"><h2 id="before-title">Before the cleanout</h2><div class="prose">'
             '<p>A few things are worth sorting out before anything leaves the house.</p>'
             '<h3>Find the paperwork</h3><p>Look for wills, deeds, tax records, bank and insurance statements. Check drawers, closets, books and coat pockets. Papers turn up in odd places.</p>'
             '<h3>Set aside keepsakes</h3><p>Photos, letters, jewelry and anything with family value should be pulled out first. Anything that goes on our truck is gone.</p>'
             '<h3>Confirm who signs off</h3><p>If the estate is going through probate, make sure the executor or administrator is OK with clearing the property.</p>'
             '<h3>Check with the building</h3><p>Co-ops and condos often have elevator reservations and vendor rules. Ask the management office what they need.</p>'
             '</div></div>', dark=True),
        related('estate-cleanouts'),
    ],
    faq=[
        ('Can an executor or real estate agent book the cleanout?', 'Yes. We work with families, estate representatives and real estate professionals. Whoever is handling the property can request the estimate.'),
        ("We haven't decided what to keep yet. Should we wait?", 'Yes. Sort first. Set aside documents, photos and anything you might want, then call us for the rest.'),
        ('Can you clear a house before it goes on the market?', 'Yes. We empty properties before listing, closing or renovation.'),
        ('There\'s a storage unit too. Can you clear that?', 'Yes. We do <a href="/storage-unit-cleanouts/">storage unit cleanouts</a> as well. Mention it in your request.'),
        ('How is an estate cleanout priced?', 'By how much there is, what kind of items they are and how easy the property is to work in. Send photos for a free, no-obligation estimate.'),
    ],
))

PAGES.append(dict(
    slug='storage-unit-cleanouts', crumb='Storage unit cleanouts',
    title='Storage Unit Cleanouts NYC | The Clear Out Crew',
    desc="Stop paying for a storage unit full of things you don't need. We clear out storage units across NYC. Send one photo for a free estimate.",
    service_name='Storage unit cleanouts', service_type='Storage unit cleanout', area_served=ALL_BOROS,
    h1='Storage unit <span class="y">cleanouts</span>',
    lede="Paying every month for a unit full of things you don't use? Send us a photo of the unit. We'll clear out whatever you don't want to keep.",
    proof=['Start with one photo', 'Full or partial', 'Free estimates'],
    cta='Quote my storage unit',
    hero_right=hero_storage(),
    sections=[
        band('clear', 'clear-title', head('clear-title', 'What we clear out', 'Self-storage, building storage or a business unit. Keep what you want and we take the rest.') + svc_groups(
            ('Storage', 'Personal and business units', [
                ('Self-storage units', 'Any size, from a locker to a large drive-up unit.'),
                ('Building storage rooms', 'Basement storage cages and rooms in apartment buildings.'),
                ('Partial cleanouts', 'Point out the boxes you\'re keeping. We take everything else.'),
                ('Business storage', 'Old inventory, files and furniture.', '/commercial-junk-removal/'),
            ]),
            ('Usual contents', "If it's in the unit, ask", [
                ('Furniture', 'Couches, chairs, tables and bed frames.', '/furniture-appliance-removal/'),
                ('Boxes &amp; bags', 'Clothes, household items and things packed years ago.'),
                ('Filing cabinets &amp; office items', 'Desks, cabinets and old equipment.'),
                ('Hazardous items', 'Paint and chemicals need special handling. Tell us if they\'re in there.'),
            ]),
        )),
        band('book', 'book-title',
             '<div class="split"><h2 id="book-title">Before you book</h2><div class="prose">'
             '<h3>Check the facility rules</h3><p>Many storage facilities set access hours and have rules for large move-outs, like using a loading area. Ask the front desk.</p>'
             '<h3>Plan for access</h3><p>Someone with the key or gate code needs to get the crew into the unit. Work that out with the facility ahead of time.</p>'
             '<h3>Give notice</h3><p>Most rental agreements ask for notice before you move out. Check yours so you aren\'t billed for another month.</p>'
             '<h3>Pull out keepers</h3><p>Take out what you want to keep, or tell us exactly which items stay.</p>'
             '</div></div>', dark=True),
        band('how', 'how-title', head('how-title', 'How it works', 'A photo from the door is usually enough to start.') + steps(PHOTO_STEPS)),
        related('storage-unit-cleanouts'),
    ],
    faq=[
        ('Can I just send one photo of the unit?', 'Yes. A photo from the door is usually enough to start. Add a few more if things are stacked deep.'),
        ('Can you take some things and leave the rest?', 'Yes. Tell us what stays and we\'ll leave it.'),
        ('Do I have to be there?', 'Someone has to give the crew access to the unit. Talk to us about what works for you and the facility.'),
        ('Which storage facilities do you go to?', 'Facilities across the five boroughs and surrounding areas. Send the facility address with your request.'),
        ('How much does a storage unit cleanout cost?', 'It depends on how full the unit is and what\'s in it. Send a photo for a free estimate.'),
    ],
))

PAGES.append(dict(
    slug='commercial-junk-removal', crumb='Commercial junk removal',
    title='Commercial Junk Removal NYC | The Clear Out Crew',
    desc='Office furniture, business equipment and commercial cleanouts across NYC. One-off jobs, recurring work and subcontracting. Free estimates.',
    service_name='Commercial junk removal', service_type='Commercial junk removal', area_served=ALL_BOROS,
    h1='Commercial junk <span class="y">removal</span>',
    lede="Office furniture, business equipment and full commercial cleanouts. We take one-off jobs, recurring work and large projects, and we're open to subcontracting.",
    proof=['Offices &amp; businesses', 'One-off or recurring', 'Subcontracting'],
    cta='Talk to us about your project',
    hero_right=caps([
        ('Office cleanouts', 'Desks, chairs, filing cabinets and the rest of the office furniture.'),
        ('Business equipment', "Equipment and fixtures you've replaced or no longer need."),
        ('Commercial spaces', 'Clear a space before a move-out, lease end or renovation.'),
        ('Subcontracting', 'Extra capacity for waste management and hauling companies.', '#subcontracting'),
    ]),
    sections=[
        band('work', 'work-title', head('work-title', 'Who we work with', 'Businesses, property firms and other haulers. Tell us the space, the volume and the deadline.') + svc_groups(
            ('Businesses', 'Offices, shops, commercial spaces', [
                ('Office furniture removal', 'Desks, chairs, conference tables, shelving and filing cabinets.'),
                ('Business equipment', 'Old equipment and fixtures, cleared out in one trip or several.'),
                ('Commercial cleanouts', 'Empty a space before you hand back the keys or start a buildout.'),
                ('Storage &amp; back rooms', 'Old inventory, files and furniture.', '/storage-unit-cleanouts/'),
            ]),
            ('Industry partners', 'Contractors, property firms, haulers', [
                ('Multi-unit &amp; recurring work', 'Ongoing removal across buildings and units, scheduled around your team.', '/property-management-cleanouts/'),
                ('Renovation debris', 'Wood, drywall and other accepted construction materials.', '/construction-debris-removal/'),
                ('Large projects', 'High-volume removal for contractors and property firms.'),
                ('Subcontracting', 'Overflow jobs for waste management and hauling companies.', '#subcontracting'),
            ]),
        )),
        band('subcontracting', 'sub-title',
             '<div class="split"><h2 id="sub-title">Extra capacity for haulers</h2><div class="prose">'
             '<p>Waste management and hauling companies sometimes have more jobs than trucks. We take subcontracted work, from single cleanouts to high-volume projects.</p>'
             '<p>Send the location, the volume, the timing and how you want the job handled. We\'ll tell you what we can take on.</p>'
             '<p><a class="btn btn-yellow" href="/#quote" style="margin-top:6px">Talk to us about subcontracting</a></p>'
             '</div></div>', dark=True),
        band('how', 'how-title', head('how-title', 'How it works', 'For businesses, photos plus a deadline is the fastest way to a price.') + steps([
            ('Tell us about the space', 'Send photos, the address and what needs to go. Include building rules or loading dock details.'),
            ('Get a quote', "We'll get back to you with a price and talk through scheduling."),
            ('We clear it out', 'Our crew loads everything and hauls it away, one-off or on a recurring schedule.'),
        ])),
        related('commercial-junk-removal'),
    ],
    faq=[
        ('Do you remove office furniture?', 'Yes. Desks, chairs, conference tables, shelving, filing cabinets and other office furniture.'),
        ('Can you set up recurring pickups?', 'Yes. We handle ongoing removal across buildings and units, scheduled around your team.'),
        ('Do you subcontract for other hauling companies?', 'Yes. We take subcontracted jobs from waste management and hauling companies, including large-volume projects.'),
        ('Can you clear a space before our lease ends?', 'Yes. Send photos and your deadline and we\'ll quote it.'),
        ('Do you take office electronics?', 'Business electronics have their own disposal rules in New York. List computers, monitors and printers in your request and we\'ll tell you what we can take.'),
    ],
))

PAGES.append(dict(
    slug='construction-debris-removal', crumb='Construction debris removal',
    title='Construction Debris Removal NYC | The Clear Out Crew',
    desc='Renovation debris removal in NYC: wood, drywall, old cabinets and other accepted materials, for homeowners, contractors and property managers.',
    service_name='Construction debris removal', service_type='Construction debris removal', area_served=ALL_BOROS,
    h1='Construction debris <span class="y">removal</span>',
    lede='Renovation leftovers piling up? We haul away wood, drywall and other accepted construction materials for homeowners, contractors and property managers.',
    proof=['Homeowners &amp; contractors', 'Accepted materials', 'Free estimates'],
    hero_right=caps([
        ('Renovation debris', 'Wood, drywall and the rest of the mess a remodel leaves behind.'),
        ('Old cabinets &amp; fixtures', 'Pieces pulled out during a kitchen or bath job. Send a photo to confirm.'),
        ('Post-renovation cleanouts', 'Clear a unit so it can be cleaned and rented.', '/property-management-cleanouts/'),
        ('Contractor overflow', 'Extra hauling when a job makes more debris than planned.', '/commercial-junk-removal/#subcontracting'),
    ]),
    sections=[
        band('take', 'take-title', head('take-title', 'What we take', "Accepted construction materials, loose or bagged. If you're unsure about something, ask before the job.") + svc_groups(
            ('We take', 'Common renovation debris', [
                ('Wood &amp; lumber', 'Scrap lumber, old framing and trim.'),
                ('Drywall', 'Torn-out drywall and leftover sheets.'),
                ('Cabinets &amp; fixtures', 'Old cabinets and other pieces pulled out during a remodel.'),
                ('Mixed renovation debris', "Bagged or loose, as long as it's accepted material. Send photos."),
            ]),
            ('Needs special handling', 'Ask first, or call a specialist', [
                ('Asbestos', 'Hazardous waste. It needs a licensed abatement company, never a regular haul.'),
                ('Paint &amp; chemicals', 'Paint, solvents and other hazardous products need special handling.'),
                ('Anything you\'re unsure of', "Send a photo and we'll tell you before the job."),
            ]),
        )),
        band('rules', 'rules-title',
             '<div class="split"><h2 id="rules-title">NYC rules on construction debris</h2><div class="prose">'
             '<h3>Small DIY projects</h3><p>If you did the work yourself, DSNY will collect some debris curbside under its large-item rules. Cabinets, drywall, sinks and similar items count toward the limit of 6 large items per collection day.</p>'
             '<h3>Professional jobs</h3><p>Construction and demolition waste from professional contractors can\'t be put out as residential garbage. DSNY says the contractor or resident has to arrange private removal.</p>'
             '<h3>Hazardous materials</h3><p>Asbestos should never go out with trash or recycling. Paint and harsh chemicals need special disposal too.</p>'
             + source('construction', 'large') + '</div></div>', dark=True),
        band('how', 'how-title', head('how-title', 'How it works', 'Photos of the pile are all we need to start.') + steps(PHOTO_STEPS)),
        related('construction-debris-removal'),
    ],
    faq=[
        ('Do you take debris from contractors or just homeowners?', 'Both. We work with homeowners, contractors and property managers.'),
        ("What construction materials can't you take?", 'Hazardous materials like paint, chemicals and anything with asbestos need special handling. Ask about any material you\'re unsure of before the job.'),
        ('Can I put renovation debris out for DSNY instead?', 'Small DIY projects can go out curbside under DSNY\'s large-item rules, up to 6 items per collection day. Waste from professional contractors can\'t be set out as residential garbage.'),
        ('How much does debris removal cost?', 'It depends on the amount, the material and access. Send photos of the pile for a free estimate.'),
    ],
))

PAGES.append(dict(
    slug='property-management-cleanouts', crumb='Property & real estate cleanouts',
    title='Landlord &amp; Real Estate Cleanouts NYC | The Clear Out Crew',
    desc='Rental turnovers, vacant units, eviction cleanouts and pre-sale cleanouts for NYC property managers, landlords and real estate agents.',
    service_name='Property management and real estate cleanouts', service_type='Property cleanout', area_served=ALL_BOROS,
    h1='Property &amp; real estate <span class="y">cleanouts</span>',
    lede='Property managers, landlords and real estate agents need a crew that answers the phone and shows up. We clear units and buildings so they can be cleaned, repaired, listed or sold.',
    proof=['Turnovers &amp; vacant units', 'Multi-unit work', 'Free estimates'],
    cta='Talk to us about your property',
    hero_right=caps([
        ('Rental turnovers', 'Clear out what tenants leave behind so the unit can be cleaned, repaired and re-listed.'),
        ('Eviction cleanouts', 'Cleanouts after a legally authorized eviction.'),
        ('Pre-sale &amp; closing', 'Empty a property before listing, closing or renovation.', '#real-estate'),
        ('Multi-unit &amp; recurring', 'Ongoing removal across buildings and units, scheduled around your team.'),
    ]),
    sections=[
        band('services', 'svc-title', head('svc-title', 'For managers and agents', 'One unit or a whole portfolio. Send the address, photos and your deadline.') + svc_groups(
            ('Property management', 'Managers, landlords, owners', [
                ('Rental turnovers', 'Furniture, trash and belongings left after a move-out.'),
                ('Vacant properties', 'Empty units and buildings cleared before repairs or a new lease.'),
                ('Eviction cleanouts', 'Only after a legally authorized eviction.'),
                ('Building maintenance', 'Basements, storage rooms and common areas that collect junk.'),
                ('Multi-unit &amp; recurring work', 'Several units at once, or a regular schedule for your buildings.'),
            ]),
            ('Real estate', 'Agents, sellers, investors', [
                ('Pre-listing cleanouts', 'Get a property empty so it can be shown, staged or photographed.'),
                ('Closing cleanouts', 'Clear what\'s left before the keys change hands.'),
                ('Estate properties', 'Homes being sold after a death in the family.', '/estate-cleanouts/'),
                ('Pre-renovation cleanouts', 'Empty the space so the contractor can start.', '/construction-debris-removal/'),
            ], 'real-estate'),
        )),
        band('expect', 'expect-title',
             '<div class="split"><h2 id="expect-title">How we work with property pros</h2><div class="prose">'
             '<p>Send photos of the unit, the address and your deadline. We\'ll get back to you with a price.</p>'
             '<p>For buildings with ongoing needs, we can take on recurring work and schedule it around your team, from one turnover a month to several units at once.</p>'
             '<p>Working in a building with rules for vendors, like elevator reservations or insurance paperwork? Include them in your request so they\'re sorted out before the job.</p>'
             '<p><a class="btn btn-yellow" href="/#quote" style="margin-top:6px">Talk to us about your property</a></p>'
             '</div></div>', dark=True),
        related('property-management-cleanouts'),
    ],
    faq=[
        ('Do you do eviction cleanouts?', 'Yes, after a legally authorized eviction.'),
        ('Can you handle several units at once?', 'Yes. We take on multi-unit work and ongoing removal across buildings.'),
        ('Can you set up recurring work for our buildings?', 'Yes. Tell us how often and where, and we\'ll schedule it around your team.'),
        ('Do you work with real estate agents?', 'Yes. We clear properties before listing, closing or renovation.'),
        ('How fast can you turn over a unit?', 'It depends on the unit and our schedule that week. Tell us your deadline when you ask for a quote.'),
    ],
))

# =====================================================================
# BOROUGH PAGES
# =====================================================================
def boro_page(slug, name, title, desc, lede, jobs, home_items, biz_items, logistics_title, logistics, hoods, faq, the=''):
    nm = f'{the}{name}'  # "the Bronx" in sentences
    return dict(
        slug=slug, crumb=f'{the.capitalize()}{name}',
        title=title, desc=desc,
        service_name=f'Junk removal in {nm}', service_type='Junk removal',
        area_served=[{"@type": "AdministrativeArea", "name": f"{nm}, NY", "sameAs": WIKI[nm if the else name]}],
        h1=f'Junk removal in <span class="y">{the.capitalize() if the else ""}{name}</span>',
        lede=lede,
        proof=['Free estimates', 'Homes &amp; businesses', f'All of {nm}'],
        hero_right=caps(jobs),
        sections=[
            band('services', 'svc-title', head('svc-title', f'What we haul in {nm}', 'Residential and commercial jobs, from one piece of furniture to a whole property.') + svc_groups(
                ('Homes', 'Owners, renters, families', home_items),
                ('Property &amp; business', 'Managers, agents, contractors', biz_items),
            )),
            band('local', 'local-title',
                 f'<div class="split"><div><h2 id="local-title">{logistics_title}</h2>'
                 f'<h3 style="font-size:1.35rem;letter-spacing:.06em;margin:clamp(28px,4vw,40px) 0 14px">Neighborhoods we cover</h3>{chips(hoods)}'
                 f'<p class="lede" style="font-size:1rem">And everywhere else in {nm}. Not sure we cover your block? Call and ask.</p></div>'
                 f'<div class="prose">{logistics}</div></div>', dark=True),
            band('boros', 'boros-title', head('boros-title', 'Other boroughs', 'We work across all five boroughs, plus surrounding areas.') + boro_list(slug)),
        ],
        faq=faq,
    )

S = lambda slug: f'/{slug}/'

PAGES.append(boro_page(
    'brooklyn-junk-removal', 'Brooklyn',
    'Junk Removal Brooklyn, NY | The Clear Out Crew',
    'Junk removal and cleanouts in Brooklyn: brownstones, walk-ups, basements and storefronts. Furniture, appliances and full cleanouts. Free estimates.',
    'Brownstone basements, fourth-floor walk-ups, storefronts and family houses. We clear out furniture, appliances and whole properties across Brooklyn. Send a few photos for a free estimate.',
    [('Brownstone &amp; walk-up jobs', 'Furniture and boxes carried down narrow stairs and out over the stoop.'),
     ('Basement cleanouts', 'Rowhouse and two-family basements that have filled up over the years.', S('apartment-cleanouts')),
     ('Rental turnovers', 'Units cleared between tenants for Brooklyn landlords and managers.', S('property-management-cleanouts')),
     ('Renovation debris', 'Leftovers from kitchen, bath and gut renovations.', S('construction-debris-removal'))],
    [('Furniture &amp; appliance removal', 'Couches, mattresses, fridges and washers, out of the apartment and onto our truck.', S('furniture-appliance-removal')),
     ('Apartment &amp; house cleanouts', 'Full or partial, from a studio to a three-story rowhouse.', S('apartment-cleanouts')),
     ('Estate cleanouts', 'Family homes cleared after the keepsakes are out.', S('estate-cleanouts')),
     ('Storage unit cleanouts', 'Self-storage and building storage rooms.', S('storage-unit-cleanouts'))],
    [('Commercial junk removal', 'Shops, restaurants and offices clearing out old furniture and equipment.', S('commercial-junk-removal')),
     ('Construction debris removal', 'Wood, drywall and other accepted materials from renovations.', S('construction-debris-removal')),
     ('Property management', 'Turnovers, vacant units and building basements.', S('property-management-cleanouts')),
     ('Real estate cleanouts', 'Empty properties before listing or closing.', S('property-management-cleanouts') + '#real-estate')],
    'Brooklyn buildings, handled',
    '<p>A lot of Brooklyn is brownstones, rowhouses and walk-ups. That means narrow stairs, tight turns and a stoop between the front door and the truck. Tell us the floor and anything awkward about the stairs when you send photos, so the estimate covers it.</p>'
    '<p>Basements are a big one here. Two-family houses and rowhouses collect years of furniture, boxes and old appliances downstairs. We clear the whole basement or just the part you point out.</p>'
    '<p>In larger elevator buildings, ask your super about reserving the service elevator and any move-out hours before the job.</p>'
    '<h3>Curbside or a crew?</h3><p>DSNY will pick up to 6 large items per collection day at the curb, if you can get them there and follow the rules for mattresses and appliances. For anything bigger, or anything still upstairs, send us photos.</p>',
    ['Williamsburg', 'Greenpoint', 'Bushwick', 'Bed-Stuy', 'Crown Heights', 'Park Slope', 'Flatbush', 'Sunset Park', 'Bay Ridge', 'Bensonhurst', 'Sheepshead Bay', 'Canarsie', 'East New York', 'Coney Island'],
    [('Do you cover all of Brooklyn?', 'Yes. From Greenpoint to Coney Island and Bay Ridge to East New York. Include your ZIP code when you request a quote.'),
     ('Can you take furniture out of a walk-up?', 'Yes. Carrying it down the stairs is part of the job. Tell us the floor so the estimate covers it.'),
     ('Can you clear out a brownstone basement?', 'Yes. We clear full basements or just the section you point out.'),
     ('Do you work with Brooklyn landlords and property managers?', 'Yes. We handle rental turnovers, vacant units and recurring work across buildings.'),
     ('How much does junk removal cost in Brooklyn?', 'It depends on how much there is, what it is and how easy it is to reach. Send photos for a free estimate.')],
))

PAGES.append(boro_page(
    'queens-junk-removal', 'Queens',
    'Junk Removal Queens, NY | The Clear Out Crew',
    'Junk removal and cleanouts in Queens: houses, basements, garages, co-ops and garden apartments. Furniture, appliances and estates. Free estimates.',
    'Detached houses with full basements, garden apartments, co-ops and storefronts. We haul furniture and appliances and clear out whole properties across Queens. Send a few photos for a free estimate.',
    [('House &amp; basement cleanouts', 'Full basements, attics and garages in Queens houses.', S('apartment-cleanouts')),
     ('Co-op &amp; garden apartments', 'Cleanouts in buildings with elevator and vendor rules.'),
     ('Estate cleanouts', 'Family homes cleared once the family has what it wants.', S('estate-cleanouts')),
     ('Yard cleanouts', 'Bags, bins, old furniture and debris piled outside.')],
    [('Furniture &amp; appliance removal', 'Sectionals, mattresses, fridges, washers and dryers.', S('furniture-appliance-removal')),
     ('Apartment &amp; house cleanouts', 'One room, one floor or the whole house.', S('apartment-cleanouts')),
     ('Estate cleanouts', 'Houses and apartments emptied for families and executors.', S('estate-cleanouts')),
     ('Storage unit cleanouts', 'Self-storage units and building storage rooms.', S('storage-unit-cleanouts'))],
    [('Commercial junk removal', 'Offices, shops and restaurants clearing out furniture and equipment.', S('commercial-junk-removal')),
     ('Construction debris removal', 'Renovation debris from houses and apartments.', S('construction-debris-removal')),
     ('Property management', 'Turnovers and vacant units for Queens landlords.', S('property-management-cleanouts')),
     ('Real estate cleanouts', 'Houses emptied before listing or closing.', S('property-management-cleanouts') + '#real-estate')],
    'Queens houses and buildings',
    '<p>Queens has more houses than most of the city, and houses fill up. Full basements, attics, detached garages and backyards are common cleanout jobs. Point out what goes and what stays, and we\'ll take it from there.</p>'
    '<p>Neighborhoods like Jackson Heights and Forest Hills also have a lot of co-ops and garden apartment buildings. Those often have rules about elevators, move-out hours and paperwork from vendors. Ask your management office what they need and include it in your quote request.</p>'
    '<h3>Curbside or a crew?</h3><p>DSNY collects up to 6 large items per collection day from the curb. Fridges and air conditioners need a Freon appointment first, and mattresses must be bagged. For a full basement or a house cleanout, send us photos instead.</p>',
    ['Astoria', 'Long Island City', 'Sunnyside', 'Woodside', 'Jackson Heights', 'Elmhurst', 'Flushing', 'Forest Hills', 'Ridgewood', 'Jamaica', 'Bayside', 'Fresh Meadows', 'Richmond Hill', 'Ozone Park', 'Howard Beach', 'The Rockaways'],
    [('Do you cover all of Queens?', 'Yes. From Astoria and Long Island City out to Bayside, Jamaica and the Rockaways. Include your ZIP code with your request.'),
     ('Can you clear out a whole house?', 'Yes. Basements, attics, garages, yards and every room in between, or just the parts you choose.'),
     ('Can you work in a co-op with building rules?', 'Yes. Find out what the building requires, like elevator reservations or vendor paperwork, and include it in your quote request.'),
     ('Do you do estate cleanouts in Queens?', 'Yes. We work with families, executors and real estate agents to empty houses and apartments.'),
     ('How much does junk removal cost in Queens?', 'It depends on the size of the job and access. Send photos for a free estimate.')],
))

PAGES.append(boro_page(
    'manhattan-junk-removal', 'Manhattan',
    'Junk Removal Manhattan, NY | The Clear Out Crew',
    'Junk removal and apartment cleanouts in Manhattan: doorman buildings, walk-ups, offices and storage. Service elevator rules handled. Free estimates.',
    'Doorman buildings with service elevator rules, fifth-floor walk-ups, offices and storage rooms. We clear out furniture, appliances and whole apartments across Manhattan. Send photos for a free estimate.',
    [('Apartment cleanouts', 'Studios to large units, in elevator buildings and walk-ups.', S('apartment-cleanouts')),
     ('Furniture removal', 'Sofas, beds and dressers out of tight hallways and small elevators.', S('furniture-appliance-removal')),
     ('Office cleanouts', 'Desks, chairs and filing cabinets from Manhattan offices.', S('commercial-junk-removal')),
     ('Move-out cleanouts', 'What\'s left after the movers are gone.')],
    [('Furniture &amp; appliance removal', 'Single pieces or a full apartment of furniture.', S('furniture-appliance-removal')),
     ('Apartment cleanouts', 'Full or partial, including walk-ups.', S('apartment-cleanouts')),
     ('Estate cleanouts', 'Co-op and rental apartments emptied for families and executors.', S('estate-cleanouts')),
     ('Storage unit cleanouts', 'Building storage rooms and self-storage units.', S('storage-unit-cleanouts'))],
    [('Commercial junk removal', 'Office furniture, equipment and commercial cleanouts.', S('commercial-junk-removal')),
     ('Construction debris removal', 'Renovation leftovers from apartments and offices.', S('construction-debris-removal')),
     ('Property management', 'Turnovers and vacant units for managers and owners.', S('property-management-cleanouts')),
     ('Real estate cleanouts', 'Apartments emptied before listing or closing.', S('property-management-cleanouts') + '#real-estate')],
    'Manhattan buildings, handled',
    '<p>Most Manhattan jobs come down to the building. Many co-ops, condos and rental buildings require a reserved service elevator, limit move-outs to certain hours and ask vendors for paperwork like a certificate of insurance. Ask your super or management office what they need and put it in your quote request.</p>'
    '<p>Walk-ups are their own job. Five flights with a dresser takes time, so tell us the floor when you send photos and the estimate will account for it.</p>'
    '<p>Street parking is tight. If your building has a loading area or a better spot for the truck, let us know.</p>'
    '<h3>Curbside or a crew?</h3><p>DSNY picks up large items at the curb, up to 6 per collection day, but someone still has to get them down to the street. When that\'s the hard part, send us photos.</p>',
    ['Upper East Side', 'Upper West Side', 'Harlem', 'Washington Heights', 'Inwood', 'Midtown', "Hell's Kitchen", 'Chelsea', 'Murray Hill', 'Gramercy', 'Greenwich Village', 'East Village', 'Lower East Side', 'SoHo', 'Tribeca', 'Financial District'],
    [('Do you cover all of Manhattan?', 'Yes. From Inwood to the Financial District. Include your address or ZIP code with your request.'),
     ('My building requires a certificate of insurance. What should I do?', 'Ask your management office exactly what they need from vendors and include it in your quote request so it\'s sorted out before the job.'),
     ('Can you clear out a walk-up apartment?', 'Yes. Stairs are part of the job. Tell us the floor so the estimate covers it.'),
     ('Do you remove office furniture in Manhattan?', 'Yes. We clear desks, chairs, filing cabinets and other office furniture.'),
     ('How much does junk removal cost in Manhattan?', 'It depends on the amount, the items and the building. Send photos for a free estimate.')],
))

PAGES.append(boro_page(
    'bronx-junk-removal', 'Bronx',
    'Junk Removal Bronx, NY | The Clear Out Crew',
    'Junk removal and cleanouts in the Bronx: prewar buildings, co-ops, houses and businesses. Furniture, appliances and full cleanouts. Free estimates.',
    'Prewar elevator buildings, big co-ops, two-family houses and businesses. We haul furniture and appliances and clear out whole properties across the Bronx. Send a few photos for a free estimate.',
    [('Apartment cleanouts', 'Prewar and co-op apartments, full or partial.', S('apartment-cleanouts')),
     ('House cleanouts', 'Basements, garages and yards in Bronx houses.', S('apartment-cleanouts')),
     ('Rental turnovers', 'Units cleared between tenants for landlords and managers.', S('property-management-cleanouts')),
     ('Furniture &amp; appliances', 'Couches, mattresses, fridges and washers.', S('furniture-appliance-removal'))],
    [('Furniture &amp; appliance removal', 'Bulky pieces carried out and hauled away.', S('furniture-appliance-removal')),
     ('Apartment &amp; house cleanouts', 'One room or the whole place.', S('apartment-cleanouts')),
     ('Estate cleanouts', 'Family apartments and houses emptied with care for what stays.', S('estate-cleanouts')),
     ('Storage unit cleanouts', 'Self-storage and building storage.', S('storage-unit-cleanouts'))],
    [('Commercial junk removal', 'Businesses clearing out furniture, equipment and back rooms.', S('commercial-junk-removal')),
     ('Construction debris removal', 'Renovation debris from units and houses.', S('construction-debris-removal')),
     ('Property management', 'Turnovers, vacant units and multi-unit work.', S('property-management-cleanouts')),
     ('Real estate cleanouts', 'Properties emptied before listing or closing.', S('property-management-cleanouts') + '#real-estate')],
    'Bronx buildings and houses',
    '<p>The Bronx has a lot of large prewar elevator buildings and big co-ops, along with two-family houses in neighborhoods like Throgs Neck, Pelham Bay and Riverdale. Big buildings usually have elevator and move-out rules. Ask your super or management office before the job and include what they need in your request.</p>'
    '<p>For houses, basements, garages and yards are where most of the junk ends up. Tell us which areas need clearing and what stays.</p>'
    '<p>Landlords and managers with several units can line up turnovers together or set up recurring work.</p>'
    '<h3>Curbside or a crew?</h3><p>DSNY collects up to 6 large items per collection day from the curb, with extra rules for mattresses and fridges. If it\'s more than that, or it\'s still upstairs, send us photos.</p>',
    ['Riverdale', 'Kingsbridge', 'Fordham', 'Bedford Park', 'Grand Concourse', 'Mott Haven', 'Hunts Point', 'Soundview', 'Parkchester', 'Castle Hill', 'Morris Park', 'Pelham Bay', 'Throgs Neck', 'Co-op City', 'Williamsbridge', 'Wakefield'],
    [('Do you cover all of the Bronx?', 'Yes. From Riverdale and Kingsbridge to Throgs Neck, Co-op City and Mott Haven. Include your ZIP code with your request.'),
     ('Can you work in a large co-op or prewar building?', 'Yes. Find out the building\'s elevator and vendor rules and include them in your quote request.'),
     ('Do you clear out houses too?', 'Yes. Basements, garages, yards and full houses.'),
     ('Can you handle several rental units at once?', 'Yes. We take on multi-unit turnovers and recurring work for Bronx landlords and managers.'),
     ('How much does junk removal cost in the Bronx?', 'Prices depend on the volume, the type of items and the building, like the floor and elevator access. Photos of each room get you a free estimate.')],
    the='the ',
))

PAGES.append(boro_page(
    'staten-island-junk-removal', 'Staten Island',
    'Junk Removal Staten Island, NY | The Clear Out Crew',
    'Junk removal and cleanouts on Staten Island: houses, garages, basements, sheds and yards. Furniture, appliances and estates. Free estimates.',
    'Single-family houses, garages, basements, sheds and backyards. We haul furniture and appliances and clear out whole properties across Staten Island. Send a few photos for a free estimate.',
    [('Garage &amp; shed cleanouts', 'Years of tools, boxes and things nobody uses anymore.', S('apartment-cleanouts')),
     ('Basement cleanouts', 'Full or partial, from one corner to the whole floor.', S('apartment-cleanouts')),
     ('Yard &amp; outdoor cleanouts', 'Bags, bins, old furniture and debris piled outside.'),
     ('Estate cleanouts', 'Family houses emptied once the keepsakes are out.', S('estate-cleanouts'))],
    [('Furniture &amp; appliance removal', 'Couches, mattresses, fridges, washers and dryers.', S('furniture-appliance-removal')),
     ('House cleanouts', 'Every room, the basement, the garage and the yard.', S('apartment-cleanouts')),
     ('Estate cleanouts', 'Houses emptied for families and executors.', S('estate-cleanouts')),
     ('Storage unit cleanouts', 'Self-storage units you\'re done paying for.', S('storage-unit-cleanouts'))],
    [('Commercial junk removal', 'Offices, shops and commercial spaces.', S('commercial-junk-removal')),
     ('Construction debris removal', 'Renovation debris from house projects.', S('construction-debris-removal')),
     ('Property management', 'Turnovers and vacant houses for landlords.', S('property-management-cleanouts')),
     ('Real estate cleanouts', 'Houses emptied before listing or closing.', S('property-management-cleanouts') + '#real-estate')],
    'Staten Island houses, handled',
    '<p>Staten Island is mostly houses, and houses mean garages, basements, sheds and backyards. Those are where things pile up. Tell us which spaces need clearing and point out anything that stays.</p>'
    '<p>Driveways usually make loading easier here than in the rest of the city. If the truck can\'t get close, or the job is up a steep driveway or down basement stairs, mention it in your request.</p>'
    '<h3>Curbside or a crew?</h3><p>DSNY collects up to 6 large items per collection day at the curb. Wood furniture goes out on your trash-only day and metal goes with recycling. Fridges and air conditioners need a Freon appointment first. For a garage, basement or full house, send us photos instead.</p>',
    ['St. George', 'Stapleton', 'Port Richmond', 'West Brighton', 'Westerleigh', 'Mariners Harbor', 'Bulls Head', 'Todt Hill', 'Dongan Hills', 'Grant City', 'New Dorp', 'Great Kills', 'Eltingville', 'Annadale', 'Huguenot', 'Tottenville'],
    [('Do you cover all of Staten Island?', 'Yes. From St. George to Tottenville. Include your ZIP code with your request.'),
     ('Can you clear out a garage or shed?', 'Yes. Garages, sheds, basements and yards. Point out what stays and we take the rest.'),
     ('Do you do whole-house cleanouts?', 'Yes, including estate cleanouts for families and executors.'),
     ('Can you pick up just a few large items?', 'Yes. We take jobs from a single piece of furniture to a full house.'),
     ('How much does junk removal cost on Staten Island?', 'The price comes down to how much is going and where it sits, like a basement, a garage or the yard. Send photos of each space for a free estimate.')],
))
