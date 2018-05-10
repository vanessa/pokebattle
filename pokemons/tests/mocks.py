# pylint: skip-file

POKEAPI_POKEMON_LIST_EXAMPLE = {
    "count": 949,
    "previous": None,
    "results": [
        {
            "url": "https://pokeapi.co/api/v2/pokemon/21/",
            "name": "spearow"
        },
        {
            "url": "https://pokeapi.co/api/v2/pokemon/22/",
            "name": "fearow"
        }
    ]
}

POKEAPI_POKEMON_DATA_EXAMPLE_FIRST = {
    "forms": [
        {
            "url": "https://pokeapi.co/api/v2/pokemon-form/21/",
            "name": "spearow"
        }
    ],
    "stats": [
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/6/",
                "name": "speed"
            },
            "effort": 1,
            "base_stat": 70
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/5/",
                "name": "special-defense"
            },
            "effort": 0,
            "base_stat": 31
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/4/",
                "name": "special-attack"
            },
            "effort": 0,
            "base_stat": 31
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/3/",
                "name": "defense"
            },
            "effort": 0,
            "base_stat": 30
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/2/",
                "name": "attack"
            },
            "effort": 0,
            "base_stat": 60
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/1/",
                "name": "hp"
            },
            "effort": 0,
            "base_stat": 40
        }
    ],
    "name": "spearow",
    "weight": 20,
    "sprites": {
        "back_female": None,
        "back_shiny_female": None,
        "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/21.png",
        "front_female": None,
        "front_shiny_female": None,
        "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/21.png",
        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/21.png",
        "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/21.png"
    },
    "id": 21,
    "order": 30,
    "base_experience": 52
}

POKEAPI_POKEMON_DATA_EXAMPLE_SECOND = {
    "forms": [
        {
            "url": "https://pokeapi.co/api/v2/pokemon-form/22/",
            "name": "fearow"
        }
    ],
    "stats": [
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/6/",
                "name": "speed"
            },
            "effort": 2,
            "base_stat": 100
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/5/",
                "name": "special-defense"
            },
            "effort": 0,
            "base_stat": 31
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/4/",
                "name": "special-attack"
            },
            "effort": 0,
            "base_stat": 31
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/3/",
                "name": "defense"
            },
            "effort": 0,
            "base_stat": 65
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/2/",
                "name": "attack"
            },
            "effort": 0,
            "base_stat": 90
        },
        {
            "stat": {
                "url": "https://pokeapi.co/api/v2/stat/1/",
                "name": "hp"
            },
            "effort": 0,
            "base_stat": 40
        }
    ],
    "name": "fearow",
    "weight": 100,
    "sprites": {
        "back_female": None,
        "back_shiny_female": None,
        "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/22.png",
        "front_female": None,
        "front_shiny_female": None,
        "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/22.png",
        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/22.png",
        "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/22.png"
    },
    "id": 22,
    "order": 30,
    "base_experience": 52
}
