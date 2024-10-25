"""
  Generated by Eclipse Cyclone DDS idlc Python Backend
  Cyclone DDS IDL version: v0.11.0
  Module: inspire
  IDL file: inspire_hand_ctrl.idl

"""

from dataclasses import dataclass
from enum import auto
from typing import TYPE_CHECKING, Optional

import cyclonedds.idl as idl
import cyclonedds.idl.annotations as annotate
import cyclonedds.idl.types as types

# root module import for resolving types
# import inspire_dds


@dataclass
@annotate.final
@annotate.autoid("sequential")
class inspire_hand_ctrl(idl.IdlStruct, typename="inspire.inspire_hand_ctrl"):
    pos_set: types.sequence[types.int16, 6]
    angle_set: types.sequence[types.int16, 6]
    force_set: types.sequence[types.int16, 6]
    speed_set: types.sequence[types.int16, 6]
    mode: types.int8


