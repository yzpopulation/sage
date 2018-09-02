r"""
Subalgebras of Lie algebras

AUTHORS:

- Eero Hakavuori (2018-08-29): initial version
"""

# ****************************************************************************
#       Copyright (C) 2018 Eero Hakavuori <eero.hakavuori@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                 https://www.gnu.org/licenses/
# ****************************************************************************

from sage.algebras.lie_algebras.lie_algebra_element import LieAlgebraElementWrapper
from sage.categories.lie_algebras import LieAlgebras
from sage.categories.homset import Hom
from sage.categories.morphism import SetMorphism
from sage.categories.sets_cat import Sets
from sage.misc.cachefunc import cached_method
from sage.modules.free_module_element import vector
from sage.sets.family import Family
from sage.structure.element import coercion_model, have_same_parent
from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation


class LieSubset(Parent, UniqueRepresentation):
    r"""
    An abstract base class for a subset of a Lie algebra.

    INPUT:

    - ``ambient`` -- the Lie algebra containing the subset

    EXAMPLES::

        sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
        sage: L.<X,Y> = LieAlgebra(QQ)
        sage: S = LieSubset(L); S
        Abstract subset of Free Lie algebra generated by (X, Y) over Rational Field
        sage: S.category()
        Category of subobjects of sets

    TESTS::

        sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
        sage: L.<X,Y> = LieAlgebra(QQ, abelian=True)
        sage: K.<X,Y> = LieAlgebra(QQ, {})
        sage: LieSubset(L) == LieSubset(K)
        True
    """

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<X,Y> = LieAlgebra(QQ)
            sage: LieSubset(L)
            Abstract subset of Free Lie algebra generated by (X, Y) over Rational Field
        """
        return "Abstract subset of %s" % self.ambient()

    def __init__(self, ambient, category=None):
        r"""
        Initialize ``self``.

        TESTS::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<X,Y> = LieAlgebra(QQ)
            sage: S = LieSubset(L)
            sage: TestSuite(S).run()
        """
        self._ambient = ambient
        cat = Sets().Subobjects()
        category = cat.or_subcategory(category)
        super(LieSubset, self).__init__(ambient.base_ring(), category=category)

        # register a coercion to the ambient Lie algebra
        H = Hom(self, ambient)
        f = SetMorphism(H, self.lift)
        ambient.register_coercion(f)

    def __getitem__(self, x):
        r"""
        If `x` is a pair `(a, b)`, return the Lie bracket `[a, b]`.
        Otherwise try to return the `x`-th element of ``self``.

        This replicates the convenience syntax for Lie brackets of Lie algebras.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<x,y> = LieAlgebra(QQ, representation="polynomial")
            sage: S = LieSubset(L)
            sage: a = S(x); b = S(y)
            sage: S[a, b]
            x*y - y*x
            sage: S[a, a + S[a,b]]
            x^2*y - 2*x*y*x + y*x^2
        """
        if isinstance(x, tuple) and len(x) == 2:
            return self(x[0])._bracket_(self(x[1]))
        return super(LieSubset, self).__getitem__(x)

    def _an_element_(self):
        r"""
        Return an element of ``self``.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<X,Y> = LieAlgebra(QQ)
            sage: S = LieSubset(L)
            sage: S._an_element_()
            X + Y
        """
        return self.element_class(self, self.ambient()._an_element_())

    def _element_constructor_(self, x):
        r"""
        Convert ``x`` into ``self``.

        EXAMPLES:

        Elements of subsets are created directly from elements
        of the ambient Lie algebra::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<x,y> = LieAlgebra(ZZ, {('x','y'): {'x': 1}})
            sage: S = LieSubset(L)
            sage: S(x)
            x
            sage: S(x).parent()
            Abstract subset of Lie algebra on 2 generators (x, y) over Integer Ring

        A list of 2 elements is interpreted as a Lie bracket::

            sage: S([S(x), S(y)])
            x
            sage: S([S(x), S(y)]) == S(L[x, y])
            True
        """
        if isinstance(x, list) and len(x) == 2:
            return self(x[0])._bracket_(self(x[1]))

        try:
            P = x.parent()
#             if P is self:
#                 return x
            if x.parent() == self.ambient():
                return self.element_class(self, x)
        except AttributeError:
            pass

        return super(LieSubset, self)._element_constructor_(x)

    @cached_method
    def zero(self):
        r"""
        Return the element `0`.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<x,y> = LieAlgebra(QQ, representation="polynomial")
            sage: S = LieSubset(L)
            sage: S.zero()
            0
            sage: S.zero() == S(L.zero())
            True
        """
        return self.element_class(self, self.ambient().zero())

    def ambient(self):
        r"""
        Return the ambient Lie algebra of ``self``.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<x,y> = LieAlgebra(QQ, abelian=True)
            sage: S = LieSubset(L)
            sage: S.ambient() is L
            True
        """
        return self._ambient

    def lift(self, X):
        r"""
        Coerce an element ``X`` of ``self`` into the ambient Lie algebra.

        INPUT:

        - ``X`` -- an element of ``self``

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<x,y> = LieAlgebra(QQ, abelian=True)
            sage: S = LieSubset(L)
            sage: sx = S(x); sx
            x
            sage: sx.parent()
            Abstract subset of Abelian Lie algebra on 2 generators (x, y) over Rational Field
            sage: a = S.lift(sx); a
            x
            sage: a.parent()
            Abelian Lie algebra on 2 generators (x, y) over Rational Field
        """
        return X.value

    def retract(self, x):
        r"""
        Retract ``x`` to ``self``.

        INPUT:

        - ``x`` -- an element of the ambient Lie algebra

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
            sage: L.<x,y> = LieAlgebra(QQ, abelian=True)
            sage: S = LieSubset(L)
            sage: S.retract(x)
            x
            sage: S.retract(x).parent()
            Abstract subset of Abelian Lie algebra on 2 generators (x, y) over Rational Field
        """
        return self.element_class(self, x)

    class Element(LieAlgebraElementWrapper):
        r"""
        Wrap an element of the ambient Lie algebra as an element.
        """

        def _bracket_(self, x):
            """
            Return the Lie bracket ``[self, x]``.

            Assumes ``x`` and ``self`` have the same parent.

            INPUT:

            - ``x`` -- an element of the same Lie subalgebra as ``self``

            EXAMPLES::

                sage: from sage.algebras.lie_algebras.subalgebra import LieSubset
                sage: L.<x,y> = LieAlgebra(QQ)
                sage: S = LieSubset(L)
                sage: S(x)._bracket_(S(y))
                [x, y]
            """
            P = self.parent()
            self_lift = P.lift(self)
            x_lift = P.lift(x)
            return P.retract(P.ambient().bracket(self_lift, x_lift))


class LieSubset_with_gens(LieSubset):
    r"""
    An abstract base class for a subset of a Lie algebra with a generating set.

    INPUT:

    - ``ambient`` -- the Lie algebra containing the subset
    - ``gens`` -- a tuple of generators from the ambient Lie algebra

    EXAMPLES::

        sage: from sage.algebras.lie_algebras.subalgebra import LieSubset_with_gens
        sage: L.<X,Y> = LieAlgebra(QQ)
        sage: L = L.Lyndon()
        sage: LieSubset_with_gens(L, (X, L[X, Y]))
        Abstract subset with generators (X, [X, Y]) of Free Lie algebra
        generated by (X, Y) over Rational Field in the Lyndon basis
    """

    def __init__(self, ambient, gens, category=None):
        r"""
        Initialize ``self``.

        TESTS::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset_with_gens
            sage: L.<X,Y> = LieAlgebra(QQ)
            sage: S = LieSubset_with_gens(L, (X,))
            sage: TestSuite(S).run()
        """
        self._gens = gens
        super(LieSubset_with_gens, self).__init__(ambient, category=category)

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset_with_gens
            sage: L.<X,Y> = LieAlgebra(QQ)
            sage: LieSubset_with_gens(L, (X,))
            Abstract subset with generators (X,) of Free Lie algebra generated by (X, Y) over Rational Field
        """
        return "Abstract subset with generators %s of %s" % (self.gens(), self.ambient())

    def _an_element_(self):
        r"""
        Return an element of ``self``.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset_with_gens
            sage: L.<X,Y> = LieAlgebra(QQ)
            sage: S = LieSubset_with_gens(L, (X,))
            sage: S._an_element_()
            X
        """
        return self.element_class(self, self.gens()[0])

    def gens(self):
        r"""
        Return the generating set of ``self``.

        EXAMPLES::

            sage: from sage.algebras.lie_algebras.subalgebra import LieSubset_with_gens
            sage: L.<x,y,z> = LieAlgebra(QQ, {('x','y'): {'z': 1}})
            sage: S = LieSubset_with_gens(L, (x,))
            sage: S.gens()
            (x,)
        """
        return self._gens


class LieSubalgebra_finite_dimensional_with_basis(LieSubset_with_gens):
    r"""
    A Lie subalgebra of a finite dimensional Lie algebra with basis.

    INPUT:

    - ``ambient`` -- the Lie algebra containing the subalgebra
    - ``gens`` -- a list of generators of the subalgebra
    - ``category`` -- (optional) a subcategory of subobjects of finite
      dimensional Lie algebras with basis

    EXAMPLES:

    A subalgebra is defined by giving a list of generators::

        sage: L = lie_algebras.Heisenberg(QQ, 1)
        sage: X, Y, Z = L.basis()
        sage: I =  L.subalgebra([X, Z]); I
        Subalgebra generated by (p1, z) of Heisenberg algebra of rank 1 over Rational Field
        sage: I.basis()
        Family (p1, z)

    A subalgebra of a subalgebra is a subalgebra of the original::

        sage: sc = {('X','Y'): {'Z': 1}, ('X','Z'): {'W': 1}}
        sage: L.<X,Y,Z,W> = LieAlgebra(QQ, sc)
        sage: S1 = L.subalgebra([Y, Z, W]); S1
        Subalgebra generated by (Y, Z, W) of Lie algebra on 4 generators (X, Y, Z, W) over Rational Field
        sage: S2 = S1.subalgebra(S1.basis()[1:]); S2
        Subalgebra generated by (Z, W) of Lie algebra on 4 generators (X, Y, Z, W) over Rational Field
        sage: S3 = S2.subalgebra(S2.basis()[1:]); S3
        Subalgebra generated by W of Lie algebra on 4 generators (X, Y, Z, W) over Rational Field

    The zero dimensional subalgebra can be created by giving 0 as a generator
    or with an empty list of generators::

        sage: L.<X,Y,Z> = LieAlgebra(QQ, {('X','Y'): {'Z': 1}})
        sage: S1 = L.subalgebra(0)
        sage: S2 = L.subalgebra([])
        sage: S1 is S2
        True
        sage: S1.basis()
        Family ()

    TESTS:

    A test suite::

        sage: S =  L.subalgebra(X + Y)
        sage: TestSuite(S).run()
    """

    @staticmethod
    def __classcall_private__(cls, ambient, gens, category=None):
        """
        Normalize input to ensure a unique representation.

        EXAMPLES::

            sage: L.<X,Y> = LieAlgebra(QQ, {('X','Y'): {'X': 1}})
            sage: S1 = L.subalgebra(X)
            sage: S2 = L.subalgebra((X,))
            sage: S3 = L.subalgebra([X])
            sage: S1 is S2 and S2 is S3
            True
        """
        if not isinstance(gens, (list, tuple)):
            gens = [gens]
        gens = tuple(ambient(gen) for gen in gens)

        gens = tuple(gens)
        if len(gens) == 0:
            gens = (ambient.zero(),)

        if isinstance(ambient, LieSubalgebra_finite_dimensional_with_basis):
            # a nested subalgebra is a subalgebra
            gens = tuple(ambient.lift(gen) for gen in gens)
            ambient = ambient.ambient()

        cat = LieAlgebras(ambient.base_ring()).FiniteDimensional().WithBasis()
        category = cat.Subobjects().or_subcategory(category)

        sup = super(LieSubalgebra_finite_dimensional_with_basis, cls)
        return sup.__classcall__(cls, ambient, gens, category)

    def __contains__(self, x):
        r"""
        Return ``True`` if ``x`` is an element of ``self``.

        EXAMPLES:

        Elements of the ambient Lie algebra are contained in the subalgebra
        if they are iterated brackets of the generators::

            sage: sc = {('x','y'): {'z': 1}, ('x','z'): {'w': 1}}
            sage: L.<x,y,z,w,u> = LieAlgebra(QQ, sc)
            sage: S = L.subalgebra([x, y])
            sage: z in S
            True
            sage: w in S
            True
            sage: u in S
            False

        TESTS::

            sage: L.<x,y,z> = LieAlgebra(QQ, {('x','y'): {'z': 1}})
            sage: I = L.subalgebra(x)
            sage: I(x) in I
            True

        """
        if x in self.ambient():
            x = self.ambient()(x)
            return x.to_vector() in self.ambient_submodule()
        return super(LieSubset, self).__contains__(x)

    def _element_constructor_(self, x):
        """
        Convert ``x`` into ``self``.

        EXAMPLES:

        Elements of subalgebras are created directly from elements
        of the ambient Lie algebra::

            sage: L.<x,y,z,w> = LieAlgebra(ZZ, {('x','y'): {'z': 1}})
            sage: S = L.subalgebra([x, y])
            sage: S(y)
            y
            sage: S(y).parent()
            Subalgebra generated by (x, y) of Lie algebra on 4 generators (x, y, z, w) over Integer Ring

        A vector of length equal to the dimension of the subalgebra is
        interpreted as a coordinate vector::

            sage: S(vector(ZZ, [2,3,5]))
            2*x + 3*y + 5*z
        """
        if x in self.module():
            return self.from_vector(x)

        return super(LieSubalgebra_finite_dimensional_with_basis, self)._element_constructor_(x)

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLES::

            sage: L.<X,Y> = LieAlgebra(QQ, abelian=True)
            sage: L.subalgebra([X, Y])
            Subalgebra generated by (X, Y) of Abelian Lie algebra on 2 generators (X, Y) over Rational Field
        """
        gens = self.gens()
        if len(gens) == 1:
            gens = gens[0]
        return "Subalgebra generated by %s of %s" % (gens, self.ambient())

    def retract(self, X):
        r"""
        Retract ``X`` to ``self``.

        INPUT:

        - ``X`` -- an element of the ambient Lie algebra

        EXAMPLES:

        Retraction to a subalgebra of a free nilpotent Lie algebra::

            sage: L = LieAlgebra(QQ, 3, step=2)
            sage: L.inject_variables()
            Defining X_1, X_2, X_3, X_12, X_13, X_23
            sage: S = L.subalgebra([X_1, X_2])
            sage: el = S.retract(2*X_1 + 3*X_2 + 5*X_12); el
            2*X_1 + 3*X_2 + 5*X_12
            sage: el.parent()
            Subalgebra generated by (X_1, X_2) of Free Nilpotent Lie algebra on
            6 generators (X_1, X_2, X_3, X_12, X_13, X_23) over Rational Field

        Retraction raises an error if the element is not contained in the
        subalgebra::

            sage: S.retract(X_3)
            Traceback (most recent call last):
            ...
            ValueError: the element X_3 is not in Subalgebra generated
            by (X_1, X_2) of Free Nilpotent Lie algebra on 6 generators
            (X_1, X_2, X_3, X_12, X_13, X_23) over Rational Field
        """
        if X not in self:
            raise ValueError("the element %s is not in %s" % (X, self))

        sup = super(LieSubalgebra_finite_dimensional_with_basis, self)
        return sup.retract(X)

    @cached_method
    def basis(self):
        r"""
        Return a basis of ``self``.

        EXAMPLES:

            sage: sc = {('x','y'): {'z': 1}, ('x','z'): {'w': 1}}
            sage: L.<x,y,z,w> = LieAlgebra(QQ, sc)
            sage: L.subalgebra([x + y, z + w]).basis()
            Family (x + y, z, w)
        """
        L = self.ambient()
        m = L.module()
        sm = m.submodule([X.to_vector() for X in self.gens()])
        d = 0

        while sm.dimension() > d:
            d = sm.dimension()
            SB = sm.basis()
            sm = m.submodule(sm.basis() +
                             [L.bracket(v, w).to_vector()
                              for v in SB for w in SB])

        return Family(self.element_class(self, L.from_vector(v))
                      for v in sm.echelonized_basis())

    def from_vector(self, v):
        r"""
        Return the element of ``self`` corresponding to the vector ``v``

        INPUT:

        - ``v`` -- a vector in ``self.module()`` or ``self.ambient().module()``

        EXAMPLES:

        An element from a vector of the intrinsic module::

            sage: L.<X,Y,Z> = LieAlgebra(ZZ, abelian=True)
            sage: L.dimension()
            3
            sage: S = L.subalgebra([X, Y])
            sage: S.dimension()
            2
            sage: el = S.from_vector([1, 2]); el
            X + 2*Y
            sage: el.parent() == S
            True

        An element from a vector of the ambient module

            sage: el = S.from_vector([1, 2, 0]); el
            X + 2*Y
            sage: el.parent() == S
            True
        """
        if len(v) == self.ambient().dimension():
            return self.retract(self.ambient().from_vector(v))

        sup = super(LieSubalgebra_finite_dimensional_with_basis, self)
        return sup.from_vector(v)

    def basis_matrix(self):
        r"""
        Return the basis matrix of ``self`` as a submodule
        of the ambient Lie algebra.

        EXAMPLES::

            sage: L.<X,Y,Z> = LieAlgebra(ZZ, {('X','Y'): {'Z': 3}})
            sage: S1 = L.subalgebra([4*X + Y, Y])
            sage: S1.basis_matrix()
            [ 4  0  0]
            [ 0  1  0]
            [ 0  0 12]
            sage: K.<X,Y,Z> = LieAlgebra(QQ, {('X','Y'): {'Z': 3}})
            sage: S2 = K.subalgebra([4*X + Y, Y])
            sage: S2.basis_matrix()
            [1 0 0]
            [0 1 0]
            [0 0 1]
        """
        return self.ambient_submodule().basis_matrix()

    @cached_method
    def ambient_submodule(self):
        r"""
        Return the submodule of the ambient Lie algebra
        corresponding to ``self``.

        EXAMPLES::

            sage: L.<X,Y,Z> = LieAlgebra(ZZ, {('X','Y'): {'Z': 3}})
            sage: S = L.subalgebra([X, Y])
            sage: S.ambient_submodule()
            Sparse free module of degree 3 and rank 3 over Integer Ring
            User basis matrix:
            [1 0 0]
            [0 1 0]
            [0 0 3]
        """
        m = self.ambient().module()
        ambientbasis = [self.lift(X).to_vector() for X in self.basis()]
        return m.submodule_with_basis(ambientbasis)

    class Element(LieSubset.Element):

        def __getitem__(self, i):
            r"""
            Return the coefficient of ``self`` indexed by ``i``.

            EXAMPLES::

                sage: L.<X,Y,Z> = LieAlgebra(QQ, {('X','Y'): {'Z': 1}})
                sage: S = L.subalgebra([X, Y])
                sage: el = S(2*Y + 9*Z)
                sage: el[1]
                2
                sage: el[2]
                9
            """
            return self.monomial_coefficients()[i]

        def to_vector(self):
            r"""
            Return the vector in ``g.module()`` corresponding to the
            element ``self`` of ``g`` (where ``g`` is the parent of
            ``self``).

            EXAMPLES::

                sage: L.<X,Y,Z> = LieAlgebra(ZZ, {('X','Y'): {'Z': 3}})
                sage: S = L.subalgebra([X, Y])
                sage: S.basis()
                Family (X, Y, 3*Z)
                sage: S(2*Y + 9*Z).to_vector()
                (0, 2, 3)
            """
            sm = self.parent().ambient_submodule()
            return sm.coordinate_vector(self.parent().lift(self).to_vector())

        def monomial_coefficients(self, copy=True):
            r"""
            Return a dictionary whose keys are indices of basis elements
            in the support of ``self`` and whose values are the
            corresponding coefficients.

            INPUT:

            - ``copy`` -- (default: ``True``) if ``self`` is internally
              represented by a dictionary ``d``, then make a copy of ``d``;
              if ``False``, then this can cause undesired behavior by
              mutating ``d``

            EXAMPLES::

                sage: L.<X,Y,Z> = LieAlgebra(ZZ, {('X','Y'): {'Z': 3}})
                sage: S = L.subalgebra([X, Y])
                sage: S(2*Y + 9*Z).monomial_coefficients()
                {0: 0, 1: 2, 2: 3}
            """
            v = self.to_vector()
            return dict(zip(range(len(v)), v))
