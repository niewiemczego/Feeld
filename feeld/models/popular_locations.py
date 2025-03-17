from dataclasses import dataclass
from enum import Enum


class PopularCountry(str, Enum):
    NL = "NL"
    US = "US"
    ES = "ES"
    DE = "DE"
    DK = "DK"
    GB = "GB"
    AU = "AU"
    MX = "MX"
    FR = "FR"
    SG = "SG"
    BR = "BR"
    CA = "CA"


@dataclass(frozen=True)
class PopularLocation:
    city: str
    country: PopularCountry | None = None
    latitude: float | None = None
    longitude: float | None = None


class PopularLocations(Enum):
    AMSTERDAM = PopularLocation("Amsterdam", PopularCountry.NL, 52.36658782373665, 4.902928455066088)
    AUSTIN = PopularLocation("Austin", PopularCountry.US, 30.26793198512474, -97.74751340505709)
    BARCELONA = PopularLocation("Barcelona", PopularCountry.ES, 41.387487171006704, 2.164905972684016)
    BERLIN = PopularLocation("Berlin", PopularCountry.DE, 52.51926602857233, 13.404811259698603)
    BOSTON = PopularLocation("Boston", PopularCountry.US, 42.36092759668448, -71.065050348655)
    CHICAGO = PopularLocation("Chicago", PopularCountry.US, 41.87964342194048, -87.64339636599814)
    COPENHAGEN = PopularLocation("Copenhagen", PopularCountry.DK, 55.67358283615867, 12.600645579662626)
    LAS_VEGAS = PopularLocation("Las Vegas", PopularCountry.US, 36.173388138080576, -115.1572187561562)
    LONDON = PopularLocation("London", PopularCountry.GB, 51.50972643807486, -0.1311323644745516)
    LOS_ANGELES = PopularLocation("Los Angeles", PopularCountry.US, 34.05873073533446, -118.20578013598234)
    MELBOURNE = PopularLocation("Melbourne", PopularCountry.AU, -37.81062509887025, 144.94323097803917)
    MEXICO_CITY = PopularLocation("Mexico City", PopularCountry.MX, 19.430164096355526, -99.1346978260841)
    NEW_YORK = PopularLocation("New York", PopularCountry.US, 40.71454818056282, -74.01196320524461)
    PARIS = PopularLocation("Paris", PopularCountry.FR, 48.857244323581426, 2.3559592551731563)
    PORTLAND = PopularLocation("Portland", PopularCountry.US, 45.51710136296455, -122.676382574627)
    SAN_FRANCISCO = PopularLocation("San Francisco", PopularCountry.US, 37.77534968539297, -122.42140478685103)
    SEATTLE = PopularLocation("Seattle", PopularCountry.US, 47.60658809378702, -122.33319211010884)
    SINGAPORE = PopularLocation("Singapore", PopularCountry.SG, 1.3593008858931113, 103.89161526845547)
    SAO_PAULO = PopularLocation("São Paulo", PopularCountry.BR, -23.554078696160513, -46.62584285760229)
    SYDNEY = PopularLocation("Sydney", PopularCountry.AU, -33.864911732176836, 151.20934255705617)
    TORONTO = PopularLocation("Toronto", PopularCountry.CA, 43.65655347425306, -79.3712009634627)
    VANCOUVER = PopularLocation("Vancouver", PopularCountry.CA, 49.282570419921456, -123.12775753618007)
    WASHINGTON_DC = PopularLocation("Washington, DC", PopularCountry.US, 38.90731229380647, -77.03818848366893)
    MIAMI = PopularLocation("Miami", PopularCountry.US, 25.7617, -80.1918)
    STAYING_AT_HOME = PopularLocation("QUARANTINE")
    REMOTE_TRIOS = PopularLocation("THREESOMES")
    FANTASY = PopularLocation("FANTASY_BUNKER")

    @classmethod
    def get_all_locations(cls) -> list[PopularLocation]:
        return [location.value for location in cls]

    @classmethod
    def get_location_by_city(cls, city: str) -> PopularLocation:
        for location in cls:
            if location.value.city.lower() == city.lower():
                return location.value
        raise ValueError(f"No location found for city: {city}")

    @classmethod
    def get_locations_by_country(cls, country: PopularCountry) -> list[PopularLocation]:
        return [location.value for location in cls if location.value.country == country]


if __name__ == "__main__":
    print(PopularLocations.LONDON)
    print(PopularLocations.get_all_locations())
    print(PopularLocations.get_location_by_city("Paris"))
    print(PopularLocations.get_locations_by_country(PopularCountry.US))
