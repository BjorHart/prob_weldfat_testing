from input_json import *
import json

import jsonschema




weldfat = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "additionalProperties": False,
    "description": "The root schema comprises the entire JSON document.",
    "oneOf": [
        {
            "required": [
                "serie_data"
            ]
        },
        {
            "required": [
                "stress_data"
            ]
        }
    ],
    "properties": {
        "fatigue_class": {
            "description": "Define S-N curves to be used.",
            "examples": [
                {
                    "class": "User defined",
                    "fat": 100.0,
                    "fat_fact": 1.0,
                    "m_1": 5.0,
                    "m_2": 22.0,
                    "n_c": 10000000.0,
                    "n_fat": 2000000.0
                }
            ],
            "oneOf": [
                {
                    "allOf": [
                        {
                            "required": [
                                "fat"
                            ]
                        },
                        {
                            "required": [
                                "n_fat"
                            ]
                        },
                        {
                            "required": [
                                "n_c"
                            ]
                        },
                        {
                            "required": [
                                "m_1"
                            ]
                        },
                        {
                            "required": [
                                "m_2"
                            ]
                        }
                    ]
                }
            ],
            "properties": {
                "class": {
                    "description": "Specify the S-N curves from the list of available S-N curves",
                    "enum": [
                        "IIW FAT160 steel",
                        "IIW FAT125 steel",
                        "IIW FAT112 steel",
                        "IIW FAT100 steel",
                        "IIW FAT90 steel",
                        "IIW FAT80 steel",
                        "IIW FAT71 steel",
                        "IIW FAT63 steel",
                        "IIW FAT56 steel",
                        "IIW FAT50 steel",
                        "IIW FAT45 steel",
                        "IIW FAT40 steel",
                        "IIW FAT36 steel",
                        "IIW FAT160 steel vari",
                        "IIW FAT125 steel vari",
                        "IIW FAT112 steel vari",
                        "IIW FAT100 steel vari",
                        "IIW FAT90 steel vari",
                        "IIW FAT80 steel vari",
                        "IIW FAT71 steel vari",
                        "IIW FAT63 steel vari",
                        "IIW FAT56 steel vari",
                        "IIW FAT50 steel vari",
                        "IIW FAT45 steel vari",
                        "IIW FAT40 steel vari",
                        "IIW FAT36 steel vari",
                        "IIW FAT71 aluminium",
                        "IIW FAT50 aluminium",
                        "IIW FAT45 aluminium",
                        "IIW FAT40 aluminium",
                        "IIW FAT36 aluminium",
                        "IIW FAT32 aluminium",
                        "IIW FAT28 aluminium",
                        "IIW FAT25 aluminium",
                        "IIW FAT22 aluminium",
                        "IIW FAT18 aluminium",
                        "IIW FAT16 aluminium",
                        "IIW FAT14 aluminium",
                        "IIW FAT12 aluminium",
                        "IIW FAT71 alu vari",
                        "IIW FAT50 alu vari",
                        "IIW FAT45 alu vari",
                        "IIW FAT40 alu vari",
                        "IIW FAT36 alu vari",
                        "IIW FAT32 alu vari",
                        "IIW FAT28 alu vari",
                        "IIW FAT25 alu vari",
                        "IIW FAT22 alu vari",
                        "IIW FAT18 alu vari",
                        "IIW FAT16 alu vari",
                        "IIW FAT14 alu vari",
                        "IIW FAT12 alu vari",
                        "IIW FAT225 R1 steel",
                        "IIW FAT71 R1 aluminium",
                        "IIW FAT28 R1 magnesium",
                        "IIW FAT630 R0.05 steel",
                        "IIW FAT180 R0.05 aluminium",
                        "IIW FAT71 R0.05 magnesium",
                        "IIW FAT225 R1 steel vari",
                        "IIW FAT71 R1 alu vari",
                        "IIW FAT28 R1 magn vari",
                        "IIW FAT630 R0.05 steel vari",
                        "IIW FAT180 R0.05 alu vari",
                        "IIW FAT71 R0.05 magn vari",
                        "DNV T.2-1 B1",
                        "DNV T.2-1 B2",
                        "DNV T.2-1 C",
                        "DNV T.2-1 C1",
                        "DNV T.2-1 C2",
                        "DNV T.2-1 D",
                        "DNV T.2-1 E",
                        "DNV T.2-1 F",
                        "DNV T.2-1 F1",
                        "DNV T.2-1 F3",
                        "DNV T.2-1 G",
                        "DNV T.2-1 W1",
                        "DNV T.2-1 W2",
                        "DNV T.2-1 W3",
                        "DNV T.2-1 T",
                        "DNV (2.4.6) Steel",
                        "DNV T.2-2 B1",
                        "DNV T.2-2 B2",
                        "DNV T.2-2 C",
                        "DNV T.2-2 C1",
                        "DNV T.2-2 C2",
                        "DNV T.2-2 D",
                        "DNV T.2-2 E",
                        "DNV T.2-2 F",
                        "DNV T.2-2 F1",
                        "DNV T.2-2 F3",
                        "DNV T.2-2 G",
                        "DNV T.2-2 W1",
                        "DNV T.2-2 W2",
                        "DNV T.2-2 W3",
                        "DNV T.2-2 T",
                        "DNV T.2-3 B1",
                        "DNV T.2-3 B2",
                        "DNV T.2-3 C",
                        "DNV T.2-3 C1",
                        "DNV T.2-3 C2",
                        "DNV T.2-3 D",
                        "DNV T.2-3 E",
                        "DNV T.2-3 F",
                        "DNV T.2-3 F1",
                        "DNV T.2-3 F3",
                        "DNV T.2-3 G",
                        "DNV T.2-3 W1",
                        "DNV T.2-3 W2",
                        "DNV T.2-3 W3",
                        "DNV T.2-3 T",
                        "EC3 FAT160",
                        "EC3 FAT140",
                        "EC3 FAT125",
                        "EC3 FAT112",
                        "EC3 FAT100",
                        "EC3 FAT90",
                        "EC3 FAT80",
                        "EC3 FAT71",
                        "EC3 FAT63",
                        "EC3 FAT56",
                        "EC3 FAT50",
                        "EC3 FAT45",
                        "EC3 FAT40",
                        "EC3 FAT36",
                        "EC3 FAT160 vari",
                        "EC3 FAT140 vari",
                        "EC3 FAT125 vari",
                        "EC3 FAT112 vari",
                        "EC3 FAT100 vari",
                        "EC3 FAT90 vari",
                        "EC3 FAT80 vari",
                        "EC3 FAT71 vari",
                        "EC3 FAT63 vari",
                        "EC3 FAT50 vari",
                        "EC3 FAT45 vari",
                        "EC3 FAT40 vari",
                        "EC3 FAT36 vari"
                    ],
                    "examples": [
                        "IIW FAT160 steel"
                    ],
                    "title": "The Fatclass Schema",
                    "type": "string"
                },
                "fat": {
                    "$id": "#/properties/fatigue_class/properties/fat",
                    "type": ["object","number"],
                    "title": "The fat schema",
                    "description": "An explanation about the purpose of this instance.",
                    "examples":
                        [
                            100
                        ],
                    "additionalItems": False,
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False
                            }
                        ]
                },
                "fat_fact": {
                    "description": "Scale factor for FAT value. E.g. to apply a thickness or temperature modification factor",
                    "examples": [
                        1.0
                    ],
                    "title": "The fat_fact Schema",
                    "type": ["number","object"],
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False
                            }
                        ]
                },
                "m_1": {
                    "description": "S-N curve slope for N < n_c. (IIW: Default = 5 for Nominal)",
                    "examples": [
                        5
                    ],
                    
                    "title": "The M1 Schema",
                    "type": ["number","object"],
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False
                            }
                        ]

                },
                "m_2": {
                    "description": "S-N curve slope for N > n_c. (IIW: Default = 22)",
                    "examples": [
                        22
                    ],
                    "title": "The M2 Schema",
                    "type": ["number","object"],
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False
                            }
                        ]
                },
                "n_c": {
                    "description": "Break point between slope m_1 and m_2. (IIW: Default = 10e6 cycles.)",
                    "examples": [
                        10000000
                    ],
                    "type": ["number","object"],
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False
                            }
                        ]
                },
                "n_fat": {
                    "description": "Number of cycles for defining FAT. (IIW: Default = 2e6 cycles.)",
                    "examples": [
                        2000000
                    ],
                    "type": ["number","object"],
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False
                            }
                        ]
                }
            },
            "title": "The fatigue_class Schema",
            "type": "object"
        },
        "mean_stress_theory": {
            "additionalProperties": False,
            "description": "Specify mean stress theory",
            "oneOf": [
                {
                    "properties": {
                        "theory": {
                            "enum": [
                                "Goodman",
                                "Gerber"
                            ]
                        }
                    },
                    "required": [
                        "ultimate_limit"
                    ]
                },
                {
                    "properties": {
                        "theory": {
                            "enum": [
                                "Soderberg"
                            ]
                        }
                    },
                    "required": [
                        "yield_limit"
                    ]
                }
            ],
            "properties": {
                "theory": {
                    "description": "Specify mean stress theory",
                    "enum": [
                        "Goodman",
                        "Gerber",
                        "Soderberg"
                    ],
                    "examples": [
                        "Goodman"
                    ],
                    "title": "The theory Schema",
                    "type": "string"
                },
                "ultimate_limit": {
                    "description": "Ultimate limit",
                    "examples": [
                        500
                    ],
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False,
                            "additionalItems":False
                            }
                        ]
                },
                "yield_limit": {
                    "description": "Yield Limit",
                    "examples": [
                        200
                    ],
                    "oneOf": [
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/0",
                            "type": "number",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                100
                            ],
                            "minimum":0
                        },
                        {
                            "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1",
                            "type": "object",
                            "title": "The second anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "examples": [
                                {
                                    "d": "normal",
                                    "m": 100.0,
                                    "sd": 10
                                }
                            ],
                            "required": [
                                "d",
                                "m",
                                "sd"
                            ],
                            "properties": {
                                "d": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/d",
                                    "type": "string",
                                    "title": "The d schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "examples": [
                                        "normal"
                                    ],
                                    "enum":["normal","lognormal","uniform","halfnormal"]
                                    },
                                "m": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/m",
                                    "type": "number",
                                    "title": "The m schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0.0,
                                    "examples": [
                                        100.0
                                    ]
                                },
                                "sd": {
                                    "$id": "#/properties/fatigue_class/properties/fat/items/anyOf/1/properties/sd",
                                    "type": "integer",
                                    "title": "The sd schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": 0,
                                    "minimum":0,
                                    "examples": [
                                        10
                                    ]
                                }
                            },
                            "additionalProperties": False
                            }
                        ]
                }
            },
            "title": "The mean_stress_theory Schema",
            "type": "object"
        },
        "method": {
            "description": "Specify the Weld Fatigue method based on the IIW recommendations",
            "enum": [
                "Nominal Fatigue"
            ],
            "examples": [
                "Nominal Fatigue"
            ],
            "title": "The method Schema",
            "type": "string"
        },
        "serie_data": {
            "additionalProperties": True,
            "description": "An explanation about the purpose of this instan_ce.",
            "examples": [
                {
                    "maxrange": 10.0,
                    "nbins": 3.0,
                    "series": [
                        0.4,
                        0.4220859399104398,
                        0.43617274661485916
                    ]
                }
            ],
            "properties": {
                "maxrange": {
                    "default": 0,
                    "description": "An explanation about the purpose of this instan_ce.",
                    "examples": [
                        10.0
                    ],
                    "title": "The Maxrange Schema",
                    "type": "number"
                },
                "nbins": {
                    "default": 0,
                    "description": "An explanation about the purpose of this instan_ce.",
                    "examples": [
                        3.0
                    ],
                    "title": "The Nbins Schema",
                    "type": "integer"
                },
                "series": {
                    "additionalItems": True,
                    "description": "An explanation about the purpose of this instan_ce.",
                    "examples": [
                        [
                            0.4,
                            0.4220859399104398,
                            0.43617274661485916
                        ]
                    ],
                    "items": {
                        "description": "An explanation about the purpose of this instan_ce.",
                        "examples": [
                            0.4,
                            0.4220859399104398,
                            0.43617274661485916
                        ],
                        "title": "The Items Schema",
                        "type": "number"
                    },
                    "title": "The Series Schema",
                    "type": "array"
                }
            },
            "required": [
                "series"
            ],
            "title": "The serie_data Schema",
            "type": "object"
        },
        "stress_data": {
            "additionalProperties": False,
            "description": "Stress data inputs",
            "examples": [
                {
                    "bin1": {
                        "cycles": 0.38,
                        "rng": 0.5,
                        "sm": 0.11
                    }
                }
            ],
            "patternProperties": {
                "^([0-9]+)+$": {
                    "description": "An explanation about the purpose of this instan_ce.",
                    "examples": [
                        {
                            "cycles": 0.38,
                            "sa": 0.11,
                            "sm": 0.5
                        }
                    ],
                    "properties": {
                        "cycles": {
                            "description": "An explanation about the purpose of this instan_ce.",
                            "examples": [
                                0.38
                            ],
                            "title": "The Cycles Schema",
                            "type": "number"
                        },
                        "rng": {
                            "description": "An explanation about the purpose of this instan_ce.",
                            "examples": [
                                0.5
                            ],
                            "title": "The rng Schema",
                            "type": "number"
                        },
                        "sm": {
                            "description": "An explanation about the purpose of this instan_ce.",
                            "examples": [
                                0.11
                            ],
                            "title": "The Sm Schema",
                            "type": "number"
                        }
                    },
                    "required": [
                        "rng",
                        "cycles"
                    ],
                    "title": "The Bin1 Schema",
                    "type": "object"
                }
            },
            "properties": {
                "/": {}
            },
            "title": "The stress_data Schema",
            "type": "object"
        },
        "stress_unit": {
            "description": "Stress unit for the inputs",
            "enum": [
                "Pa",
                "MPa",
                "psi",
                "ksi"
            ],
            "examples": [
                "MPa"
            ],
            "title": "The stress_unit Schema",
            "type": "string"
        }
    },
    "required": [
        "method",
        "fatigue_class",
        "stress_unit"
    ],
    "title": "The Weld Fatigue Root Schema",
    "type": "object"
}

weldfat_schema = json.dumps(weldfat,indent=4,sort_keys=True)