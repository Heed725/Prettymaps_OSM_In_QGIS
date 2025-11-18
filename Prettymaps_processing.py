"""
QGIS Processing Script: Style OSM Map Layers (Prettymaps Style)
Applies prettymaps-inspired styling to any OSM polygon and line layers
Works with any location - not just Times Square!
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFeatureSink,
    QgsSymbol,
    QgsRuleBasedRenderer,
    QgsProject,
    QgsProcessingException
)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import Qt, QCoreApplication

class StyleOSMMapAlgorithm(QgsProcessingAlgorithm):
    """
    Processing algorithm to apply prettymaps styling to OSM layers from any location
    """
    
    # Parameter names
    POLYGON_LAYER = 'POLYGON_LAYER'
    LINE_LAYER = 'LINE_LAYER'
    
    def initAlgorithm(self, config=None):
        """
        Define the inputs and outputs of the algorithm
        """
        
        # Input polygon layer (buildings, parks, water, etc.)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.POLYGON_LAYER,
                'Polygon Layer (buildings, parks, water)',
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        
        # Input line layer (streets/roads)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.LINE_LAYER,
                'Line Layer (streets/roads)',
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
        
        # Color definitions matching prettymaps style
        colors = {
            'background': '#F2F4CB',
            'green': '#D0F1BF',
            'forest': '#64B96A',
            'water': '#a1e3ff',
            'parking': '#F2F4CB',
            'streets': '#2F3737',
            'building_palette': ['#FFC857', '#E9724C', '#C5283D'],
            'edge': '#2F3737'
        }
        
        # ========== STYLE POLYGON LAYER ==========
        feedback.pushInfo('\n--- Styling Polygons ---')
        self.style_polygons(polygon_layer, colors, feedback)
        
        # ========== STYLE LINE LAYER ==========
        feedback.pushInfo('\n--- Styling Lines ---')
        self.style_lines(line_layer, colors, feedback)
        
        # Set canvas background
        canvas = context.project().mapCanvas() if hasattr(context.project(), 'mapCanvas') else None
        if canvas:
            canvas.setCanvasColor(QColor(colors['background']))
            canvas.refresh()
        
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
        Apply styling rules to polygon layer
        """
        
        # Create rule-based renderer
        root_rule = QgsRuleBasedRenderer.Rule(None)
        
        # GREEN SPACES - flexible attribute checking
        green_conditions = [
            '"landuse" = \'grass\'',
            '"leisure" = \'park\'',
            '"leisure" = \'garden\'',
            '"natural" = \'island\'',
            '"natural" = \'wood\'',
            '"natural" = \'grassland\'',
            '"landuse" = \'meadow\'',
            '"landuse" = \'recreation_ground\''
        ]
        green_filter = ' OR '.join(green_conditions)
        green_symbol = QgsSymbol.defaultSymbol(2)
        green_symbol.setColor(QColor(colors['green']))
        green_symbol.symbolLayer(0).setStrokeColor(QColor(colors['edge']))
        green_symbol.symbolLayer(0).setStrokeWidth(0.3)
        green_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(green_symbol, 0, 0, green_filter, 'Green Spaces'))
        
        # FOREST
        forest_conditions = [
            '"landuse" = \'forest\'',
            '"natural" = \'tree_row\'',
            '"natural" = \'scrub\''
        ]
        forest_filter = ' OR '.join(forest_conditions)
        forest_symbol = QgsSymbol.defaultSymbol(2)
        forest_symbol.setColor(QColor(colors['forest']))
        forest_symbol.symbolLayer(0).setStrokeColor(QColor(colors['edge']))
        forest_symbol.symbolLayer(0).setStrokeWidth(0.3)
        forest_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(forest_symbol, 0, 0, forest_filter, 'Forest'))
        
        # WATER
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
        water_symbol.setColor(QColor(colors['water']))
        water_symbol.symbolLayer(0).setStrokeColor(QColor(colors['edge']))
        water_symbol.symbolLayer(0).setStrokeWidth(0.3)
        water_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(water_symbol, 0, 0, water_filter, 'Water'))
        
        # PARKING / PEDESTRIAN / PLAZAS
        parking_conditions = [
            '"amenity" = \'parking\'',
            '"highway" = \'pedestrian\'',
            '"highway" = \'footway\'',
            '"man_made" = \'pier\'',
            '"leisure" = \'plaza\'',
            '"place" = \'square\''
        ]
        parking_filter = ' OR '.join(parking_conditions)
        parking_symbol = QgsSymbol.defaultSymbol(2)
        parking_symbol.setColor(QColor(colors['parking']))
        parking_symbol.symbolLayer(0).setStrokeColor(QColor(colors['edge']))
        parking_symbol.symbolLayer(0).setStrokeWidth(0.3)
        parking_symbol.symbolLayer(0).setStrokeStyle(Qt.SolidLine)
        root_rule.appendChild(QgsRuleBasedRenderer.Rule(parking_symbol, 0, 0, parking_filter, 'Parking/Pedestrian'))
        
        # BUILDINGS (3-color palette) - flexible building detection
        building_conditions = [
            '"building" IS NOT NULL',
            '"building" != \'no\'',
            '"building" != \'\''
        ]
        building_filter = ' AND '.join(building_conditions)
        
        for i, color in enumerate(colors['building_palette']):
            building_symbol = QgsSymbol.defaultSymbol(2)
            building_symbol.setColor(QColor(color))
            building_symbol.symbolLayer(0).setStrokeColor(QColor(colors['edge']))
            building_symbol.symbolLayer(0).setStrokeWidth(0.15)
            # Use fid or osm_id for color distribution - works with any layer
            if 'osm_id' in [field.name() for field in layer.fields()]:
                building_sub_filter = f'({building_filter}) AND ("osm_id" % 3 = {i})'
            elif 'fid' in [field.name() for field in layer.fields()]:
                building_sub_filter = f'({building_filter}) AND ("fid" % 3 = {i})'
            else:
                building_sub_filter = f'({building_filter}) AND ($id % 3 = {i})'
            root_rule.appendChild(QgsRuleBasedRenderer.Rule(building_symbol, 0, 0, building_sub_filter, f'Buildings {i+1}'))
        
        # Apply renderer
        renderer = QgsRuleBasedRenderer(root_rule)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        
        feedback.pushInfo(f'  ✓ Applied {len(root_rule.children())} polygon rules')
    
    def style_lines(self, layer, colors, feedback):
        """
        Apply styling rules to line layer (streets)
        """
        
        # Create rule-based renderer
        root_rule = QgsRuleBasedRenderer.Rule(None)
        
        # Define road styles - comprehensive road types
        road_styles = [
            ('motorway', 1.2, '"highway" = \'motorway\' OR "highway" = \'motorway_link\''),
            ('trunk', 1.1, '"highway" = \'trunk\' OR "highway" = \'trunk_link\''),
            ('primary', 1.0, '"highway" = \'primary\' OR "highway" = \'primary_link\''),
            ('secondary', 0.9, '"highway" = \'secondary\' OR "highway" = \'secondary_link\''),
            ('tertiary', 0.8, '"highway" = \'tertiary\' OR "highway" = \'tertiary_link\''),
            ('residential', 0.6, '"highway" = \'residential\''),
            ('service', 0.4, '"highway" = \'service\''),
            ('unclassified', 0.5, '"highway" = \'unclassified\''),
            ('living_street', 0.5, '"highway" = \'living_street\''),
            ('pedestrian', 0.4, '"highway" = \'pedestrian\''),
            ('footway', 0.3, '"highway" = \'footway\' OR "highway" = \'path\''),
            ('cycleway', 0.3, '"highway" = \'cycleway\''),
            ('track', 0.3, '"highway" = \'track\''),
            ('other', 0.3, '"highway" IS NOT NULL')
        ]
        
        for road_name, width, filter_expr in road_styles:
            street_symbol = QgsSymbol.defaultSymbol(1)
            street_symbol.setColor(QColor(colors['streets']))
            street_symbol.setWidth(width)
            street_symbol.symbolLayer(0).setPenCapStyle(Qt.RoundCap)
            street_symbol.symbolLayer(0).setPenJoinStyle(Qt.RoundJoin)
            
            root_rule.appendChild(QgsRuleBasedRenderer.Rule(street_symbol, 0, 0, filter_expr, f'Street - {road_name}'))
        
        # Apply renderer
        renderer = QgsRuleBasedRenderer(root_rule)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
        
        feedback.pushInfo(f'  ✓ Applied {len(root_rule.children())} line rules')
    
    def name(self):
        """
        Returns the algorithm name
        """
        return 'style_osm_prettymaps'
    
    def displayName(self):
        """
        Returns the translated algorithm name
        """
        return 'Style OSM Map (Prettymaps)'
    
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
        Apply prettymaps-inspired styling to OSM layers from ANY location.
        
        This algorithm styles:
        - Polygon layer: Buildings (3-color palette), parks, water, forests, parking, plazas
        - Line layer: Streets with varying widths based on road type (14 road types)
        
        Works with OSM data from anywhere in the world!
        
        Input Requirements:
        - Polygon layer with OSM attributes (building, landuse, natural, leisure, amenity, waterway)
        - Line layer with highway attribute
        
        Compatible with data from:
        - QuickOSM plugin
        - Overpass API queries
        - OSM shapefiles
        - Any OSM-tagged vector data
        
        Colors match the prettymaps aesthetic with cream background and 
        orange/red building palette.
        """
    
    def createInstance(self):
        """
        Returns a new instance of the algorithm
        """
        return StyleOSMMapAlgorithm()


def classFactory(iface):
    """
    Required function for QGIS to recognize this as a processing provider
    """
    return StyleOSMMapAlgorithm()
