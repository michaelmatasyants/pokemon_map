import folium

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.timezone import localtime
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_image_url(request: HttpRequest, pokemon: Pokemon) -> str:
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)
    return DEFAULT_IMAGE_URL


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = localtime()
    pokemon_entities = PokemonEntity.objects.select_related('pokemon').exclude(
        appeared_at__gt=now).exclude(disappeared_at__lte=now)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_image_url(request, pokemon_entity.pokemon),
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': get_image_url(request, pokemon),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    now = localtime()
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    pokemon_entities = PokemonEntity.objects.select_related(
        'pokemon').filter(pokemon=requested_pokemon).exclude(
        disappeared_at__lte=now).exclude(appeared_at__gt=now)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_image_url(request, pokemon_entity.pokemon),
        )

    previous_evolution, next_evolution = {}, {}
    if previous_evolution_pokemon := requested_pokemon.previous_evolutions.first():
        previous_evolution = {
            'title_ru': previous_evolution_pokemon.title,
            'pokemon_id': previous_evolution_pokemon.id,
            'img_url': previous_evolution_pokemon.image.url,
        }
    if next_evolution_pokemon := requested_pokemon.next_evolution:
        next_evolution = {
            'title_ru': next_evolution_pokemon.title,
            'pokemon_id': next_evolution_pokemon.id,
            'img_url': next_evolution_pokemon.image.url,
        }
    pokemon_on_page = {
        'pokemon_id': requested_pokemon.id,
        'img_url': requested_pokemon.image.url,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'next_evolution': next_evolution,
        'previous_evolution': previous_evolution,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
