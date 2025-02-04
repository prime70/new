from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bauiv1 as bui
import bascenev1 as bs
from bascenev1lib.gameutils import SharedObjects
import copy
if TYPE_CHECKING:
    from typing import Any, List, Dict


class mapdefs:
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (-0.2457963347, 3.828181068,
                                        -1.528362695) + (0.0, 0.0, 0.0) + (
                                            19.14849937, 7.312788846, 8.436232726)
    points['ffa_spawn1'] = (-5.869295124, 3.715437928,
                            -1.617274877) + (0.9410329222, 1.0, 1.818908238)
    points['ffa_spawn2'] = (5.160809653, 3.761793434,
                            -1.443012115) + (0.7729807005, 1.0, 1.818908238)
    points['ffa_spawn3'] = (-0.4266381164, 3.761793434,
                            -1.555562653) + (4.034151421, 1.0, 0.2731725824)
    points['flag1'] = (-7.354603923, 3.770769731, -1.617274877)
    points['flag2'] = (6.885846926, 3.770685211, -1.443012115)
    points['flag_default'] = (-0.2227795102, 3.802429326, -1.562586233)
    boxes['map_bounds'] = (-0.1916036665, 7.481446847, -1.311948055) + (
        0.0, 0.0, 0.0) + (27.41996888, 18.47258973, 19.52220249)
    points['powerup_spawn1'] = (6.82849491, 4.658454461, 0.1938139802)
    points['powerup_spawn2'] = (-7.253381358, 4.728692078, 0.252121017)
    points['powerup_spawn3'] = (6.82849491, 4.658454461, -3.461765427)
    points['powerup_spawn4'] = (-7.253381358, 4.728692078, -3.40345839)
    points['shadow_lower_bottom'] = (-0.2227795102, 2.83188898, 2.680075641)
    points['shadow_lower_top'] = (-0.2227795102, 3.498267184, 2.680075641)
    points['shadow_upper_bottom'] = (-0.2227795102, 6.305086402, 2.680075641)
    points['shadow_upper_top'] = (-0.2227795102, 9.470923628, 2.680075641)
    points['spawn1'] = (-5.869295124, 3.715437928,
                        -1.617274877) + (0.9410329222, 1.0, 1.818908238)
    points['spawn2'] = (5.160809653, 3.761793434,
                        -1.443012115) + (0.7729807005, 1.0, 1.818908238)


class BridgitParallelo(bs.Map):
    """Map with a narrow bridge in the middle."""
    defs = mapdefs
    defs.points['powerup_spawn4'] = (-7.253381358, 4.728692078, -6.40345839)
    defs.points['powerup_spawn3'] = (6.82849491, 4.658454461, -6.461765427)
    defs.points['spawn1'] = (-5.869295124, 3.715437928,
                             -3.617274877) + (0.9410329222, 1.0, 0.818908238)
    defs.boxes['area_of_interest_bounds'] = (-0.2457963347, 3.828181068,
                                             -3.528362695) + (0.0, 0.0, 0.0) + (
        19.14849937, 7.312788846, 6.436232726)

    name = 'Bridgit Parallelo'
    dataname = 'bridgit'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        # print('getting playtypes', cls._getdata()['play_types'])
        return ['melee', 'team_flag', 'keep_away']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'bridgitPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'mesh_top': bs.getmesh('bridgitLevelTop'),
            'mesh_bottom': bs.getmesh('bridgitLevelBottom'),
            'mesh_bg': bs.getmesh('natureBackground'),
            'bg_vr_fill_mesh': bs.getmesh('natureBackgroundVRFill'),
            'collision_mesh': bs.getcollisionmesh('bridgitLevelCollide'),
            'tex': bs.gettexture('bridgitLevelColor'),
            'mesh_bg_tex': bs.gettexture('natureBackgroundColor'),
            'collide_bg': bs.getcollisionmesh('natureBackgroundCollide'),
            'railing_collision_mesh':
                (bs.getcollisionmesh('bridgitLevelRailingCollide')),
            'bg_material': bs.Material()
        }
        data['bg_material'].add_actions(actions=('modify_part_collision',
                                                 'friction', 10.0))
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = bs.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collision_mesh': self.preloaddata['collision_mesh'],
                'mesh': self.preloaddata['mesh_top'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.bottom = bs.newnode('terrain',
                                 attrs={
                                     'mesh': self.preloaddata['mesh_bottom'],
                                     'lighting': False,
                                     'color_texture': self.preloaddata['tex']
                                 })
        self.background = bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['mesh_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['mesh_bg_tex']
            })
        bs.newnode('terrain',
                   attrs={
                       'mesh': self.preloaddata['bg_vr_fill_mesh'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['mesh_bg_tex']
                   })
        # self.railing = bs.newnode(
        #     'terrain',
        #     attrs={
        #         'collision_mesh': self.preloaddata['railing_collision_mesh'],
        #         'materials': [shared.railing_material],
        #         'bumper': False
        #     })
        self.bg_collide = bs.newnode('terrain',
                                     attrs={
                                         'collision_mesh':
                                             self.preloaddata['collide_bg'],
                                         'materials': [
                                             shared.footing_material,
                                             self.preloaddata['bg_material'],
                                             shared.death_material
                                             ]
                                     })
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.1, 1.2, 1.3)
        gnode.ambient_color = (1.1, 1.2, 1.3)
        gnode.vignette_outer = (0.65, 0.6, 0.55)
        gnode.vignette_inner = (0.9, 0.9, 0.93)
        self.map_extend()

    def is_point_near_edge(self,
                           point: babase.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

    def map_extend(self):

        shared = SharedObjects.get()
        self._real_wall_material = bs.Material()

        self._real_wall_material.add_actions(

            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', True)

            ))
        self.mat = bs.Material()
        self.mat.add_actions(

            actions=(('modify_part_collision', 'physical', False),
                     ('modify_part_collision', 'collide', False))
        )
        spaz_collide_mat = bs.Material()
        # spaz_collide_mat.add_actions(
        #     conditions=('they_have_material',shared.player_material),
        #     actions=(
        #         ('modify_part_collision', 'collide', True),
        #         ( 'call','at_connect',babase.Call(self._handle_player_pad_collide,real )),
        #     ),
        #     )
        pos = (0.0, 3.004164695739746, -3.3991328477859497)
        self.ud_1_r = bs.newnode('region', attrs={'position': pos, 'scale': (2, 1, 2), 'type': 'box', 'materials': [
                                 shared.footing_material, self._real_wall_material, spaz_collide_mat]})

        self.node = bs.newnode('prop',
                               owner=self.ud_1_r,
                               attrs={
                                   'mesh': bs.getmesh('bridgitLevelTop'),
                                   'light_mesh': bs.getmesh('powerupSimple'),
                                   'position': (2, 7, 2),
                                   'body': 'puck',
                                   'shadow_size': 0.0,
                                   'velocity': (0, 0, 0),
                                   'color_texture': bs.gettexture('bridgitLevelColor'),

                                   'reflection_scale': [1.5],
                                   'materials': [self.mat, shared.object_material, shared.footing_material],

                                   'density': 9000000000
                               })
        self.node.changerotation(0, 0, 0)
        mnode = bs.newnode('math',
                           owner=self.ud_1_r,
                           attrs={
                               'input1': (0, -2.9, 0),
                               'operation': 'add'
                           })

        self.ud_1_r.connectattr('position', mnode, 'input2')
        mnode.connectattr('output', self.node, 'position')

        #   base / bottom ====================================

        pos = (0.0, 2.004164695739746, -3.3991328477859497)
        self.ud_2_r = bs.newnode('region', attrs={'position': pos, 'scale': (2, 1, 2), 'type': 'box', 'materials': [
                                 shared.footing_material, self._real_wall_material, spaz_collide_mat]})

        self.node2 = bs.newnode('prop',
                                owner=self.ud_2_r,
                                attrs={
                                    'mesh': bs.getmesh('bridgitLevelBottom'),
                                    'light_mesh': bs.getmesh('powerupSimple'),
                                    'position': (2, 7, 2),
                                    'body': 'puck',
                                    'shadow_size': 0.0,
                                    'velocity': (0, 0, 0),
                                    'color_texture': bs.gettexture('bridgitLevelColor'),

                                    'reflection_scale': [1.5],
                                    'materials': [self.mat, shared.object_material, shared.footing_material],

                                    'density': 9000000000
                                })
        mnode = bs.newnode('math',
                           owner=self.ud_2_r,
                           attrs={
                               'input1': (0, -1.8, 0),
                               'operation': 'add'
                           })

        self.ud_2_r.connectattr('position', mnode, 'input2')
        mnode.connectattr('output', self.node2, 'position')

        # /// region to stand long bar ===============

        pos = (-6.25, 3.204164695739746, -5.3991328477859497)
        self.v_region = bs.newnode('region', attrs={'position': pos, 'scale': (3.4, 1, 4), 'type': 'box', 'materials': [
                                   shared.footing_material, self._real_wall_material, spaz_collide_mat]})

        pos = (0.5, 3.204164695739746, -4.7991328477859497)
        self.h_1_region = bs.newnode('region', attrs={'position': pos, 'scale': (12, 1, 1.4), 'type': 'box', 'materials': [
                                     shared.footing_material, self._real_wall_material, spaz_collide_mat]})
        pos = (5.6, 3.204164695739746, -5.3991328477859497)
        self.h_2_region = bs.newnode('region', attrs={'position': pos, 'scale': (3.4, 1, 4), 'type': 'box', 'materials': [
                                     shared.footing_material, self._real_wall_material, spaz_collide_mat]})


bs._map.register_map(BridgitParallelo)
