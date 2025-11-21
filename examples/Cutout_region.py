from helpers.setup import *

# Initialize with this script's path
db, cell, layout, gnd_net = initialize_edb(__file__)

# Create multiple nets
net_names = ["Signal_1", "Signal_2", "Signal_3"]
for name in net_names:
    Net.create(layout, name)

# Create stackup layers
insulator_layer_1 = StackupLayer.create(
    "D1", LayerType.DIELECTRIC_LAYER, 0.0002, 0.0002, "FR4_epoxy"
)
layer_1 = StackupLayer.create("S1", LayerType.SIGNAL_LAYER, 0.0001, 0.0003, "copper")
insulator_layer_2 = StackupLayer.create(
    "D2", LayerType.DIELECTRIC_LAYER, 0.0001, 0.0004, "FR4_epoxy"
)
layer_2 = StackupLayer.create("S2", LayerType.SIGNAL_LAYER, 0.0001, 0.0005, "copper")
insulator_layer_3 = StackupLayer.create(
    "D3", LayerType.DIELECTRIC_LAYER, 0.0003, 0.0005, "FR4_epoxy"
)
layer_3 = StackupLayer.create("S3", LayerType.SIGNAL_LAYER, 0.0001, 0.0007, "copper")

# Create Layer Collection
lc = layout.layer_collection
lc.mode = LayerCollectionMode.OVERLAPPING
lc.add_layers([insulator_layer_1, layer_1, insulator_layer_2, layer_2, insulator_layer_3, layer_3])

# Find layers by name
layer_1 = lc.find_by_name("S1")
layer_2 = lc.find_by_name("S2")
layer_3 = lc.find_by_name("S3")

# Print layer names in the Layer Collection
print("Layers in Layer Collection:", [(l.name) for l in lc.get_layers()])

# Unit conversion function
um = lambda val: val * 1e-6

# Create rectangles on different layers and nets
rect = Rectangle.create(
    layout=layout,
    layer=layer_1,
    net="Signal_1",
    rep_type=RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT,
    param1=um(-46),
    param2=um(9),
    param3=um(-17),
    param4=um(-14),
    corner_rad=0.0,
    rotation=0.0,
)
rect_2 = Rectangle.create(
    layout=layout,
    layer=layer_2,
    net="Signal_2",
    rep_type=RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT,
    param1=um(-33),
    param2=um(14),
    param3=um(0),
    param4=um(-3),
    corner_rad=0.0,
    rotation=0.0,
)
rect_3 = Rectangle.create(
    layout=layout,
    layer=layer_3,
    net="Signal_3",
    rep_type=RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT,
    param1=um(-8),
    param2=um(-11),
    param3=um(-36),
    param4=um(2),
    corner_rad=0.0,
    rotation=0.0,
)
rect_4 = Rectangle.create(
    layout=layout,
    layer=layer_1,
    net="GND",
    rep_type=RectangleRepresentationType.LOWER_LEFT_UPPER_RIGHT,
    param1=um(-116),
    param2=um(-11),
    param3=um(-101),
    param4=um(-20),
    corner_rad=0.0,
    rotation=0.0,
)

# Retrieve the primitives created
primitives_created = layout.primitives

# Print primitive types and their layers
print(
    "Primitive Types and Layers Before Cutout:",
    [(p.primitive_type.name, p.layer.name) for p in primitives_created],
)

# Create a cutout region using PolygonData
um = lambda val_1, val_2: (val_1 * 1e-6, val_2 * 1e-6)
cutout_region = PolygonData(
    [um(-7, 7), um(-23, -13), um(-39, -5), um(-38, 12), um(-20, 17)], closed=True
)

# Get all nets in the layout
nets = layout.nets

# Create a new cell with the cutout region applied to all nets
new_cutout_cell = cell.cutout(nets, nets, cutout_region)

# Retrieve the primitives in the new cutout cell
primitives_of_cutout_region = new_cutout_cell.layout.primitives

# Print primitive types and their layers in the cutout region cell
print(
    "Primitive Types and Layers After Cutout:",
    [(p.primitive_type.name, p.layer.name) for p in primitives_of_cutout_region],
)

# Save and close the design
db.save()
db.close()
