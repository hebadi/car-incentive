"""Incentive matching engine - core business logic."""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from itertools import combinations
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incentive_program import IncentiveProgram

# Approximate ZIP-to-state mapping (first 3 digits). In production, use a proper geo library.
_ZIP_PREFIX_TO_STATE: dict[str, str] = {
    "006": "PR", "007": "PR", "008": "PR", "009": "PR",
    "010": "MA", "011": "MA", "012": "MA", "013": "MA", "014": "MA", "015": "MA",
    "016": "MA", "017": "MA", "018": "MA", "019": "MA", "020": "MA", "021": "MA",
    "022": "MA", "023": "MA", "024": "MA", "025": "MA", "026": "MA", "027": "MA",
    "028": "RI", "029": "RI",
    "030": "NH", "031": "NH", "032": "NH", "033": "NH", "034": "NH", "035": "NH",
    "036": "NH", "037": "NH", "038": "NH",
    "039": "ME", "040": "ME", "041": "ME", "042": "ME", "043": "ME", "044": "ME",
    "045": "ME", "046": "ME", "047": "ME", "048": "ME", "049": "ME",
    "050": "VT", "051": "VT", "052": "VT", "053": "VT", "054": "VT", "055": "VT",
    "056": "VT", "057": "VT", "058": "VT", "059": "VT",
    "060": "CT", "061": "CT", "062": "CT", "063": "CT", "064": "CT", "065": "CT",
    "066": "CT", "067": "CT", "068": "CT", "069": "CT",
    "070": "NJ", "071": "NJ", "072": "NJ", "073": "NJ", "074": "NJ", "075": "NJ",
    "076": "NJ", "077": "NJ", "078": "NJ", "079": "NJ", "080": "NJ", "081": "NJ",
    "082": "NJ", "083": "NJ", "084": "NJ", "085": "NJ", "086": "NJ", "087": "NJ",
    "088": "NJ", "089": "NJ",
    "100": "NY", "101": "NY", "102": "NY", "103": "NY", "104": "NY", "105": "NY",
    "106": "NY", "107": "NY", "108": "NY", "109": "NY", "110": "NY", "111": "NY",
    "112": "NY", "113": "NY", "114": "NY", "115": "NY", "116": "NY", "117": "NY",
    "118": "NY", "119": "NY", "120": "NY", "121": "NY", "122": "NY", "123": "NY",
    "124": "NY", "125": "NY", "126": "NY", "127": "NY", "128": "NY", "129": "NY",
    "130": "NY", "131": "NY", "132": "NY", "133": "NY", "134": "NY", "135": "NY",
    "136": "NY", "137": "NY", "138": "NY", "139": "NY", "140": "NY", "141": "NY",
    "142": "NY", "143": "NY", "144": "NY", "145": "NY", "146": "NY", "147": "NY",
    "148": "NY", "149": "NY",
    "150": "PA", "151": "PA", "152": "PA", "153": "PA", "154": "PA", "155": "PA",
    "156": "PA", "157": "PA", "158": "PA", "159": "PA", "160": "PA", "161": "PA",
    "162": "PA", "163": "PA", "164": "PA", "165": "PA", "166": "PA", "167": "PA",
    "168": "PA", "169": "PA", "170": "PA", "171": "PA", "172": "PA", "173": "PA",
    "174": "PA", "175": "PA", "176": "PA", "177": "PA", "178": "PA", "179": "PA",
    "180": "PA", "181": "PA", "182": "PA", "183": "PA", "184": "PA", "185": "PA",
    "186": "PA", "187": "PA", "188": "PA", "189": "PA", "190": "PA", "191": "PA",
    "192": "PA", "193": "PA", "194": "PA", "195": "PA", "196": "PA",
    "197": "DE", "198": "DE", "199": "DE",
    "200": "DC", "201": "VA", "202": "DC", "203": "DC", "204": "MD",
    "205": "DC", "206": "MD", "207": "MD", "208": "MD", "209": "MD",
    "210": "MD", "211": "MD", "212": "MD", "214": "MD", "215": "MD",
    "216": "MD", "217": "WV", "218": "WV", "219": "WV",
    "220": "VA", "221": "VA", "222": "VA", "223": "VA", "224": "VA", "225": "VA",
    "226": "VA", "227": "VA", "228": "VA", "229": "VA", "230": "VA", "231": "VA",
    "232": "VA", "233": "VA", "234": "VA", "235": "VA", "236": "VA", "237": "VA",
    "238": "VA", "239": "VA", "240": "VA", "241": "WV", "242": "WV", "243": "WV",
    "244": "WV", "245": "WV", "246": "WV", "247": "WV", "248": "WV", "249": "WV",
    "250": "WV", "251": "WV", "252": "WV", "253": "WV", "254": "WV", "255": "WV",
    "256": "WV", "257": "WV", "258": "WV", "259": "WV", "260": "WV", "261": "WV",
    "262": "WV", "263": "WV", "264": "WV", "265": "WV", "266": "WV", "267": "WV",
    "268": "WV",
    "270": "NC", "271": "NC", "272": "NC", "273": "NC", "274": "NC", "275": "NC",
    "276": "NC", "277": "NC", "278": "NC", "279": "NC", "280": "NC", "281": "NC",
    "282": "NC", "283": "NC", "284": "NC", "285": "NC", "286": "NC", "287": "NC",
    "288": "NC", "289": "NC",
    "290": "SC", "291": "SC", "292": "SC", "293": "SC", "294": "SC", "295": "SC",
    "296": "SC", "297": "SC", "298": "SC", "299": "SC",
    "300": "GA", "301": "GA", "302": "GA", "303": "GA", "304": "GA", "305": "GA",
    "306": "GA", "307": "GA", "308": "GA", "309": "GA", "310": "GA", "311": "GA",
    "312": "GA", "313": "GA", "314": "GA", "315": "GA", "316": "GA", "317": "GA",
    "318": "GA", "319": "GA",
    "320": "FL", "321": "FL", "322": "FL", "323": "FL", "324": "FL", "325": "FL",
    "326": "FL", "327": "FL", "328": "FL", "329": "FL", "330": "FL", "331": "FL",
    "332": "FL", "333": "FL", "334": "FL", "335": "FL", "336": "FL", "337": "FL",
    "338": "FL", "339": "FL",
    "350": "AL", "351": "AL", "352": "AL", "354": "AL", "355": "AL", "356": "AL",
    "357": "AL", "358": "AL", "359": "AL", "360": "AL", "361": "AL", "362": "AL",
    "363": "AL", "364": "AL", "365": "AL", "366": "AL", "367": "AL", "368": "AL",
    "369": "AL",
    "370": "TN", "371": "TN", "372": "TN", "373": "TN", "374": "TN", "375": "TN",
    "376": "TN", "377": "TN", "378": "TN", "379": "TN", "380": "TN", "381": "TN",
    "382": "TN", "383": "TN", "384": "TN", "385": "TN",
    "386": "MS", "387": "MS", "388": "MS", "389": "MS", "390": "MS", "391": "MS",
    "392": "MS", "393": "MS", "394": "MS", "395": "MS", "396": "MS", "397": "MS",
    "400": "KY", "401": "KY", "402": "KY", "403": "KY", "404": "KY", "405": "KY",
    "406": "KY", "407": "KY", "408": "KY", "409": "KY", "410": "KY", "411": "KY",
    "412": "KY", "413": "KY", "414": "KY", "415": "KY", "416": "KY", "417": "KY",
    "418": "KY", "420": "KY", "421": "KY", "422": "KY", "423": "KY", "424": "KY",
    "425": "KY", "426": "KY", "427": "KY",
    "430": "OH", "431": "OH", "432": "OH", "433": "OH", "434": "OH", "435": "OH",
    "436": "OH", "437": "OH", "438": "OH", "439": "OH", "440": "OH", "441": "OH",
    "442": "OH", "443": "OH", "444": "OH", "445": "OH", "446": "OH", "447": "OH",
    "448": "OH", "449": "OH", "450": "OH", "451": "OH", "452": "OH", "453": "OH",
    "454": "OH", "455": "OH", "456": "OH", "457": "OH", "458": "OH",
    "460": "IN", "461": "IN", "462": "IN", "463": "IN", "464": "IN", "465": "IN",
    "466": "IN", "467": "IN", "468": "IN", "469": "IN", "470": "IN", "471": "IN",
    "472": "IN", "473": "IN", "474": "IN", "475": "IN", "476": "IN", "477": "IN",
    "478": "IN", "479": "IN",
    "480": "MI", "481": "MI", "482": "MI", "483": "MI", "484": "MI", "485": "MI",
    "486": "MI", "487": "MI", "488": "MI", "489": "MI", "490": "MI", "491": "MI",
    "492": "MI", "493": "MI", "494": "MI", "495": "MI", "496": "MI", "497": "MI",
    "498": "MI", "499": "MI",
    "500": "IA", "501": "IA", "502": "IA", "503": "IA", "504": "IA", "505": "IA",
    "506": "IA", "507": "IA", "508": "IA", "509": "IA", "510": "IA", "511": "IA",
    "512": "IA", "513": "IA", "514": "IA", "515": "IA", "516": "IA",
    "520": "WI", "521": "WI", "522": "WI", "530": "WI", "531": "WI", "532": "WI",
    "534": "WI", "535": "WI", "537": "WI", "538": "WI", "539": "WI", "540": "WI",
    "541": "WI", "542": "WI", "543": "WI", "544": "WI", "545": "WI", "546": "WI",
    "547": "WI", "548": "WI", "549": "WI",
    "550": "MN", "551": "MN", "553": "MN", "554": "MN", "555": "MN", "556": "MN",
    "557": "MN", "558": "MN", "559": "MN", "560": "MN", "561": "MN", "562": "MN",
    "563": "MN", "564": "MN", "565": "MN", "566": "MN", "567": "MN",
    "570": "SD", "571": "SD", "572": "SD", "573": "SD", "574": "SD", "575": "SD",
    "576": "SD", "577": "SD",
    "580": "ND", "581": "ND", "582": "ND", "583": "ND", "584": "ND", "585": "ND",
    "586": "ND", "587": "ND", "588": "ND",
    "590": "MT", "591": "MT", "592": "MT", "593": "MT", "594": "MT", "595": "MT",
    "596": "MT", "597": "MT", "598": "MT", "599": "MT",
    "600": "IL", "601": "IL", "602": "IL", "603": "IL", "604": "IL", "605": "IL",
    "606": "IL", "607": "IL", "608": "IL", "609": "IL", "610": "IL", "611": "IL",
    "612": "IL", "613": "IL", "614": "IL", "615": "IL", "616": "IL", "617": "IL",
    "618": "IL", "619": "IL", "620": "IL", "622": "IL", "623": "IL", "624": "IL",
    "625": "IL", "626": "IL", "627": "IL", "628": "IL", "629": "IL",
    "630": "MO", "631": "MO", "633": "MO", "634": "MO", "635": "MO", "636": "MO",
    "637": "MO", "638": "MO", "639": "MO", "640": "MO", "641": "MO", "644": "MO",
    "645": "MO", "646": "MO", "647": "MO", "648": "MO", "649": "MO", "650": "MO",
    "651": "MO", "652": "MO", "653": "MO", "654": "MO", "655": "MO", "656": "MO",
    "657": "MO", "658": "MO",
    "660": "KS", "661": "KS", "662": "KS", "664": "KS", "665": "KS", "666": "KS",
    "667": "KS", "668": "KS", "669": "KS", "670": "KS", "671": "KS", "672": "KS",
    "673": "KS", "674": "KS", "675": "KS", "676": "KS", "677": "KS", "678": "KS",
    "679": "KS",
    "680": "NE", "681": "NE", "683": "NE", "684": "NE", "685": "NE", "686": "NE",
    "687": "NE", "688": "NE", "689": "NE", "690": "NE", "691": "NE", "692": "NE",
    "693": "NE",
    "700": "LA", "701": "LA", "703": "LA", "704": "LA", "705": "LA", "706": "LA",
    "707": "LA", "708": "LA", "710": "LA", "711": "LA", "712": "LA", "713": "LA",
    "714": "LA",
    "716": "AR", "717": "AR", "718": "AR", "719": "AR", "720": "AR", "721": "AR",
    "722": "AR", "723": "AR", "724": "AR", "725": "AR", "726": "AR", "727": "AR",
    "728": "AR", "729": "AR",
    "730": "OK", "731": "OK", "734": "OK", "735": "OK", "736": "OK", "737": "OK",
    "738": "OK", "739": "OK", "740": "OK", "741": "OK", "743": "OK", "744": "OK",
    "745": "OK", "746": "OK", "747": "OK", "748": "OK", "749": "OK",
    "750": "TX", "751": "TX", "752": "TX", "753": "TX", "754": "TX", "755": "TX",
    "756": "TX", "757": "TX", "758": "TX", "759": "TX", "760": "TX", "761": "TX",
    "762": "TX", "763": "TX", "764": "TX", "765": "TX", "766": "TX", "767": "TX",
    "768": "TX", "769": "TX", "770": "TX", "771": "TX", "772": "TX", "773": "TX",
    "774": "TX", "775": "TX", "776": "TX", "777": "TX", "778": "TX", "779": "TX",
    "780": "TX", "781": "TX", "782": "TX", "783": "TX", "784": "TX", "785": "TX",
    "786": "TX", "787": "TX", "788": "TX", "789": "TX", "790": "TX", "791": "TX",
    "792": "TX", "793": "TX", "794": "TX", "795": "TX", "796": "TX", "797": "TX",
    "798": "TX", "799": "TX",
    "800": "CO", "801": "CO", "802": "CO", "803": "CO", "804": "CO", "805": "CO",
    "806": "CO", "807": "CO", "808": "CO", "809": "CO", "810": "CO", "811": "CO",
    "812": "CO", "813": "CO", "814": "CO", "815": "CO", "816": "CO",
    "820": "WY", "821": "WY", "822": "WY", "823": "WY", "824": "WY", "825": "WY",
    "826": "WY", "827": "WY", "828": "WY", "829": "WY", "830": "WY", "831": "WY",
    "832": "ID", "833": "ID", "834": "ID", "835": "ID", "836": "ID", "837": "ID",
    "838": "ID",
    "840": "UT", "841": "UT", "842": "UT", "843": "UT", "844": "UT", "845": "UT",
    "846": "UT", "847": "UT",
    "850": "AZ", "851": "AZ", "852": "AZ", "853": "AZ", "855": "AZ", "856": "AZ",
    "857": "AZ", "858": "AZ", "859": "AZ", "860": "AZ",
    "870": "NM", "871": "NM", "872": "NM", "873": "NM", "874": "NM", "875": "NM",
    "877": "NM", "878": "NM", "879": "NM", "880": "NM", "881": "NM", "882": "NM",
    "883": "NM", "884": "NM",
    "889": "NV", "890": "NV", "891": "NV", "893": "NV", "894": "NV", "895": "NV",
    "897": "NV", "898": "NV",
    "900": "CA", "901": "CA", "902": "CA", "903": "CA", "904": "CA", "905": "CA",
    "906": "CA", "907": "CA", "908": "CA", "910": "CA", "911": "CA", "912": "CA",
    "913": "CA", "914": "CA", "915": "CA", "916": "CA", "917": "CA", "918": "CA",
    "919": "CA", "920": "CA", "921": "CA", "922": "CA", "923": "CA", "924": "CA",
    "925": "CA", "926": "CA", "927": "CA", "928": "CA", "930": "CA", "931": "CA",
    "932": "CA", "933": "CA", "934": "CA", "935": "CA", "936": "CA", "937": "CA",
    "938": "CA", "939": "CA", "940": "CA", "941": "CA", "943": "CA", "944": "CA",
    "945": "CA", "946": "CA", "947": "CA", "948": "CA", "949": "CA", "950": "CA",
    "951": "CA", "952": "CA", "953": "CA", "954": "CA", "955": "CA", "956": "CA",
    "957": "CA", "958": "CA", "959": "CA", "960": "CA", "961": "CA",
    "967": "HI", "968": "HI",
    "970": "OR", "971": "OR", "972": "OR", "973": "OR", "974": "OR", "975": "OR",
    "976": "OR", "977": "OR", "978": "OR", "979": "OR",
    "980": "WA", "981": "WA", "982": "WA", "983": "WA", "984": "WA", "985": "WA",
    "986": "WA", "988": "WA", "989": "WA", "990": "WA", "991": "WA", "992": "WA",
    "993": "WA", "994": "WA",
    "995": "AK", "996": "AK", "997": "AK", "998": "AK", "999": "AK",
}


def zip_to_state(zip_code: str) -> str | None:
    """Resolve a ZIP code to a 2-letter state code."""
    prefix = zip_code[:3]
    return _ZIP_PREFIX_TO_STATE.get(prefix)


# Income range midpoints for comparison against thresholds
_INCOME_MIDPOINTS: dict[str, float] = {
    "under_25k": 20_000,
    "under_30k": 20_000,
    "25k-50k": 37_500,
    "30k_50k": 40_000,
    "50k-75k": 62_500,
    "50k_75k": 62_500,
    "75k-100k": 87_500,
    "75k_100k": 87_500,
    "100k-150k": 125_000,
    "100k_150k": 125_000,
    "150k-200k": 175_000,
    "150k_200k": 175_000,
    "200k-300k": 250_000,
    "200k_300k": 250_000,
    "over_300k": 350_000,
}


def _parse_income(income_range: str | None) -> float | None:
    """Return approximate income from a range string."""
    if not income_range:
        return None
    return _INCOME_MIDPOINTS.get(income_range)


def _zip_matches(zip_code: str, eligible_zips: list[str]) -> bool:
    """Check if a ZIP code matches a list of ZIPs or ZIP prefixes (e.g. '920*')."""
    for pattern in eligible_zips:
        if pattern.endswith("*"):
            if zip_code.startswith(pattern[:-1]):
                return True
        elif zip_code == pattern:
            return True
    return False


def filter_by_geography(incentives: list[IncentiveProgram], zip_code: str) -> list[IncentiveProgram]:
    """Filter incentives by geographic eligibility."""
    state = zip_to_state(zip_code)
    result = []
    for inc in incentives:
        scope = inc.geographic_scope
        if scope == "national":
            result.append(inc)
        elif scope == "state" and state and inc.eligible_states and state in inc.eligible_states:
            result.append(inc)
        elif scope == "zip" and inc.eligible_zips and _zip_matches(zip_code, inc.eligible_zips):
            result.append(inc)
        elif scope == "county":
            if inc.eligible_zips and _zip_matches(zip_code, inc.eligible_zips):
                result.append(inc)
            elif state and inc.eligible_states and state in inc.eligible_states:
                result.append(inc)
        elif scope == "utility_territory":
            if inc.eligible_zips and _zip_matches(zip_code, inc.eligible_zips):
                result.append(inc)
            # If no ZIPs defined, do NOT fall back to state — utility programs
            # are specific to a service area and should not match broadly
    return result


def filter_by_vehicle(incentives: list[IncentiveProgram], vehicle: dict) -> list[IncentiveProgram]:
    """Filter incentives by vehicle criteria (fuel type, make/model, MSRP cap, new/used)."""
    if not vehicle:
        return incentives

    result = []
    v_fuel = vehicle.get("fuel_type", "").upper() if vehicle.get("fuel_type") else None
    v_make = vehicle.get("make", "").lower() if vehicle.get("make") else None
    v_model = vehicle.get("model", "").lower() if vehicle.get("model") else None
    v_msrp = vehicle.get("msrp")
    v_new_used = vehicle.get("new_or_used", "").lower() if vehicle.get("new_or_used") else None

    for inc in incentives:
        criteria = inc.vehicle_criteria or {}
        if not criteria:
            result.append(inc)
            continue

        # Skip charger installation programs when searching for a vehicle
        if criteria.get("category") == "charger_installation":
            continue

        # Fuel type check
        fuel_types = criteria.get("fuel_types", [])
        if fuel_types and v_fuel and v_fuel not in [ft.upper() for ft in fuel_types]:
            continue
        # If user specified a non-EV fuel type, exclude EV-only programs
        if fuel_types and v_fuel and v_fuel == "ICE" and all(ft.upper() in ("BEV", "PHEV", "FCEV") for ft in fuel_types):
            continue
        # If user didn't specify fuel type but we know the make/model is ICE-only, still show EV programs
        # (user might be considering an EV version) — so no additional filtering here

        # Make check
        makes = criteria.get("make", [])
        if makes:
            # Normalize: "make" can be a string or list in seed data
            if isinstance(makes, str):
                makes = [makes]
            if v_make and v_make not in [m.lower() for m in makes]:
                continue

        # Model check (seed data uses "models" plural)
        models = criteria.get("models", criteria.get("model", []))
        if models:
            if isinstance(models, str):
                models = [models]
            if v_model and v_model not in [m.lower() for m in models]:
                continue

        # MSRP cap check
        msrp_cap = criteria.get("msrp_cap")
        if msrp_cap is not None and v_msrp is not None and float(v_msrp) > float(msrp_cap):
            continue

        # New/used check
        new_used_req = criteria.get("new_or_used")
        if new_used_req and v_new_used and new_used_req.lower() != "both" and new_used_req.lower() != v_new_used:
            continue

        result.append(inc)
    return result


def filter_by_buyer(incentives: list[IncentiveProgram], buyer_profile: dict) -> list[IncentiveProgram]:
    """Filter incentives by buyer criteria (income, filing status, affinity groups)."""
    if not buyer_profile:
        return incentives

    result = []
    buyer_income = _parse_income(buyer_profile.get("income_range"))
    buyer_filing = buyer_profile.get("filing_status")
    buyer_affinity = set(g.lower() for g in buyer_profile.get("affinity_groups", []))
    buyer_has_trade = buyer_profile.get("has_trade_in", False)

    for inc in incentives:
        criteria = inc.buyer_criteria or {}
        if not criteria:
            result.append(inc)
            continue

        # Income check
        income_max = criteria.get("income_max")
        if income_max is not None and buyer_income is not None:
            # Check filing-status-specific limits first
            filing_limits = criteria.get("filing_status_limits", {})
            if buyer_filing and filing_limits and buyer_filing in filing_limits:
                limit = float(filing_limits[buyer_filing])
            else:
                limit = float(income_max)
            if buyer_income > limit:
                continue

        # Trade-in / scrap requirement
        if criteria.get("trade_in_required") and not buyer_has_trade:
            continue
        if criteria.get("scrap_required") and not buyer_has_trade:
            continue

        # Affinity group requirement
        required_affinity = criteria.get("affinity_group")
        if required_affinity and required_affinity.lower() not in buyer_affinity:
            continue

        # Conquest/competitive owner requirement — only show if user indicated they're switching
        conquest_type = criteria.get("conquest_type")
        if conquest_type and not buyer_profile.get("conquest_type"):
            continue

        # Captive financing / lease-only — show but don't block (informational)
        # (we don't filter on these since any buyer could choose to finance through captive)

        result.append(inc)
    return result


def resolve_stacking(candidates: list[IncentiveProgram]) -> list[IncentiveProgram]:
    """Handle mutual exclusions and choose the financially optimal combination.

    For each set of mutually exclusive incentives, pick the one with the highest value.
    All non-exclusive incentives are always included.
    """
    if not candidates:
        return []

    id_to_inc: dict[uuid.UUID, IncentiveProgram] = {inc.id: inc for inc in candidates}
    candidate_ids = set(id_to_inc.keys())

    # Build mutual exclusion groups
    # Each group is a frozenset of IDs that are mutually exclusive with each other
    exclusion_pairs: list[tuple[uuid.UUID, uuid.UUID]] = []
    for inc in candidates:
        if inc.mutually_exclusive_with:
            for exc_id in inc.mutually_exclusive_with:
                if isinstance(exc_id, str):
                    exc_id = uuid.UUID(exc_id)
                if exc_id in candidate_ids:
                    pair = tuple(sorted([inc.id, exc_id], key=str))
                    if pair not in exclusion_pairs:
                        exclusion_pairs.append(pair)

    if not exclusion_pairs:
        return candidates

    # Build connected components of mutually exclusive groups
    parent: dict[uuid.UUID, uuid.UUID] = {}

    def find(x: uuid.UUID) -> uuid.UUID:
        if x not in parent:
            parent[x] = x
        while parent[x] != x:
            grandparent = parent.get(parent[x], parent[x])
            parent[x] = grandparent
            x = parent[x]
        return x

    def union(a: uuid.UUID, b: uuid.UUID) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    involved_ids: set[uuid.UUID] = set()
    for a, b in exclusion_pairs:
        union(a, b)
        involved_ids.add(a)
        involved_ids.add(b)

    # Group by connected component
    groups: dict[uuid.UUID, list[IncentiveProgram]] = {}
    for iid in involved_ids:
        root = find(iid)
        groups.setdefault(root, []).append(id_to_inc[iid])

    # Non-exclusive incentives
    result = [inc for inc in candidates if inc.id not in involved_ids]

    # For each exclusive group, pick the one with the highest computed value
    for group in groups.values():
        best = max(group, key=lambda i: _quick_value(i))
        result.append(best)

    return result


def _quick_value(inc: IncentiveProgram) -> float:
    """Quick dollar value estimate for stacking comparison."""
    if inc.incentive_value_type == "fixed" and inc.incentive_amount:
        return float(inc.incentive_amount)
    if inc.incentive_value_type == "tax_credit" and inc.incentive_amount:
        return float(inc.incentive_amount)
    if inc.incentive_value_type == "percentage" and inc.incentive_percentage:
        max_amt = float(inc.incentive_max_amount) if inc.incentive_max_amount else 50_000 * float(inc.incentive_percentage) / 100
        return max_amt
    if inc.incentive_value_type == "rate_reduction":
        # Approximate savings vs 6.5% market rate on a $35k loan over 60 months
        offered_rate = float(inc.incentive_percentage) if inc.incentive_percentage is not None else 0
        rate_savings = 6.5 - offered_rate
        return max(0, 35_000 * rate_savings / 100 * 5 / 2)
    return float(inc.incentive_amount) if inc.incentive_amount else 0


def compute_value(incentive: IncentiveProgram, vehicle: dict) -> float:
    """Calculate the actual dollar value of an incentive for a given vehicle."""
    vtype = incentive.incentive_value_type

    if vtype == "fixed":
        return float(incentive.incentive_amount) if incentive.incentive_amount else 0

    if vtype == "tax_credit":
        return float(incentive.incentive_amount) if incentive.incentive_amount else 0

    if vtype == "percentage":
        pct = float(incentive.incentive_percentage) if incentive.incentive_percentage else 0
        base_price = vehicle.get("msrp") or vehicle.get("price") or 0
        value = float(base_price) * pct / 100
        if incentive.incentive_max_amount:
            value = min(value, float(incentive.incentive_max_amount))
        return value

    if vtype == "rate_reduction":
        offered_rate = float(incentive.incentive_percentage) if incentive.incentive_percentage is not None else 0
        market_rate = 6.5  # current average new car loan rate
        rate_savings = market_rate - offered_rate
        if rate_savings <= 0:
            return 0
        loan_amount = vehicle.get("msrp") or vehicle.get("price") or 35_000
        # Approximate interest savings over 60-month loan (simple interest approximation)
        return round(float(loan_amount) * rate_savings / 100 * 5 / 2, 2)

    return float(incentive.incentive_amount) if incentive.incentive_amount else 0


def generate_disclaimers(incentives: list[IncentiveProgram]) -> list[str]:
    """Produce warnings for low-confidence data, funding status issues, expiring programs."""
    disclaimers: list[str] = []
    now = datetime.now(timezone.utc)
    sixty_days = now + timedelta(days=60)

    for inc in incentives:
        if inc.confidence_score < 0.8:
            disclaimers.append(
                f"'{inc.name}' data has not been recently verified (confidence: {inc.confidence_score:.0%}). "
                f"Please verify at {inc.source_url}."
            )
        if inc.funding_status in ("waitlisted", "depleted", "suspended"):
            disclaimers.append(
                f"'{inc.name}' funding status is '{inc.funding_status}'. This incentive may not be available."
            )
        if inc.end_date and inc.end_date <= sixty_days:
            days_left = (inc.end_date - now).days
            if days_left > 0:
                disclaimers.append(
                    f"'{inc.name}' expires in {days_left} days. Act quickly to secure this incentive."
                )
            elif days_left <= 0:
                disclaimers.append(
                    f"'{inc.name}' has expired or is expiring today."
                )

    if not incentives:
        disclaimers.append("No matching incentives found for this combination.")

    return disclaimers


async def match_incentives(
    db: AsyncSession,
    zip_code: str,
    vehicle_interest: dict,
    buyer_profile: dict,
) -> dict[str, Any]:
    """Main entry point: match incentives for a buyer/vehicle/location combination.

    Returns dict with incentives, total_savings, confidence, disclaimers.
    """
    # Sources that are generic/unreliable and should not be shown to users
    BLOCKED_SOURCES = {"https://www.marketcheck.com", "https://www.marketcheck.com/"}

    # Load all active, non-expired incentives from the DB
    now = datetime.now(timezone.utc)
    stmt = select(IncentiveProgram).where(
        IncentiveProgram.is_active.is_(True),
        IncentiveProgram.funding_status.in_(["open", "waitlisted"]),
        or_(IncentiveProgram.end_date.is_(None), IncentiveProgram.end_date > now),
    )
    result = await db.execute(stmt)
    all_incentives = [
        inc for inc in result.scalars().all()
        if inc.source_url not in BLOCKED_SOURCES
    ]

    # Filter pipeline
    candidates = filter_by_geography(all_incentives, zip_code)
    candidates = filter_by_vehicle(candidates, vehicle_interest)
    candidates = filter_by_buyer(candidates, buyer_profile)

    # Stacking resolver
    optimal_stack = resolve_stacking(candidates)

    # Compute values
    incentive_results = []
    total_savings = 0.0
    for inc in optimal_stack:
        value = compute_value(inc, vehicle_interest)
        total_savings += value
        incentive_results.append({
            "id": str(inc.id),
            "name": inc.name,
            "type": inc.type,
            "amount": round(value, 2),
            "claim_mechanism": inc.claim_mechanism,
            "confidence_score": inc.confidence_score,
            "source_url": inc.source_url,
            "funding_status": inc.funding_status,
            "end_date": inc.end_date.isoformat() if inc.end_date else None,
            "last_verified": inc.last_verified.isoformat() if inc.last_verified else None,
            "eligible_purchase_types": getattr(inc, "eligible_purchase_types", None) or ["cash", "finance", "lease"],
            "claim_steps": inc.claim_steps or [],
        })

    confidence = min((i.confidence_score for i in optimal_stack), default=0)
    disclaimers = generate_disclaimers(optimal_stack)

    return {
        "incentives": incentive_results,
        "total_savings": round(total_savings, 2),
        "confidence": confidence,
        "disclaimers": disclaimers,
    }


async def match_incentives_simple(
    zip_code: str,
    vehicle_interest: dict,
    buyer_profile: dict,
) -> dict[str, Any]:
    """Non-DB version for use in tests or when DB is unavailable. Operates on provided lists."""
    return {
        "incentives": [],
        "total_savings": 0,
        "confidence": 0,
        "disclaimers": ["No incentive data available."],
    }
