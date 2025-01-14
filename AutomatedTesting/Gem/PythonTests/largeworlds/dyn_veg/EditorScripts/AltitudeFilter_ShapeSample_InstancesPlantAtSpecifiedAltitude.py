"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import azlmbr.editor as editor
import azlmbr.legacy.general as general
import azlmbr.bus as bus
import azlmbr.math as math
import azlmbr.paths

sys.path.append(os.path.join(azlmbr.paths.devroot, 'AutomatedTesting', 'Gem', 'PythonTests'))
import editor_python_test_tools.hydra_editor_utils as hydra
from editor_python_test_tools.editor_test_helper import EditorTestHelper
from largeworlds.large_worlds_utils import editor_dynveg_test_helper as dynveg


class TestAltitudeFilterShapeSample(EditorTestHelper):
    def __init__(self):
        EditorTestHelper.__init__(self, log_prefix="AltitudeFilterShapeSample", args=["level"])

    def run_test(self):
        """
        Summary:
        A new level is created. A spawner entity is added, along with a planting surface at 32 on Z, and another at 36
        on Z. An Altitude Filter is added to the spawner entity, and set to sample a shape entity. Instance counts are
        validated.

        Expected Behavior:
        Instances are only spawned within the altitude range specified by the sampled shape.

        Test Steps:
         1) Create a new level
         2) Create an instance spawner entity
         3) Create surfaces to plant on, one at 32 on Z and another at 36 on Z.
         4) Initial instance counts pre-filter are verified.
         5) A new entity with shape is created, an sampled on the Vegetation Altitude Filter.
         6) Instance counts post-filter are verified.

        Note:
        - This test file must be called from the Open 3D Engine Editor command terminal
        - Any passed and failed tests are written to the Editor.log file.
                Parsing the file or running a log_monitor are required to observe the test results.

        :return: None
        """

        # 1) Create a new, temporary level
        self.test_success = self.create_level(
            self.args["level"],
            heightmap_resolution=1024,
            heightmap_meters_per_pixel=1,
            terrain_texture_resolution=4096,
            use_terrain=False,
        )

        # Set view of planting area for visual debugging
        general.set_current_view_position(512.0, 500.0, 38.0)
        general.set_current_view_rotation(-20.0, 0.0, 0.0)

        # 2) Create a new entity with required vegetation area components
        center_point = math.Vector3(512.0, 512.0, 32.0)
        asset_path = os.path.join("Slices", "PinkFlower.dynamicslice")
        spawner_entity = dynveg.create_vegetation_area("Instance Spawner", center_point, 16.0, 16.0, 16.0, asset_path)

        # Add a Vegetation Altitude Filter
        spawner_entity.add_component("Vegetation Altitude Filter")

        # 3) Add surfaces to plant on
        dynveg.create_surface_entity("Planting Surface", center_point, 32.0, 32.0, 1.0)
        elevated_surface_center_point = math.Vector3(512.0, 512.0, 36.0)
        dynveg.create_surface_entity("Planting Surface Elevated", elevated_surface_center_point, 32.0, 32.0, 1.0)

        # Set instances to spawn on a center snap point to avoid unexpected instances around the edges of the box shape
        veg_system_settings_component = hydra.add_level_component("Vegetation System Settings")
        editor.EditorComponentAPIBus(bus.Broadcast, "SetComponentProperty", veg_system_settings_component,
                                     'Configuration|Area System Settings|Sector Point Snap Mode', 1)

        # 4) Verify initial instance counts pre-filter
        num_expected = (20 * 20) * 2  # 20 instances per 16m per side x 2 surfaces
        spawner_success = self.wait_for_condition(lambda: dynveg.validate_instance_count_in_entity_shape(spawner_entity.id, num_expected), 5.0)
        self.test_success = self.test_success and spawner_success

        # 5) Create a new entity with a shape at 36 on the Z-axis, and pin the entity to the Vegetation Altitude Filter
        shape_sampler_center_point = math.Vector3(512.0, 512.0, 36.0)
        shape_sampler = hydra.Entity("Shape Sampler")
        shape_sampler.create_entity(
            shape_sampler_center_point,
            ["Box Shape"]
        )
        if shape_sampler.id.IsValid():
            print(f"'{shape_sampler.name}' created")
        spawner_entity.get_set_test(3, 'Configuration|Pin To Shape Entity Id', shape_sampler.id)

        # 6) Validate expected instance counts
        num_expected = 20 * 20  # Instances should now only plant on the elevated surface
        sampler_success = self.wait_for_condition(lambda: dynveg.validate_instance_count_in_entity_shape(spawner_entity.id, num_expected), 5.0)
        self.test_success = self.test_success and sampler_success


test = TestAltitudeFilterShapeSample()
test.run()
