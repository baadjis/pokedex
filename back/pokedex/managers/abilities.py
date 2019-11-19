import requests
from playhouse.shortcuts import model_to_dict

from pokedex.models.pokemon import Ability, Generation, AbilityEffects, VerboseEffect, Language, PokemonAbilities


def load_ability_from_api(name):
    """this function will load pokemon from api to the database
    :parameter name the name of the pokemon"""

    request = requests.get(f'https://pokeapi.co/api/v2/ability/{name}')
    data = request.json()

    generation = Generation.get_or_none(name=data['generation']['name'])
    if generation is None:
        generation = Generation.create(name=data['generation']['name'])

    ability = Ability.get_or_none(name=name)
    if ability is None:
        db_data = {'name': data['name'], 'is_main_series': data['is_main_series'], 'generation': generation}
        ability = Ability.create(**db_data)

    AbilityEffects.delete().where(AbilityEffects.ability == ability).execute()
    for effect in data['effect_entries']:
        verbose_effect = VerboseEffect.get_or_none(short_effect=effect['short_effect'])
        if verbose_effect is None:
            language = Language.get_or_none(name=effect['language']['name'])
            if language is None:
                language = Language.create(name=effect['language']['name'])
            verbose_effect = VerboseEffect.create(effect=effect['effect'], short_effect=effect['short_effect'],
                                                  language=language)
        ability_effect = AbilityEffects.create(ability=ability, effect=verbose_effect)

    return ability


def load_abilities_from_api():
    i = 0

    next_page = 'https://pokeapi.co/api/v2/ability/'
    while next_page is not None:
        request = requests.get(next_page)
        data = request.json()

        next_page = data['next']

        for ability in data['results']:
            load_ability_from_api(ability['name'])
            i += 1

        print(f'{i} abilities loaded.')

    return i


def search_abilities(query=None, limits=None, offset=None):
    if limits == None:
        limits = 10
    if offset == None:
        offset = 0
    abilities = (Ability.select(Ability.id, Ability.name, Ability.is_main_series, Ability.generation)
                 .join(Generation)).order_by(Ability.name).limit(limits).offset(offset)
    if query != None:
        abilities = abilities.where(query in Ability.name)
    if len(abilities) > (limits + offset):
        abilities = abilities.limits(limits).offset(offset)
    data = [dict({"id": ability.id, "name": ability.name, "is_main_series": ability.is_main_series,
                  "generation": ability.generation.name}) for ability in abilities]
    return data


def get_ability_effects(ability_id):
    """ get the  ability effect if given the ability id
    :parameter abylity_id  :the ability id
    """
    effects = (VerboseEffect.select(VerboseEffect.effect)
               .join(AbilityEffects)
               .join(Ability)
               .where(Ability.id == ability_id))
    return [ef.effect for ef in effects]


def add_effects(liste):
    for d in liste:
        d["effects"] = get_ability_effects(d["id"])
    return liste


def filter_ability_by_generation(liste):
    genations = set([d["generation"] for d in liste])
    filtered = {gen: [d for d in liste if (gen == d["generation"])] for gen in genations}
    return filtered
