from enum import Enum

class SpAppsEnum(str,Enum):
    ezanalytics = 'ez_analytics/saml','ezanalytics/local/saml'
    ezweb = "ezweb/saml","ezweb/local/saml"

    def __new__(cls, *values):
        obj = str.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

# print(SpAppsEnum('ez_analytics/saml/').name)
