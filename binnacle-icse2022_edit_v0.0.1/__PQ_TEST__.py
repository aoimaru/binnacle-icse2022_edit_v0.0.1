
import pickle
import pprint
import json
import numpy as np

from libs.files import *
from libs.d2v import *
from pqgrams_wrapper import *
from libs.contents import *
from libs.algorithms import *

import tqdm
from functools import lru_cache
import zlib
import random

from zss import simple_distance


def main():
    DATA_1 = {
        "children": [
            {
                "children": [],
                "type": "SC-APK-F-NO-CACHE"
            },
            {
                "children": [
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:CA-CERTIFICATES"
                    },
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:CURL"
                    },
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:TAR"
                    }
                ],
                "type": "SC-APK-PACKAGES"
            }
        ],
        "type": "SC-APK-ADD"
    }

    DATA_2 = {
        "children": [
            {
                "children": [],
                "type": "SC-APK-F-NO-CACHE"
            },
            {
                "children": [
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:CA-CERTIFICATES"
                    },
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:CURL"
                    },
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:TAR"
                    }
                ],
                "type": "SC-APK-PACKAGES"
            }
        ],
        "type": "SC-APK-ADD"
    }

    DATA_3 = {
        "children": [
            {
                "children": [],
                "type": "SC-APK-F-NO-CACHE"
            },
            {
                "children": [
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:CA-CERTIFICATES"
                    }
                ],
                "type": "SC-APK-PACKAGES"
            }
        ],
        "type": "SC-APK-ADD"
    }

    DATA_4 = {
        "children": [
            {
                "children": [],
                "type": "SC-APK-F-NO-CACHE"
            },
            {
                "children": [
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:CA-CERTIFICATES"
                    },
                    {
                        "children": [],
                        "type": "SC-APK-PACKAGE:TAR"
                    }
                ],
                "type": "SC-APK-PACKAGES"
            }
        ],
        "type": "SC-APK-ADD"
    }

    DATA_5 = {
        "children": [
                {
                    "children": [],
                    "type": "SC-CURL-F-FAIL"
                },
                {
                    "children": [],
                    "type": "SC-CURL-F-LOCATION"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "type": "ABS-EXTENSION-TAR",
                                            "children": []
                                        }
                                    ],
                                    "type": "BASH-LITERAL"
                                }
                            ],
                            "type": "BASH-PATH"
                        }
                    ],
                    "type": "SC-CURL-OUTPUT"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "type": "ABS-PROBABLY-URL",
                                    "children": []
                                },
                                {
                                    "type": "ABS-URL-PROTOCOL-HTTPS",
                                    "children": []
                                }
                            ],
                            "type": "BASH-LITERAL"
                        }
                    ],
                    "type": "SC-CURL-URL"
                }
            ],
            "type": "SC-CURL"
        }

    DATA_6 = {
            "children": [
                {
                    "children": [],
                    "type": "SC-CURL-F-FAIL"
                },
                {
                    "children": [],
                    "type": "SC-CURL-F-LOCATION"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "type": "ABS-EXTENSION-TAR",
                                            "children": []
                                        }
                                    ],
                                    "type": "BASH-LITERAL"
                                }
                            ],
                            "type": "BASH-PATH"
                        }
                    ],
                    "type": "SC-CURL-OUTPUT"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "type": "ABS-PROBABLY-URL",
                                    "children": []
                                },
                                {
                                    "type": "ABS-URL-PROTOCOL-HTTPS",
                                    "children": []
                                }
                            ],
                            "type": "BASH-LITERAL"
                        }
                    ],
                    "type": "SC-CURL-URL"
                }
            ],
            "type": "SC-CURL"
        }



    DATA_5 = {
            "children": [
                {
                    "children": [],
                    "type": "SC-TAR-X"
                },
                {
                    "children": [],
                    "type": "SC-TAR-Z"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "type": "ABS-EXTENSION-TAR",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-PATH-ABSOLUTE",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-MAYBE-PATH",
                                            "children": []
                                        }
                                    ],
                                    "type": "BASH-LITERAL"
                                }
                            ],
                            "type": "BASH-PATH"
                        }
                    ],
                    "type": "SC-TAR-FILE"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "type": "ABS-PATH-ABSOLUTE",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-MAYBE-SRC-DIR",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-USR-SRC-DIR",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-MAYBE-PATH",
                                            "children": []
                                        }
                                    ],
                                    "type": "BASH-LITERAL"
                                }
                            ],
                            "type": "BASH-PATH"
                        }
                    ],
                    "type": "SC-TAR-DIRECTORY"
                },
                {
                    "children": [
                        {
                            "children": [],
                            "type": "BASH-LITERAL"
                        }
                    ],
                    "type": "SC-TAR-STRIP-COMPONENTS"
                }
            ],
            "type": "SC-TAR"
        }
    
    DATA_6 = {
            "children": [
                {
                    "children": [],
                    "type": "SC-TAR-X"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "type": "ABS-EXTENSION-TAR",
                                            "children": []
                                        }
                                    ],
                                    "type": "BASH-LITERAL"
                                }
                            ],
                            "type": "BASH-PATH"
                        }
                    ],
                    "type": "SC-TAR-FILE"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "type": "ABS-MAYBE-PATH",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-PATH-ABSOLUTE",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-MAYBE-SRC-DIR",
                                            "children": []
                                        },
                                        {
                                            "type": "ABS-USR-SRC-DIR",
                                            "children": []
                                        }
                                    ],
                                    "type": "BASH-LITERAL"
                                }
                            ],
                            "type": "BASH-PATH"
                        }
                    ],
                    "type": "SC-TAR-DIRECTORY"
                },
                {
                    "children": [
                        {
                            "children": [],
                            "type": "BASH-LITERAL"
                        }
                    ],
                    "type": "SC-TAR-STRIP-COMPONENTS"
                }
            ],
            "type": "SC-TAR"
        }

    # pq_12 = PQ_GramWrapper._get_pq_edit_distance(DATA_1, DATA_2, 5, 2)
    # print(pq_12)

    # pq_13 = PQ_GramWrapper._get_pq_edit_distance(DATA_1, DATA_3, 5, 2)
    # print(pq_13)

    pq_56 = PQ_GramWrapper._get_pq_edit_distance(DATA_5, DATA_6, 5, 2)
    print(pq_56)


if __name__ == "__main__":
    main()