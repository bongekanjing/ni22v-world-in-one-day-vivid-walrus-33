"""The day's reporting, one record per story.

Every record names the story as it was reported on Sunday 22 November 2026 and
the outlet that carried it. Region tags are what the page counts, so the region
bar is derived here rather than typed onto the sheet: the numbers on the page
cannot drift away from the stories the page shows.

Stories that happened at a place on Earth carry its latitude and longitude.
The map is drawn from those numbers, so a pin can never sit somewhere the story
did not happen.
"""

DAY_LABEL = "Sunday 22 November 2026"

# The three sell lines under the masthead, in the order the leads appear.
STRAPLINE = (
    "COP31 adopts a deal that never names fossil fuels",
    "Russia sends about 150 drones over Ukraine",
    "Iran strikes Bahrain; two tankers hit in Hormuz",
)

# Six figures drawn from the leads, each one stated by the reporting.
FIGURES = [
    ("~200", "countries in\nthe Antalya hall"),
    ("150", "drones sent over\nUkraine overnight"),
    ("8,000", "homes wrecked\nin one Brazil town"),
    ("36", "still missing\nin a Java fire"),
    ("11", "dead as a cartel\nboss is taken"),
    ("2", "spacecraft reach\nMercury at once"),
]

REGIONS = [
    ("EUROPE", "#1f4e79"),
    ("MIDDLE EAST", "#8c1f2b"),
    ("AMERICAS", "#2e6b4f"),
    ("ASIA-PACIFIC", "#b8621b"),
    ("AFRICA", "#7a5230"),
    ("WORLD", "#5b3d82"),
]

LEADS = [
    {
        "tag": "COP31: DEAL ADOPTED",
        "flag": "TOP STORY",
        "region": "EUROPE",
        "figure": "~200 nations",
        "kicker": "ANTALYA, TURKIYE · CLIMATE",
        "head": ["COP31 adopts a climate", "deal that omits fossil fuels"],
        "deck": "Nearly 200 countries pass the cover decision two days late; the text never names coal, oil or gas.",
        "outlet": "Reuters, AP",
        "vignette": "summit",
        "caption": "Summit president",
        "lat": 36.9, "lon": 30.7,
    },
    {
        "tag": "UKRAINE: ANOTHER BARRAGE",
        "flag": None,
        "region": "EUROPE",
        "figure": "150 drones",
        "kicker": "KYIV, UKRAINE · WAR",
        "head": ["Russia sends about 150", "drones over Ukraine"],
        "deck": "The air force counts the overnight wave; two nights earlier 404 drones and missiles flew, two of them into Poland.",
        "outlet": "Kyiv Independent, Reuters",
        "vignette": "drones",
        "caption": "Air force count",
        "lat": 50.4, "lon": 30.5,
    },
    {
        "tag": "BAHRAIN: SITE STRUCK",
        "flag": None,
        "region": "MIDDLE EAST",
        "figure": "2 attacks",
        "kicker": "MANAMA, BAHRAIN · IRAN WAR",
        "head": ["Iran hits a Bahraini", "plant; tankers attacked"],
        "deck": "A civilian industrial site burns with no injuries reported, and two tankers are struck in the Strait of Hormuz.",
        "outlet": "Al Jazeera, CNA",
        "vignette": "refinery",
        "caption": "Bahrain government",
        "lat": 26.2, "lon": 50.6,
    },
]

# Mid-tier cards. "num" is the story's number on the page and on the map.
CARDS = [
    {
        "num": 4, "tab": "WITHDRAWAL DEMAND", "place": "BEIRUT",
        "head": ["Aoun tells Israel to quit", "and Iran to stop meddling"],
        "deck": "In his Independence Day address he calls the occupation and foreign meddling inseparably linked.",
        "outlet": "Al Jazeera, MEE", "region": "MIDDLE EAST", "icon": "parliament",
        "lat": 33.9, "lon": 35.5,
    },
    {
        "num": 5, "tab": "POWER CUTS", "place": "TEHRAN",
        "head": ["Iran rations electricity", "as war damage bites"],
        "deck": "Rolling cuts of about two hours begin, the grid operator says.",
        "outlet": "AFP", "region": "MIDDLE EAST", "icon": "pylon",
        "lat": 35.7, "lon": 51.4,
    },
    {
        "num": 6, "tab": "KINGPIN TAKEN", "place": "GUASAVE, MEXICO",
        "head": ["Cartel boss 'El Chapo", "Isidro' is captured"],
        "deck": "Soldiers seize an FBI top-ten fugitive; 11 die in Sinaloa gun battles.",
        "outlet": "AP, Reuters", "region": "AMERICAS", "icon": "raid",
        "lat": 25.6, "lon": -108.5,
    },
    {
        "num": 7, "tab": "SUPERCELL STORM", "place": "TUPANCIRETA, BRAZIL",
        "head": ["Storm shreds a Brazil", "town in 40 minutes"],
        "deck": "Four dead, 162 hurt and 8,000 homes damaged as 114km/h winds hit.",
        "outlet": "AFP", "region": "AMERICAS", "icon": "storm",
        "lat": -29.1, "lon": -54.0,
    },
    {
        "num": 8, "tab": "36 MISSING", "place": "CIKANDE, INDONESIA",
        "head": ["Fire kills three at a", "Java sweet factory"],
        "deck": "Rescuers hunt smouldering sections for workers unaccounted for.",
        "outlet": "AP, AFP", "region": "ASIA-PACIFIC", "icon": "factory",
        "lat": -6.2, "lon": 106.3,
    },
    {
        "num": 9, "tab": "MERCURY ARRIVAL", "place": "IN ORBIT",
        "head": ["Two spacecraft reach", "Mercury after 8 years"],
        "deck": "BepiColombo's European and Japanese halves will split in December.",
        "outlet": "AP, ESA", "region": "WORLD", "icon": "space",
        "lat": None, "lon": None,
    },
    {
        "num": 10, "tab": "24 DEAD", "place": "BAYELSA, NIGERIA",
        "head": ["Mourners' boat capsizes", "on a Delta creek"],
        "deck": "Twenty-four are rescued; police say the operator ignored pleas to turn back.",
        "outlet": "AP", "region": "AFRICA", "icon": "boat",
        "lat": 4.8, "lon": 6.0,
    },
    {
        "num": 11, "tab": "~700,000 FLEE", "place": "MOYALE, ETHIOPIA",
        "head": ["Border fighting displaces", "a vast crowd"],
        "deck": "Islamic Relief's count, not yet independently confirmed; 50,000 reach Kenya.",
        "outlet": "Africanews, UNHCR", "region": "AFRICA", "icon": "displaced",
        "lat": 3.5, "lon": 39.1,
    },
    {
        "num": 12, "tab": "UNITY TALKS", "place": "JERUSALEM",
        "head": ["Eisenkot asks Likud in", "for coalition talks"],
        "deck": "Talks open on Sunday as he works to a December deadline for a majority.",
        "outlet": "Straits Times", "region": "MIDDLE EAST", "icon": "table",
        "lat": 31.8, "lon": 35.2,
    },
    {
        "num": 13, "tab": "ALL FLIGHTS CUT", "place": "BRUSSELS",
        "head": ["Strike to shut Belgian", "airspace on Monday"],
        "deck": "Controllers walk out over austerity; airports plan a near-total stop.",
        "outlet": "AFP", "region": "EUROPE", "icon": "plane",
        "lat": 50.8, "lon": 4.4,
    },
]

# The one-line rail: place, headline, outlet, region.
RAIL = [
    ("SAUDI ARABIA", "Coalition downs a missile aimed at the west", "Reuters", "MIDDLE EAST"),
    ("GAZA", "Death toll reaches 1,671, officials say", "Al Jazeera", "MIDDLE EAST"),
    ("PAKISTAN", "Foreign minister hopeful of a US-Iran deal", "Arab News", "MIDDLE EAST"),
    ("UNITED STATES", "Trump wants a 'permanent' Iran nuclear deal", "AFP", "AMERICAS"),
    ("UNITED STATES", "SEC opens an accounting inquiry into Nvidia", "Bloomberg", "AMERICAS"),
    ("UNITED STATES", "ICE arrests at a Seattle airport delay a flight", "AP", "AMERICAS"),
    ("CANADA", "Defence chief sees no change in US military ties", "Reuters", "AMERICAS"),
    ("HONDURAS", "Swimmer crosses a strait as a tanker burns", "BBC", "AMERICAS"),
    ("FRANCE", "Sixth weekend of marches over living costs", "AFP", "EUROPE"),
    ("GERMANY", "IG Metall widens car and shipyard strikes", "Reuters", "EUROPE"),
    ("PORTUGAL", "Thousands march in Lisbon on living costs", "Reuters", "EUROPE"),
    ("DENMARK", "Russian attaché expelled over an alleged plot", "Guardian", "EUROPE"),
    ("MOLDOVA", "Reports a Russian breach of its airspace", "Kyiv Ind.", "EUROPE"),
    ("POLAND", "NATO will defend 'every inch', Rutte says", "Reuters", "EUROPE"),
    ("SOUTH KOREA", "Education chief quits in an AI cheating row", "AFP", "ASIA-PACIFIC"),
    ("INDIA", "Delhi's air eases to an index of 236", "CPCB", "ASIA-PACIFIC"),
    ("BANGLADESH", "Thirty party homes set alight in unrest", "TOI", "ASIA-PACIFIC"),
    ("AUSTRALIA", "Fred Nile, former NSW MP, dies at 92", "ABC", "ASIA-PACIFIC"),
    ("INDONESIA", "EU signs a trade pact after ten years of talks", "DW", "ASIA-PACIFIC"),
    ("SUDAN", "UN counts 2,230 civilian deaths this year", "UN OHCHR", "AFRICA"),
    ("KENYA", "El Nino rain puts 1.5 million people at risk", "Met Dept", "AFRICA"),
    ("ENGLAND", "Five tries as England beat NZ 37-12", "AP", "WORLD"),
    ("TENNIS", "Alcaraz meets Zverev in the ATP final", "AP", "WORLD"),
    ("SPACE", "Only the third craft ever reaches Mercury", "ESA", "WORLD"),
]

DATE_CHECK = (
    "Wires read to 01:00 UTC on Sunday 22 November 2026. Every story here was reported, "
    "or still developing, on 22 November in at least one time zone. Left out as other "
    "days' news: the Ecuador and Peru earthquakes (20 Nov), the Shenzhen summit (10 Nov) "
    "and last week's Kerch bridge strikes."
)

SOURCES = (
    "Sources: Reuters, AP, AFP, Al Jazeera, BBC, Arab News, Africanews, DW, The Straits "
    "Times, ABC Australia, Kyiv Independent, UN OHCHR, ESA. Pictures and map: original, "
    "drawn in code from this file."
)


def all_stories():
    """Every story on the sheet as one flat list, in page order."""
    out = []
    for lead in LEADS:
        out.append(lead)
    for card in CARDS:
        out.append(card)
    for i, item in enumerate(RAIL):
        out.append({"place": item[0], "head": [item[1]], "outlet": item[2],
                    "region": item[3], "lat": None, "lon": None})
    return out


def region_counts():
    """Count the stories per region, straight from the records above."""
    counts = {name: 0 for name, _ in REGIONS}
    for story in all_stories():
        counts[story["region"]] += 1
    return counts


def total_stories():
    """How many stories the sheet carries, counted rather than asserted."""
    return len(LEADS) + len(CARDS) + len(RAIL)


def pins():
    """Numbered stories that happened at a place on Earth: (num, lat, lon)."""
    out = []
    for i, lead in enumerate(LEADS):
        if lead["lat"] is not None:
            out.append((i + 1, lead["lat"], lead["lon"]))
    for card in CARDS:
        if card["lat"] is not None:
            out.append((card["num"], card["lat"], card["lon"]))
    return out
