"""Devices abstraction."""
from .base_interface import BaseInterface
from .utility import Utility


class Devices(BaseInterface):
    """This object covers devices tracked in the Kismet DB.


    Unlike other abstractions which contain the object detail under the `json`
    key, this abstraction contains the details under the key named `device`

    Args:
        file_location (str): Path to Kismet log file.

    Keyword args:
        first_time_lt (str, datetime.datetime): Match devices where the first
            observation timestamp is before this time.
        first_time_gt (str, datetime.datetime): Match devices where the first
            observation timestamp is after this time.
        last_time_lt (str, datetime.datetime): Match devices where the most
            recent observation timestamp is before this time.
        last_time_gt (str, datetime.datetime): Match devices where the most
            recent observation timestamp is after this time.
        devkey (str, list): Exact match for this devkey.
        phyname (str, list): Exact match for this phyname.
        devmac (str, list): Exact match for this device MAC.
        type (str, list): Exact match for this device type.
        strongest_signal_gt (str, int): Match devices where the strongest
            signal is greater than the integer representation of this string.
        strongest_signal_lt (str, int): Match devices where the strongest
            signal is less than the integer representation of this string.
        bytes_data_gt (str, int): Match devices where we've seen at least this
            many bytes of data (converted to int).
        bytes_data_lt (str, int): Match devices where we've seen at most this
            many bytes of data (converted to int).

    Attributes:
        bulk_data_field (str): Field containing bulk data (typically stored
            as a blob in the DB). This allows the `get_meta()` method to
            exclude information which may have a performance impact. This
            is especially true for the retrieval of packet captures.
        column_names (str): Name of columns expected to be in table represented
            by this abstraction. Used for validation against columns in
            DB on instanitation. This is constructed on instantiation, based
            on the version of DB that's detected.
        table_name (str): Name of the table this abstraction represents.
        valid_kwargs (str): This is a dictionary where the key is the name
            of a keyword argument and the value is a reference to the function
            which builds the SQL partial and replacement dictionary.
        field_defaults (dict): Statically set these column defaults by DB
            version.
        converters_reference (dict): This provides a reference for converters
            to use on data coming from the DB on a version by version basis.
        full_query_column_names (list): Processed column names for full query
            of kismet DB. Created on instantiation.
        meta_query_column_names (list): Processed column names for meta query
            of kismet DB. Created on instantiation.

    """

    table_name = "devices"
    bulk_data_field = "device"
    field_defaults = {4: {},
                      5: {}}
    converters_reference = {4: {"device": Utility.device_field_parser,
                                "min_lat": Utility.format_int_as_latlon,
                                "min_lon": Utility.format_int_as_latlon,
                                "max_lat": Utility.format_int_as_latlon,
                                "max_lon": Utility.format_int_as_latlon,
                                "avg_lat": Utility.format_int_as_latlon,
                                "avg_lon": Utility.format_int_as_latlon},
                            5: {"device": Utility.device_field_parser}}
    column_reference = {4: ["first_time", "last_time", "devkey", "phyname",
                            "devmac", "strongest_signal", "min_lat", "min_lon",
                            "max_lat", "max_lon", "avg_lat", "avg_lon",
                            "bytes_data", "type", "device"],
                        5: ["first_time", "last_time", "devkey", "phyname",
                            "devmac", "strongest_signal", "min_lat", "min_lon",
                            "max_lat", "max_lon", "avg_lat", "avg_lon",
                            "bytes_data", "type", "device"]}
    valid_kwargs = {"first_time_lt": Utility.generate_single_tstamp_secs_lt,
                    "first_time_gt": Utility.generate_single_tstamp_secs_gt,
                    "last_time_lt": Utility.generate_single_tstamp_secs_lt,
                    "last_time_gt": Utility.generate_single_tstamp_secs_gt,
                    "devkey": Utility.generate_multi_string_sql_eq,
                    "phyname": Utility.generate_multi_string_sql_eq,
                    "devmac": Utility.generate_multi_string_sql_eq,
                    "type": Utility.generate_multi_string_sql_eq,
                    "strongest_signal_lt": Utility.generate_single_int_sql_lt,
                    "strongest_signal_gt": Utility.generate_single_int_sql_gt,
                    "bytes_data_lt": Utility.generate_single_int_sql_lt,
                    "bytes_data_gt": Utility.generate_single_int_sql_gt}
