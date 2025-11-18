# Prettymaps OSM in QGIS

<p align="center">
  <img src="https://qgis.org/styleguide/visual/qgis-logo.svg" alt="QGIS Logo" width="200"/>
</p>

Create beautiful, artistic maps in QGIS using OpenStreetMap data with prettymaps-inspired styling. Transform any location worldwide into stunning cartographic visualizations.

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"/>
  <img src="https://img.shields.io/badge/QGIS-3.x-green.svg" alt="QGIS"/>
  <img src="https://img.shields.io/badge/python-3.x-blue.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/OSM-OpenStreetMap-7ebc6f.svg" alt="OSM"/>
</p>

## 🎨 Overview

This QGIS Processing Script applies the aesthetic styling from the popular [prettymaps](https://github.com/marceloprates/prettymaps) Python library directly within QGIS. Style OpenStreetMap data from any location with a beautiful color palette featuring:

- 🏢 **Buildings**: Three-color rotating palette (yellow, orange, red)
- 🌳 **Green Spaces**: Parks, gardens, forests in natural greens
- 💧 **Water Bodies**: Rivers, lakes, bays in soft blue
- 🛣️ **Streets**: Hierarchical road styling with varying widths
- 🅿️ **Plazas & Pedestrian Areas**: Public spaces in cream tones

## ✨ Features

- **Universal Compatibility**: Works with OSM data from any location worldwide
- **Comprehensive Coverage**: Styles 40+ different OSM feature types
- **Easy to Use**: Simple Processing Algorithm with dropdown menus
- **Customizable**: Built on QGIS rule-based rendering for easy tweaking
- **Professional Output**: Publication-ready cartographic styling

## 📋 Requirements

- QGIS 3.x or higher
- QuickOSM plugin (optional, for downloading OSM data)
- OpenStreetMap data (polygon and line layers)

## 🚀 Installation

### Method 1: Add to Processing Scripts

1. Download `style_osm_prettymaps.py`
2. Copy to your QGIS scripts folder:
   - **Windows**: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\scripts`
   - **Mac**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/processing/scripts`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts`
3. Restart QGIS or reload Processing scripts

### Method 2: Create from Script Editor

1. Open QGIS Processing Toolbox (`Processing → Toolbox`)
2. Click the Python icon at the top
3. Select `Create New Script from Template`
4. Replace content with the script
5. Save with a meaningful name

## 📖 Usage

### Step 1: Get OSM Data

#### Option A: Using QuickOSM Plugin
1. Install QuickOSM plugin: `Plugins → Manage and Install Plugins → QuickOSM`
2. Open QuickOSM: `Vector → QuickOSM → QuickOSM`
3. Use the provided Overpass query or build your own
4. Download data for your area of interest

#### Option B: Using Overpass Turbo
1. Visit [Overpass Turbo](https://overpass-turbo.eu/)
2. Use the provided query template (see `overpass_query.xml`)
3. Export as GeoJSON or GPX
4. Load into QGIS

#### Option C: Using Shapefiles
- Use pre-downloaded OSM shapefiles
- Ensure they contain standard OSM tags

### Step 2: Run the Styling Algorithm

1. Open Processing Toolbox: `Processing → Toolbox`
2. Navigate to: `Scripts → Cartography → Style OSM Map (Prettymaps)`
3. Select your **polygon layer** (buildings, parks, water)
4. Select your **line layer** (streets, roads)
5. Click **Run**

### Step 3: Customize (Optional)

- Open Layer Properties to adjust colors
- Modify line widths for different scales
- Add additional rules for specific features
- Export as styled layer file (.qml) for reuse

## 🗺️ Example Overpass Query

```xml
[out:xml][timeout:25];
(
  // Green spaces
  node["landuse"="grass"](around:1100,40.758,-73.9855);
  way["landuse"="grass"](around:1100,40.758,-73.9855);
  relation["landuse"="grass"](around:1100,40.758,-73.9855);
  
  node["leisure"="park"](around:1100,40.758,-73.9855);
  way["leisure"="park"](around:1100,40.758,-73.9855);
  relation["leisure"="park"](around:1100,40.758,-73.9855);
  
  // Water
  node["natural"="water"](around:1100,40.758,-73.9855);
  way["natural"="water"](around:1100,40.758,-73.9855);
  relation["natural"="water"](around:1100,40.758,-73.9855);
  
  // Streets
  way["highway"](around:1100,40.758,-73.9855);
  
  // Buildings
  node["building"](around:1100,40.758,-73.9855);
  way["building"](around:1100,40.758,-73.9855);
  relation["building"](around:1100,40.758,-73.9855);
);
(._;>;);
out body;
```

Replace `40.758,-73.9855` with your coordinates and `1100` with your desired radius in meters.

## 🎨 Styled Features

### Polygon Features
| Feature Type | OSM Tags | Color |
|-------------|----------|-------|
| Green Spaces | `landuse=grass`, `leisure=park`, `leisure=garden` | Light Green (#D0F1BF) |
| Forests | `landuse=forest`, `natural=wood` | Dark Green (#64B96A) |
| Water | `natural=water`, `waterway=river`, `natural=bay` | Light Blue (#a1e3ff) |
| Parking/Plazas | `amenity=parking`, `highway=pedestrian` | Cream (#F2F4CB) |
| Buildings | `building=*` | Yellow/Orange/Red Palette |

### Line Features (Streets)
| Road Type | Width | Color |
|-----------|-------|-------|
| Motorway | 1.2mm | Dark Gray (#2F3737) |
| Primary | 1.0mm | Dark Gray (#2F3737) |
| Secondary | 0.9mm | Dark Gray (#2F3737) |
| Residential | 0.6mm | Dark Gray (#2F3737) |
| Footway | 0.3mm | Dark Gray (#2F3737) |

## 🛠️ Customization

### Modify Colors
Edit the `colors` dictionary in the script:

```python
colors = {
    'background': '#F2F4CB',  # Canvas background
    'green': '#D0F1BF',       # Parks and green spaces
    'forest': '#64B96A',      # Forests
    'water': '#a1e3ff',       # Water bodies
    'streets': '#2F3737',     # All streets
    'building_palette': ['#FFC857', '#E9724C', '#C5283D'],  # Buildings
    'edge': '#2F3737'         # Outline color
}
```

### Add New Feature Types
Extend the filter conditions in `style_polygons()` or `style_lines()`:

```python
# Add new green space types
green_conditions = [
    '"landuse" = \'grass\'',
    '"leisure" = \'park\'',
    '"your_tag" = \'your_value\''  # Add your custom tag
]
```

## 📚 Resources

- [Prettymaps Original Project](https://github.com/marceloprates/prettymaps)
- [OpenStreetMap Wiki](https://wiki.openstreetmap.org/)
- [Overpass API Documentation](https://wiki.openstreetmap.org/wiki/Overpass_API)
- [QGIS Processing Framework](https://docs.qgis.org/latest/en/docs/user_manual/processing/index.html)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Some ideas:

- Additional color schemes
- More OSM feature types
- Export templates for different scales
- Batch processing capabilities
- Integration with other mapping styles

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [prettymaps](https://github.com/marceloprates/prettymaps) by Marcelo Prates
- Built with [QGIS](https://qgis.org/)
- Data from [OpenStreetMap](https://www.openstreetmap.org/) contributors

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

**Made with ❤️ for the QGIS and OpenStreetMap communities**
