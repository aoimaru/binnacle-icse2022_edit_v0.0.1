from pqgrams.PQGram import *
from pqgrams.tree import *

class PQ_GramWrapper(object):
    @staticmethod
    def _zhang(me):
        if me["children"]:
            node = Node(me["type"])
            for child in me["children"]:
                node.addkid(PQ_GramWrapper._zhang(child))
            return node
        else:
            return Node(me["type"])
    
    @staticmethod
    def _get_pq_edit_distance(contents_A, contents_B, P, Q):
        tree_A = PQ_GramWrapper._zhang(contents_A); tree_B = PQ_GramWrapper._zhang(contents_B)
        profile_A = Profile(tree_A, P, Q); profile_B = Profile(tree_B, P, Q)
        pq_distance = profile_A.edit_distance(profile_B)
        return pq_distance



def main():
    import pprint
    tarA = {
            "children": [
                {
                    "children": [],
                    "type": "SC-TAR-X"
                },
                {
                    "children": [
                        {
                            "children": [],
                            "type": "BASH-LITERAL"
                        }
                    ],
                    "type": "SC-TAR-STRIP-COMPONENTS"
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
                                            "type": "ABS-MAYBE-PATH",
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
                }
            ],
            "type": "SC-TAR"
        }

    tarB = {
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
                                        },
                                        {
                                            "type": "ABS-PATH-ABSOLUTE",
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

    tarC = {
            "children": [
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
                                            "type": "ABS-MAYBE-PATH",
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
                }
            ],
            "type": "SC-TAR"
        }
    
    tarD = {
            "children": [
                {
                    "children": [],
                    "type": "SC-TAR-X"
                },
                {
                    "children": [
                        {
                            "children": [],
                            "type": "BASH-LITERAL"
                        }
                    ],
                    "type": "SC-TAR-STRIP-COMPONENTS"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
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
                }
            ],
            "type": "SC-TAR"
        }


    zhangA = PQ_GramWrapper._zhang(tarA)
    zhangB = PQ_GramWrapper._zhang(tarB)
    zhangC = PQ_GramWrapper._zhang(tarC)
    zhangD = PQ_GramWrapper._zhang(tarD)
    
    from zss import simple_distance

    sd = simple_distance(zhangA, zhangB)
    print(sd)

    pq = PQ_GramWrapper._get_pq_edit_distance(tarA, tarB, 2, 5)
    print(pq)

    print()

    sd = simple_distance(zhangA, zhangC)
    print(sd)

    pq = PQ_GramWrapper._get_pq_edit_distance(tarA, tarC, 2, 5)
    print(pq)

    print()

    sd = simple_distance(zhangA, zhangD)
    print(sd)

    pq = PQ_GramWrapper._get_pq_edit_distance(tarA, tarD, 2, 5)
    print(pq)


if __name__ == "__main__":
    main()