"""
QGIS Processing Script: Style Rio de Janeiro OSM Layers
Applies custom styling to OSM data from Rio de Janeiro area
Buildings: Grey | Parks/Grass: Light-Dark Green | Water: Pale Blue | Highways: Black variations | Railways: Orange
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsSymbol,
    QgsRuleBasedRenderer,
    QgsProcessingException
)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import Qt, QCoreApplication

class StyleRioOSMAlgorithm(QgsProcessingAlgorithm):
    """
    Processing algorithm to apply custom styling to Rio de Janeiro OSM layers
    """
    
    # Parameter names
    POLYGON_LAYER = 'POLYGON_LAYER'
    LINE_LAYER = 'LINE_LAYER'
    
    def initAlgorithm(self, config=None):
        """
        Define the inputs and outputs of the algorithm
        """
        
        # Input polygon layer (buildings, parks, water, forests)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.POLYGON_LAYER,
                'Polygon Layer (buildings, parks, water, forests)',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        
        # Input line layer (highways, railways)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.LINE_LAYER,
                'Line Layer (highways, railways)',
                [QgsProcessing.TypeVectorLine]
            )
        )
    
    def processAlgorithm(self, parameters, context, feedback):
        """
        Main processing function
        """
        
        # Get input layers
        polygon_layer = self.parameterAsVectorLayer(parameters, self.POLYGON_LAYER, context)
        line_layer = self.parameterAsVectorLayer(parameters, self.LINE_LAYER, context)
        
        if not polygon_layer or not line_layer:
            raise QgsProcessingException('Invalid input layers')
        
        feedback.pushInfo(f'Styling polygon layer: {polygon_layer.name()}')
        feedback.pushInfo(f'Styling line layer: {line_layer.name()}')
        
        # Color definitions matching the QML file
        colors = {
            'grass': (220, 228, 152),        # RGB from QML - Grass
            'park': (218, 224, 160),         # RGB from QML - Park
            'forest': (164, 171, 99),        # RGB from QML - Forest
            'water': (138, 198, 213),        # RGB from QML - Water
            'buildings': (164, 164, 162),    # RGB from QML - Buildings
            'railway': '#FF8C00',            # Orange
            'highway_motorway': '#000000',      # Black
            'highway_primary': '#1a1a1a',       # Very dark grey
            'highway_secondary': '#333333',     # Dark grey
            'highway_tertiary': '#4d4d4d',      # Medium-dark grey
            'highway_residential': '#666666',   # Medium grey
            'highway_service': '#808080',       # Grey
            'highway_footway': '#999999',       # Light grey
            'highway_path': '#b3b3b3'           # Very light grey
        }
        
        # ========== STYLE POLYGON LAYER ==========
        feedback.pushInfo('\n--- Styling Polygons ---')
        self.style_polygons(polygon_layer, colors, feedback)
        
        # ========== STYLE LINE LAYER ==========
        feedback.pushInfo('\n--- Styling Lines ---')
        self.style_lines(line_layer, colors, feedback)
        
        feedback.pushInfo('\n' + '='*50)
        feedback.pushInfo('✓ STYLING COMPLETE!')
        feedback.pushInfo('='*50)
        
        return {
            'STATUS': 'Success',
            'POLYGON_LAYER': polygon_layer.name(),
            'LINE_LAYER': line_layer.name()
        }
    
    def style_polygons(self, layer, colors, feedback):
        """
        Apply styling rules to polygon layer - matching QML structure exactly
        """
        
        # Create rule-based renderer
        root_rule = QgsRuleBasedRenderer.Rule(None)
        
        # GRASS - Light Green (symbol 0 in QML)
        grass_conditions = [
            '"landuse" = \'grass\'',
            '"landuse" = \'meadow\'',
            '"natural" = \'grassland\''
        ]
        grass_filter = ' OR '.join(grass_conditions)
        grass_symbol = QgsSymbol.defaultSymbol(2)
        grass_symbol.setColor(QColor(*colors['grass']))
        grass_symbol.setOpacity(0.7)
        grass_symbol.symbolLayer(0).setStrokeColor(QColor(*colors['grass']))
        grass_symbol.symbolLayer(0).setStrokeWidth(0.2)
        grass_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(grass_symbol, 0, 0, grass_filter, 'Grass'))
        
        # PARK - Medium Green (symbol 1 in QML)
        park_conditions = [
            '"leisure" = \'park\'',
            '"leisure" = \'garden\'',
            '"landuse" = \'recreation_ground\'',
            '"leisure" = \'playground\''
        ]
        park_filter = ' OR '.join(park_conditions)
        park_symbol = QgsSymbol.defaultSymbol(2)
        park_symbol.setColor(QColor(*colors['park']))
        park_symbol.setOpacity(0.7)
        park_symbol.symbolLayer(0).setStrokeColor(QColor(*colors['park']))
        park_symbol.symbolLayer(0).setStrokeWidth(0.2)
        park_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(park_symbol, 0, 0, park_filter, 'Park'))
        
        # FOREST - Dark Green (symbol 2 in QML)
        forest_conditions = [
            '"landuse" = \'forest\'',
            '"natural" = \'wood\'',
            '"natural" = \'tree_row\'',
            '"natural" = \'scrub\''
        ]
        forest_filter = ' OR '.join(forest_conditions)
        forest_symbol = QgsSymbol.defaultSymbol(2)
        forest_symbol.setColor(QColor(*colors['forest']))
        forest_symbol.setOpacity(0.7)
        forest_symbol.symbolLayer(0).setStrokeColor(QColor(*colors['forest']))
        forest_symbol.symbolLayer(0).setStrokeWidth(0.2)
        forest_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(forest_symbol, 0, 0, forest_filter, 'Forest'))
        
        # WATER - Pale Blue (symbol 3 in QML, pass=20)
        water_conditions = [
            '"natural" = \'water\'',
            '"natural" = \'bay\'',
            '"waterway" = \'river\'',
            '"waterway" = \'stream\'',
            '"waterway" = \'canal\'',
            '"waterway" = \'drain\'',
            '"landuse" = \'reservoir\'',
            '"landuse" = \'basin\''
        ]
        water_filter = ' OR '.join(water_conditions)
        water_symbol = QgsSymbol.defaultSymbol(2)
        water_symbol.setColor(QColor(*colors['water']))
        water_symbol.setOpacity(0.7)
        water_symbol.symbolLayer(0).setStrokeColor(QColor(*colors['water']))
        water_symbol.symbolLayer(0).setStrokeWidth(0.3)
        water_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(water_symbol, 0, 0, water_filter, 'Water'))
        
        # BUILDINGS - Grey (symbol 4 in QML)
        building_conditions = [
            '"building" IS NOT NULL',
            '"building" != \'no\'',
            '"building" != \'\''
        ]
        building_filter = ' AND '.join(building_conditions)
        building_symbol = QgsSymbol.defaultSymbol(2)
        building_symbol.setColor(QColor(*colors['buildings']))
        building_symbol.setOpacity(0.8)
        building_symbol.symbolLayer(0).setStrokeColor(QColor(*colors['buildings']))
        building_symbol.symbolLayer(0).setStrokeWidth(0.2)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(building_symbol, 0, 0, building_filter, 'Buildings'))
        
        # Apply renderer
        renderer = QgsRuleBasedRenderer(root_rule)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        
        feedback.pushInfo(f'  ✓ Applied {len(root_rule.children())} polygon rules')
    
    def style_lines(self, layer, colors, feedback):
        """
        Apply styling rules to line layer (highways and railways)
        Line widths: Start at 1.0 for motorway, decrease from there
        """
        
        # Create rule-based renderer
        root_rule = QgsRuleBasedRenderer.Rule(None)
        
        # RAILWAYS - Orange with dashed style (width 1.0)
        railway_conditions = [
            '"railway" = \'rail\'',
            '"railway" = \'subway\'',
            '"railway" = \'light_rail\'',
            '"railway" = \'tram\'',
            '"railway" IS NOT NULL'
        ]
        railway_filter = ' OR '.join(railway_conditions)
        railway_symbol = QgsSymbol.defaultSymbol(1)
        railway_symbol.setColor(QColor(colors['railway']))
        railway_symbol.setWidth(1.0)
        railway_symbol.symbolLayer(0).setPenStyle(Qt.DashLine)
        railway_symbol.symbolLayer(0).setPenCapStyle(Qt.RoundCap)
        railway_symbol.symbolLayer(0).setPenJoinStyle(Qt.RoundJoin)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(railway_symbol, 0, 0, railway_filter, 'Railway'))
        
        # HIGHWAYS - Black with variations, width starts at 1.0 and decreases
        highway_styles = [
            ('motorway', 1.0, colors['highway_motorway'], 
             '"highway" = \'motorway\' OR "highway" = \'motorway_link\''),
            ('trunk', 0.9, colors['highway_motorway'], 
             '"highway" = \'trunk\' OR "highway" = \'trunk_link\''),
            ('primary', 0.8, colors['highway_primary'], 
             '"highway" = \'primary\' OR "highway" = \'primary_link\''),
            ('secondary', 0.7, colors['highway_secondary'], 
             '"highway" = \'secondary\' OR "highway" = \'secondary_link\''),
            ('tertiary', 0.6, colors['highway_tertiary'], 
             '"highway" = \'tertiary\' OR "highway" = \'tertiary_link\''),
            ('residential', 0.5, colors['highway_residential'], 
             '"highway" = \'residential\''),
            ('unclassified', 0.45, colors['highway_service'], 
             '"highway" = \'unclassified\''),
            ('service', 0.4, colors['highway_service'], 
             '"highway" = \'service\''),
            ('living_street', 0.4, colors['highway_residential'], 
             '"highway" = \'living_street\''),
            ('pedestrian', 0.35, colors['highway_footway'], 
             '"highway" = \'pedestrian\''),
            ('footway', 0.3, colors['highway_footway'], 
             '"highway" = \'footway\''),
            ('path', 0.3, colors['highway_path'], 
             '"highway" = \'path\''),
            ('cycleway', 0.3, colors['highway_path'], 
             '"highway" = \'cycleway\''),
            ('track', 0.25, colors['highway_path'], 
             '"highway" = \'track\'')
        ]
        
        for road_name, width, color, filter_expr in highway_styles:
            highway_symbol = QgsSymbol.defaultSymbol(1)
            highway_symbol.setColor(QColor(color))
            highway_symbol.setWidth(width)
            highway_symbol.symbolLayer(0).setPenCapStyle(Qt.RoundCap)
            highway_symbol.symbolLayer(0).setPenJoinStyle(Qt.RoundJoin)
            
            root_rule.appendChild(QgsRuleBasedRenderer.Rule(highway_symbol, 0, 0, filter_expr, f'Highway - {road_name}'))
        
        # Apply renderer
        renderer = QgsRuleBasedRenderer(root_rule)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        
        feedback.pushInfo(f'  ✓ Applied {len(root_rule.children())} line rules')
    
    def name(self):
        """
        Returns the algorithm name
        """
        return 'style_rio_osm'
    
    def displayName(self):
        """
        Returns the translated algorithm name
        """
        return 'Style Rio de Janeiro OSM Layers'
    
    def group(self):
        """
        Returns the name of the group this algorithm belongs to
        """
        return 'Cartography'
    
    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to
        """
        return 'cartography'
    
    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm
        """
        return """
        Apply custom styling to OSM layers from Rio de Janeiro area.
        
        This algorithm styles:
        - Polygon layer: 
          * Buildings (grey RGB: 164,164,162)
          * Grass (light green RGB: 220,228,152)
          * Parks (medium green RGB: 218,224,160)
          * Forests (dark green RGB: 164,171,99)
          * Water (pale blue RGB: 138,198,213)
        
        - Line layer:
          * Railways (orange #FF8C00 with dashed lines, width 1.0)
          * Highways (black to grey gradient, width 1.0 to 0.25)
            - Motorway: 1.0mm, black
            - Trunk to track: Decreasing width and lightening color
        
        Input Requirements:
        - Polygon layer with OSM attributes (building, landuse, natural, leisure, waterway)
        - Line layer with highway and railway attributes
        
        Compatible with data from:
        - QuickOSM plugin
        - Overpass API queries
        - OSM shapefiles
        
        Colors match the provided QML style file.
        Based on Overpass query around coordinates: -22.9068, -43.1729 (Rio de Janeiro)
        """
    
    def createInstance(self):
        """
        Returns a new instance of the algorithm
        """
        return StyleRioOSMAlgorithm()


def classFactory(iface):
    """
    Required function for QGIS to recognize this as a processing provider
    """
    return StyleRioOSMAlgorithm()
