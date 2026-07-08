"""
Agronomic reference metadata for the 22 crops in the recommendation dataset.

Used to (1) seed the `Crop` table on first boot and (2) enrich the result
page with season / optimal-pH / water-need / tips for the recommended crop.
Values are indicative agronomic guidance, not exact prescriptions.

emoji is a lightweight visual used on the result and history pages.
"""

CROP_INFO = {
    'rice':        {'crop_type': 'Cereal',            'season': 'Kharif',              'optimal_ph': '5.5 - 6.5', 'water_requirement': 'High',     'emoji': '🌾', 'tips': 'Needs standing water and a warm, humid climate; grows best in clayey soils that hold water.'},
    'maize':       {'crop_type': 'Cereal',            'season': 'Kharif',              'optimal_ph': '5.5 - 7.0', 'water_requirement': 'Moderate', 'emoji': '🌽', 'tips': 'Warm-season cereal; requires well-drained fertile soil and moderate, evenly spread rainfall.'},
    'chickpea':    {'crop_type': 'Pulse',             'season': 'Rabi',                'optimal_ph': '6.0 - 7.5', 'water_requirement': 'Low',      'emoji': '🫛', 'tips': 'Cool-season pulse; drought-tolerant. Avoid waterlogging and excess nitrogen.'},
    'kidneybeans': {'crop_type': 'Pulse',             'season': 'Kharif',              'optimal_ph': '5.5 - 6.5', 'water_requirement': 'Moderate', 'emoji': '🫘', 'tips': 'Frost-sensitive legume; prefers well-drained loamy soil and mild temperatures.'},
    'pigeonpeas':  {'crop_type': 'Pulse',             'season': 'Kharif',              'optimal_ph': '5.0 - 7.0', 'water_requirement': 'Low',      'emoji': '🫛', 'tips': 'Deep-rooted and drought-hardy; fixes nitrogen and improves soil health.'},
    'mothbeans':   {'crop_type': 'Pulse',             'season': 'Kharif',              'optimal_ph': '6.0 - 7.5', 'water_requirement': 'Low',      'emoji': '🫘', 'tips': 'Highly drought-resistant; well suited to arid regions and sandy soils.'},
    'mungbean':    {'crop_type': 'Pulse',             'season': 'Kharif',              'optimal_ph': '6.2 - 7.2', 'water_requirement': 'Low',      'emoji': '🫛', 'tips': 'Short-duration pulse that fixes nitrogen; excellent for crop rotation.'},
    'blackgram':   {'crop_type': 'Pulse',             'season': 'Kharif',              'optimal_ph': '6.0 - 7.5', 'water_requirement': 'Moderate', 'emoji': '🫘', 'tips': 'Thrives in warm, humid climates and tolerates a wide range of soils.'},
    'lentil':      {'crop_type': 'Pulse',             'season': 'Rabi',                'optimal_ph': '6.0 - 7.5', 'water_requirement': 'Low',      'emoji': '🫛', 'tips': 'Cool-season pulse; drought-tolerant. Keep soil moist but never waterlogged.'},
    'pomegranate': {'crop_type': 'Fruit',             'season': 'Perennial',           'optimal_ph': '5.5 - 7.0', 'water_requirement': 'Low',      'emoji': '🍎', 'tips': 'Tolerates drought and mild salinity; needs hot, dry summers for sweet fruit.'},
    'banana':      {'crop_type': 'Fruit',             'season': 'Year-round',          'optimal_ph': '6.0 - 7.5', 'water_requirement': 'High',     'emoji': '🍌', 'tips': 'Needs rich, moist soil with high humidity and warmth; protect from frost and wind.'},
    'mango':       {'crop_type': 'Fruit',             'season': 'Perennial',           'optimal_ph': '5.5 - 7.5', 'water_requirement': 'Moderate', 'emoji': '🥭', 'tips': 'Tropical tree; a dry spell aids flowering. Plant in deep, well-drained soil.'},
    'grapes':      {'crop_type': 'Fruit',             'season': 'Perennial',           'optimal_ph': '6.0 - 7.0', 'water_requirement': 'Moderate', 'emoji': '🍇', 'tips': 'Prefers a warm, dry climate and well-drained soil; high humidity invites disease.'},
    'watermelon':  {'crop_type': 'Fruit',             'season': 'Zaid (Summer)',       'optimal_ph': '6.0 - 7.0', 'water_requirement': 'Moderate', 'emoji': '🍉', 'tips': 'Warm-season vine; give it sandy loam, full sun and space to spread.'},
    'muskmelon':   {'crop_type': 'Fruit',             'season': 'Zaid (Summer)',       'optimal_ph': '6.0 - 7.0', 'water_requirement': 'Moderate', 'emoji': '🍈', 'tips': 'Needs warm, dry weather and well-drained sandy loam for sweet fruit.'},
    'apple':       {'crop_type': 'Fruit (Temperate)', 'season': 'Perennial',           'optimal_ph': '5.5 - 6.5', 'water_requirement': 'Moderate', 'emoji': '🍏', 'tips': 'Temperate crop needing winter chilling hours and well-drained loamy soil.'},
    'orange':      {'crop_type': 'Fruit (Citrus)',    'season': 'Perennial',           'optimal_ph': '5.5 - 7.5', 'water_requirement': 'Moderate', 'emoji': '🍊', 'tips': 'Subtropical citrus; needs well-drained soil and protection from frost.'},
    'papaya':      {'crop_type': 'Fruit',             'season': 'Year-round',          'optimal_ph': '6.0 - 7.0', 'water_requirement': 'Moderate', 'emoji': '🫑', 'tips': 'Fast-growing tropical fruit; requires steady warmth and excellent drainage.'},
    'coconut':     {'crop_type': 'Plantation',        'season': 'Perennial',           'optimal_ph': '5.2 - 8.0', 'water_requirement': 'High',     'emoji': '🥥', 'tips': 'Coastal palm; tolerates sandy, saline soils but needs high rainfall or irrigation.'},
    'cotton':      {'crop_type': 'Fiber / Cash Crop', 'season': 'Kharif',              'optimal_ph': '5.8 - 8.0', 'water_requirement': 'Moderate', 'emoji': '☁️', 'tips': 'Warm-season fiber crop; needs a long frost-free period and deep black soil.'},
    'jute':        {'crop_type': 'Fiber',             'season': 'Kharif',              'optimal_ph': '6.0 - 7.5', 'water_requirement': 'High',     'emoji': '🌿', 'tips': 'Requires a warm, humid climate with standing water; grows well on alluvial soil.'},
    'coffee':      {'crop_type': 'Plantation',        'season': 'Perennial',           'optimal_ph': '6.0 - 6.5', 'water_requirement': 'High',     'emoji': '☕', 'tips': 'Shade-loving crop; thrives in cool, humid highlands with rich, well-drained soil.'},
}


def get_crop_info(crop_name):
    """Return the metadata dict for a crop label, or a sensible default."""
    return CROP_INFO.get(
        (crop_name or '').strip().lower(),
        {'crop_type': 'N/A', 'season': 'N/A', 'optimal_ph': 'N/A',
         'water_requirement': 'N/A', 'emoji': '🌱', 'tips': 'No additional information available for this crop.'},
    )
