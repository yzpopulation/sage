# Makes sage.combinat.root_system? equivalent to sage.combinat.root_system.root_system?
from root_system import __doc__

# currently needed to activate the backward compatibility register_unpickle_override
import type_A
import type_B
import type_C
import type_D
import type_E
import type_F
import type_G

import all

"""
Root Systems
============

.. toctree::
   :maxdepth: 2

   ../sage/combinat/root_system/cartan_type
   ../sage/combinat/root_system/dynkin_diagram
   ../sage/combinat/root_system/cartan_matrix
   ../sage/combinat/root_system/coxeter_matrix
   ../sage/combinat/root_system/type_folded

   ../sage/combinat/root_system/root_system
   ../sage/combinat/root_system/plot
   ../sage/combinat/root_system/root_lattice_realizations
   ../sage/combinat/root_system/root_lattice_realization_algebras
   ../sage/combinat/root_system/weight_lattice_realizations
   ../sage/combinat/root_system/root_space
   ../sage/combinat/root_system/weight_space
   ../sage/combinat/root_system/ambient_space

   ../sage/combinat/root_system/coxeter_group
   ../sage/combinat/root_system/weyl_group

   ../sage/combinat/root_system/weyl_characters
   ../sage/combinat/root_system/branching_rules
   ../sage/combinat/root_system/hecke_algebra_representation
   ../sage/combinat/root_system/non_symmetric_macdonald_polynomials

   ../sage/combinat/root_system/type_affine
   ../sage/combinat/root_system/type_dual
   ../sage/combinat/root_system/type_reducible
   ../sage/combinat/root_system/type_relabel
   ../sage/combinat/root_system/type_A
   ../sage/combinat/root_system/type_B
   ../sage/combinat/root_system/type_C
   ../sage/combinat/root_system/type_D
   ../sage/combinat/root_system/type_E
   ../sage/combinat/root_system/type_F
   ../sage/combinat/root_system/type_G
   ../sage/combinat/root_system/type_H
   ../sage/combinat/root_system/type_I
   ../sage/combinat/root_system/type_A_affine
   ../sage/combinat/root_system/type_B_affine
   ../sage/combinat/root_system/type_C_affine
   ../sage/combinat/root_system/type_D_affine
   ../sage/combinat/root_system/type_E_affine
   ../sage/combinat/root_system/type_F_affine
   ../sage/combinat/root_system/type_G_affine
   ../sage/combinat/root_system/type_BC_affine
"""
