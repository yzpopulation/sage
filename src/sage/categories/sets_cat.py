r"""
Sets
"""
# ****************************************************************************
#  Copyright (C) 2005      David Kohel <kohel@maths.usyd.edu>
#                          William Stein <wstein@math.ucsd.edu>
#                2008      Teresa Gomez-Diaz (CNRS) <Teresa.Gomez-Diaz@univ-mlv.fr>
#                2008-2014 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  https://www.gnu.org/licenses/
# *****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.misc.sage_unittest import TestSuite
from sage.misc.abstract_method import abstract_method
from sage.misc.lazy_attribute import lazy_attribute
from sage.misc.lazy_import import lazy_import, LazyImport
from sage.misc.lazy_format import LazyFormat
from sage.categories.category import Category
from sage.categories.category_singleton import Category_singleton
# Do not use sage.categories.all here to avoid initialization loop
from sage.categories.sets_with_partial_maps import SetsWithPartialMaps
from sage.categories.subquotients import SubquotientsCategory
from sage.categories.quotients import QuotientsCategory
from sage.categories.subobjects import SubobjectsCategory
from sage.categories.isomorphic_objects import IsomorphicObjectsCategory
from sage.categories.algebra_functor import AlgebrasCategory
from sage.categories.cartesian_product import CartesianProductsCategory, CartesianProductFunctor
from sage.categories.realizations import RealizationsCategory, Category_realization_of_parent
from sage.categories.with_realizations import WithRealizationsCategory
from sage.categories.category_with_axiom import CategoryWithAxiom
lazy_import('sage.sets.cartesian_product', 'CartesianProduct')


def print_compare(x, y):
    """
    Helper method used in
    :meth:`Sets.ParentMethods._test_elements_eq_symmetric`,
    :meth:`Sets.ParentMethods._test_elements_eq_tranisitive`.

    INPUT:

    - ``x`` -- an element

    - ``y`` -- an element

    EXAMPLES::

        sage: from sage.categories.sets_cat import print_compare
        sage: print_compare(1,2)
        1 != 2
        sage: print_compare(1,1)
        1 == 1

    """
    if x == y:
        return LazyFormat("%s == %s") % (x, y)
    else:
        return LazyFormat("%s != %s") % (x, y)


class EmptySetError(ValueError):
    """
    Exception raised when some operation can't be performed on the empty set.

    EXAMPLES::

        sage: def first_element(st):
        ....:  if not st: raise EmptySetError("no elements")
        ....:  else: return st[0]
        sage: first_element(Set((1,2,3)))
        1
        sage: first_element(Set([]))
        Traceback (most recent call last):
        ...
        EmptySetError: no elements
    """
    pass


class Sets(Category_singleton):
    r"""
    The category of sets.

    The base category for collections of elements with = (equality).

    This is also the category whose objects are all parents.

    EXAMPLES::

        sage: Sets()
        Category of sets
        sage: Sets().super_categories()
        [Category of sets with partial maps]
        sage: Sets().all_super_categories()
        [Category of sets, Category of sets with partial maps, Category of objects]

    Let us consider an example of set::

        sage: P = Sets().example("inherits")
        sage: P
        Set of prime numbers

    See ``P??`` for the code.


    P is in the category of sets::

        sage: P.category()
        Category of sets

    and therefore gets its methods from the following classes::

        sage: for cl in P.__class__.mro(): print(cl)
        <class 'sage.categories.examples.sets_cat.PrimeNumbers_Inherits_with_category'>
        <class 'sage.categories.examples.sets_cat.PrimeNumbers_Inherits'>
        <class 'sage.categories.examples.sets_cat.PrimeNumbers_Abstract'>
        <class 'sage.structure.unique_representation.UniqueRepresentation'>
        <class 'sage.structure.unique_representation.CachedRepresentation'>
        <type 'sage.misc.fast_methods.WithEqualityById'>
        <type 'sage.structure.parent.Parent'>
        <type 'sage.structure.category_object.CategoryObject'>
        <type 'sage.structure.sage_object.SageObject'>
        <class 'sage.categories.sets_cat.Sets.parent_class'>
        <class 'sage.categories.sets_with_partial_maps.SetsWithPartialMaps.parent_class'>
        <class 'sage.categories.objects.Objects.parent_class'>
        <... 'object'>

    We run some generic checks on P::

        sage: TestSuite(P).run(verbose=True)
        running ._test_an_element() . . . pass
        running ._test_cardinality() . . . pass
        running ._test_category() . . . pass
        running ._test_construction() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_new() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_new() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_pickling() . . . pass
        running ._test_some_elements() . . . pass

    Now, we manipulate some elements of P::

        sage: P.an_element()
        47
        sage: x = P(3)
        sage: x.parent()
        Set of prime numbers
        sage: x in P, 4 in P
        (True, False)
        sage: x.is_prime()
        True

    They get their methods from the following classes::

        sage: for cl in x.__class__.mro(): print(cl)
        <class 'sage.categories.examples.sets_cat.PrimeNumbers_Inherits_with_category.element_class'>
        <class 'sage.categories.examples.sets_cat.PrimeNumbers_Inherits.Element'>
        <type 'sage.rings.integer.IntegerWrapper'>
        <type 'sage.rings.integer.Integer'>
        <type 'sage.structure.element.EuclideanDomainElement'>
        <type 'sage.structure.element.PrincipalIdealDomainElement'>
        <type 'sage.structure.element.DedekindDomainElement'>
        <type 'sage.structure.element.IntegralDomainElement'>
        <type 'sage.structure.element.CommutativeRingElement'>
        <type 'sage.structure.element.RingElement'>
        <type 'sage.structure.element.ModuleElement'>
        <class 'sage.categories.examples.sets_cat.PrimeNumbers_Abstract.Element'>
        <type 'sage.structure.element.Element'>
        <type 'sage.structure.sage_object.SageObject'>
        <class 'sage.categories.sets_cat.Sets.element_class'>
        <class 'sage.categories.sets_with_partial_maps.SetsWithPartialMaps.element_class'>
        <class 'sage.categories.objects.Objects.element_class'>
        <... 'object'>

    FIXME: Objects.element_class is not very meaningful ...


    TESTS::

          sage: TestSuite(Sets()).run()

    """

    def super_categories(self):
        r"""
        We include SetsWithPartialMaps between Sets and Objects so that we
        can define morphisms between sets that are only partially defined.
        This is also to have the Homset constructor not complain that
        SetsWithPartialMaps is not a supercategory of Fields, for example.

        EXAMPLES::

            sage: Sets().super_categories()
            [Category of sets with partial maps]
        """
        return [SetsWithPartialMaps()]

    def _call_(self, X, enumerated_set=False):
        r"""
        Construct an object in this category from the data ``X``.

        INPUT:

        - ``X`` -- an object to be converted into a set

        - ``enumerated_set`` -- if set to ``True`` and the input is either a
          Python tuple or a Python list then the output will be a finite
          enumerated set.

        EXAMPLES::

            sage: Sets()(ZZ)
            Integer Ring
            sage: Sets()([1, 2, 3])
            {1, 2, 3}

            sage: S = Sets()([1, 2, 3]); S.category()
            Category of finite sets
            sage: S = Sets()([1, 2, 3], enumerated_set=True); S.category()
            Category of facade finite enumerated sets

        .. NOTE::

           Using ``Sets()(A)`` used to implement some sort of forgetful functor
           into the ``Sets()`` category. This feature has been removed, because
           it was not consistent with the semantic of :meth:`Category.__call__`.
           Proper forgetful functors will eventually be implemented, with
           another syntax.
        """
        if enumerated_set and type(X) in (tuple, list, range):
            from sage.categories.enumerated_sets import EnumeratedSets
            return EnumeratedSets()(X)
        from sage.sets.set import Set
        return Set(X)

    def example(self, choice=None):
        """
        Return examples of objects of ``Sets()``, as per
        :meth:`Category.example()
        <sage.categories.category.Category.example>`.

        EXAMPLES::

            sage: Sets().example()
            Set of prime numbers (basic implementation)

            sage: Sets().example("inherits")
            Set of prime numbers

            sage: Sets().example("facade")
            Set of prime numbers (facade implementation)

            sage: Sets().example("wrapper")
            Set of prime numbers (wrapper implementation)
        """
        if choice is None:
            from sage.categories.examples.sets_cat import PrimeNumbers
            return PrimeNumbers()
        elif choice == "inherits":
            from sage.categories.examples.sets_cat import PrimeNumbers_Inherits
            return PrimeNumbers_Inherits()
        elif choice == "facade":
            from sage.categories.examples.sets_cat import PrimeNumbers_Facade
            return PrimeNumbers_Facade()
        elif choice == "wrapper":
            from sage.categories.examples.sets_cat import PrimeNumbers_Wrapper
            return PrimeNumbers_Wrapper()
        else:
            raise ValueError("unknown choice")

    class SubcategoryMethods:

        @cached_method
        def CartesianProducts(self):
            r"""
            Return the full subcategory of the objects of ``self``
            constructed as Cartesian products.

            .. SEEALSO::

                - :class:`.cartesian_product.CartesianProductFunctor`
                - :class:`~.covariant_functorial_construction.RegressiveCovariantFunctorialConstruction`

            EXAMPLES::

                sage: Sets().CartesianProducts()
                Category of Cartesian products of sets
                sage: Semigroups().CartesianProducts()
                Category of Cartesian products of semigroups
                sage: EuclideanDomains().CartesianProducts()
                Category of Cartesian products of commutative rings
            """
            return CartesianProductsCategory.category_of(self)

        @cached_method
        def Subquotients(self):
            r"""
            Return the full subcategory of the objects of ``self``
            constructed as subquotients.

            Given a concrete category ``self == As()`` (i.e. a subcategory
            of ``Sets()``), ``As().Subquotients()`` returns the category
            of objects of ``As()`` endowed with a distinguished
            description as subquotient of some other object of ``As()``.

            EXAMPLES::

                sage: Monoids().Subquotients()
                Category of subquotients of monoids

            A parent `A` in ``As()`` is further in
            ``As().Subquotients()`` if there is a distinguished parent
            `B` in ``As()``, called the *ambient set*, a subobject
            `B'` of `B`, and a pair of maps:

            .. MATH::

                l: A \to B'  \text{ and }  r: B' \to A

            called respectively the *lifting map* and *retract map*
            such that `r \circ l` is the identity of `A` and `r` is a
            morphism in ``As()``.

            .. TODO:: Draw the typical commutative diagram.

            It follows that, for each operation `op` of the category,
            we have some property like:

            .. MATH::

                op_A(e) = r(op_B(l(e))), \text{ for all } e\in A

            This allows for implementing the operations on `A` from
            those on `B`.

            The two most common use cases are:

             - *homomorphic images* (or *quotients*), when `B'=B`,
               `r` is an homomorphism from `B` to `A` (typically a
               canonical quotient map), and `l` a section of it (not
               necessarily a homomorphism); see :meth:`Quotients`;

             - *subobjects* (up to an isomorphism), when `l` is an
               embedding from `A` into `B`; in this case, `B'` is
               typically isomorphic to `A` through the inverse
               isomorphisms `r` and `l`; see :meth:`Subobjects`;

            .. NOTE::

                - The usual definition of "subquotient"
                  (:wikipedia:`Subquotient`) does not involve the
                  lifting map `l`. This map is required in Sage's
                  context to make the definition constructive. It is
                  only used in computations and does not affect their
                  results. This is relatively harmless since the
                  category is a concrete category (i.e., its objects
                  are sets and its morphisms are set maps).

                - In mathematics, especially in the context of
                  quotients, the retract map `r` is often referred to
                  as a *projection map* instead.

                - Since `B'` is not specified explicitly, it is
                  possible to abuse the framework with situations
                  where `B'` is not quite a subobject and `r` not
                  quite a morphism, as long as the lifting and retract
                  maps can be used as above to compute all the
                  operations in `A`. Use at your own risk!

            Assumptions:

            - For any category ``As()``, ``As().Subquotients()`` is a
              subcategory of ``As()``.

              Example: a subquotient of a group is a group (e.g., a left
              or right quotient of a group by a non-normal subgroup is
              not in this category).

            - This construction is covariant: if ``As()`` is a
              subcategory of ``Bs()``, then ``As().Subquotients()`` is a
              subcategory of ``Bs().Subquotients()``.

              Example: if `A` is a subquotient of `B` in the category of
              groups, then it is also a subquotient of `B` in the category
              of monoids.

            - If the user (or a program) calls ``As().Subquotients()``,
              then it is assumed that subquotients are well defined in
              this category. This is not checked, and probably never will
              be. Note that, if a category ``As()`` does not specify
              anything about its subquotients, then its subquotient
              category looks like this::

                 sage: EuclideanDomains().Subquotients()
                 Join of Category of euclidean domains
                     and Category of subquotients of monoids

            Interface: the ambient set `B` of `A` is given by
            ``A.ambient()``. The subset `B'` needs not be specified, so
            the retract map is handled as a partial map from `B` to `A`.

            The lifting and retract map are implemented
            respectively as methods ``A.lift(a)`` and ``A.retract(b)``.
            As a shorthand for the former, one can use alternatively
            ``a.lift()``::

                sage: S = Semigroups().Subquotients().example(); S
                An example of a (sub)quotient semigroup: a quotient of the left zero semigroup
                sage: S.ambient()
                An example of a semigroup: the left zero semigroup
                sage: S(3).lift().parent()
                An example of a semigroup: the left zero semigroup
                sage: S(3) * S(1) == S.retract( S(3).lift() * S(1).lift() )
                True

            See ``S?`` for more.

            .. TODO:: use a more interesting example, like `\ZZ/n\ZZ`.

            .. SEEALSO::

                - :meth:`Quotients`, :meth:`Subobjects`, :meth:`IsomorphicObjects`
                - :class:`.subquotients.SubquotientsCategory`
                - :class:`~.covariant_functorial_construction.RegressiveCovariantFunctorialConstruction`

            TESTS::

                sage: TestSuite(Sets().Subquotients()).run()
            """
            return SubquotientsCategory.category_of(self)

        @cached_method
        def Quotients(self):
            r"""
            Return the full subcategory of the objects of ``self``
            constructed as quotients.

            Given a concrete category ``As()`` (i.e. a subcategory of
            ``Sets()``), ``As().Quotients()`` returns the category of
            objects of ``As()`` endowed with a distinguished
            description as quotient (in fact homomorphic image) of
            some other object of ``As()``.

            Implementing an object of ``As().Quotients()`` is done in
            the same way as for ``As().Subquotients()``; namely by
            providing an ambient space and a lift and a retract
            map. See :meth:`Subquotients` for detailed instructions.

            .. SEEALSO::

                - :meth:`Subquotients` for background
                - :class:`.quotients.QuotientsCategory`
                - :class:`~.covariant_functorial_construction.RegressiveCovariantFunctorialConstruction`

            EXAMPLES::

                sage: C = Semigroups().Quotients(); C
                Category of quotients of semigroups
                sage: C.super_categories()
                [Category of subquotients of semigroups, Category of quotients of sets]
                sage: C.all_super_categories()
                [Category of quotients of semigroups,
                 Category of subquotients of semigroups,
                 Category of semigroups,
                 Category of subquotients of magmas,
                 Category of magmas,
                 Category of quotients of sets,
                 Category of subquotients of sets,
                 Category of sets,
                 Category of sets with partial maps,
                 Category of objects]

            The caller is responsible for checking that the given category
            admits a well defined category of quotients::

                sage: EuclideanDomains().Quotients()
                Join of Category of euclidean domains
                    and Category of subquotients of monoids
                    and Category of quotients of semigroups

            TESTS::

                sage: TestSuite(C).run()
            """
            return QuotientsCategory.category_of(self)

        @cached_method
        def Subobjects(self):
            r"""
            Return the full subcategory of the objects of ``self``
            constructed as subobjects.

            Given a concrete category ``As()`` (i.e. a subcategory of
            ``Sets()``), ``As().Subobjects()`` returns the category of
            objects of ``As()`` endowed with a distinguished embedding
            into some other object of ``As()``.

            Implementing an object of ``As().Subobjects()`` is done in
            the same way as for ``As().Subquotients()``; namely by
            providing an ambient space and a lift and a retract
            map. In the case of a trivial embedding, the two maps will
            typically be identity maps that just change the parent of
            their argument. See :meth:`Subquotients` for detailed
            instructions.

            .. SEEALSO::

                - :meth:`Subquotients` for background
                - :class:`.subobjects.SubobjectsCategory`
                - :class:`~.covariant_functorial_construction.RegressiveCovariantFunctorialConstruction`

            EXAMPLES::

                sage: C = Sets().Subobjects(); C
                Category of subobjects of sets

                sage: C.super_categories()
                [Category of subquotients of sets]

                sage: C.all_super_categories()
                [Category of subobjects of sets,
                 Category of subquotients of sets,
                 Category of sets,
                 Category of sets with partial maps,
                 Category of objects]

            Unless something specific about subobjects is implemented for this
            category, one actually gets an optimized super category::

                sage: C = Semigroups().Subobjects(); C
                Join of Category of subquotients of semigroups
                    and Category of subobjects of sets

            The caller is responsible for checking that the given category
            admits a well defined category of subobjects.

            TESTS::

                sage: Semigroups().Subobjects().is_subcategory(Semigroups().Subquotients())
                True
                sage: TestSuite(C).run()

            """
            return SubobjectsCategory.category_of(self)

        @cached_method
        def IsomorphicObjects(self):
            r"""
            Return the full subcategory of the objects of ``self``
            constructed by isomorphism.

            Given a concrete category ``As()`` (i.e. a subcategory of
            ``Sets()``), ``As().IsomorphicObjects()`` returns the category of
            objects of ``As()`` endowed with a distinguished description as
            the image of some other object of ``As()`` by an isomorphism in
            this category.

            See :meth:`Subquotients` for background.

            EXAMPLES:

            In the following example, `A` is defined as the image by `x\mapsto
            x^2` of the finite set `B = \{1,2,3\}`::

                sage: A = FiniteEnumeratedSets().IsomorphicObjects().example(); A
                The image by some isomorphism of An example of a finite enumerated set: {1,2,3}

            Since `B` is a finite enumerated set, so is `A`::

                sage: A in FiniteEnumeratedSets()
                True
                sage: A.cardinality()
                3
                sage: A.list()
                [1, 4, 9]

            The isomorphism from `B` to `A` is available as::

                sage: A.retract(3)
                9

            and its inverse as::

                sage: A.lift(9)
                3

            It often is natural to declare those morphisms as coercions so
            that one can do ``A(b)`` and ``B(a)`` to go back and forth between
            `A` and `B` (TODO: refer to a category example where the maps are
            declared as a coercion). This is not done by default. Indeed, in
            many cases one only wants to transport part of the structure of
            `B` to `A`. Assume for example, that one wants to construct the
            set of integers `B=ZZ`, endowed with ``max`` as addition, and
            ``+`` as multiplication instead of the usual ``+`` and ``*``. One
            can construct `A` as isomorphic to `B` as an infinite enumerated
            set. However `A` is *not* isomorphic to `B` as a ring; for
            example, for `a\in A` and `a\in B`, the expressions `a+A(b)` and
            `B(a)+b` give completely different results; hence we would not want
            the expression `a+b` to be implicitly resolved to any one of above
            two, as the coercion mechanism would do.

            Coercions also cannot be used with facade parents (see
            :class:`Sets.Facade`) like in the example above.


            We now look at a category of isomorphic objects::

                sage: C = Sets().IsomorphicObjects(); C
                Category of isomorphic objects of sets

                sage: C.super_categories()
                [Category of subobjects of sets, Category of quotients of sets]

                sage: C.all_super_categories()
                [Category of isomorphic objects of sets,
                 Category of subobjects of sets,
                 Category of quotients of sets,
                 Category of subquotients of sets,
                 Category of sets,
                 Category of sets with partial maps,
                 Category of objects]

            Unless something specific about isomorphic objects is implemented
            for this category, one actually get an optimized super category::

                sage: C = Semigroups().IsomorphicObjects(); C
                Join of Category of quotients of semigroups
                    and Category of isomorphic objects of sets

            .. SEEALSO::

                - :meth:`Subquotients` for background
                - :class:`.isomorphic_objects.IsomorphicObjectsCategory`
                - :class:`~.covariant_functorial_construction.RegressiveCovariantFunctorialConstruction`

            TESTS::

                sage: TestSuite(Sets().IsomorphicObjects()).run()
            """
            return IsomorphicObjectsCategory.category_of(self)

        @cached_method
        def Topological(self):
            """
            Return the subcategory of the topological objects of ``self``.

            TESTS::

                sage: TestSuite(Sets().Topological()).run()
            """
            from sage.categories.topological_spaces import TopologicalSpacesCategory
            return TopologicalSpacesCategory.category_of(self)

        @cached_method
        def Metric(self):
            """
            Return the subcategory of the metric objects of ``self``.

            TESTS::

                sage: TestSuite(Sets().Metric()).run()
            """
            from sage.categories.metric_spaces import MetricSpacesCategory
            return MetricSpacesCategory.category_of(self)

        @cached_method
        def Algebras(self, base_ring):
            """
            Return the category of objects constructed as algebras of
            objects of ``self`` over ``base_ring``.

            INPUT:

            - ``base_ring`` -- a ring

            See :meth:`Sets.ParentMethods.algebra` for the precise
            meaning in Sage of the *algebra of an object*.

            EXAMPLES::

                sage: Monoids().Algebras(QQ)
                Category of monoid algebras over Rational Field

                sage: Groups().Algebras(QQ)
                Category of group algebras over Rational Field

                sage: AdditiveMagmas().AdditiveAssociative().Algebras(QQ)
                Category of additive semigroup algebras over Rational Field

                sage: Monoids().Algebras(Rings())
                Category of monoid algebras over Category of rings

            .. SEEALSO::

                - :class:`.algebra_functor.AlgebrasCategory`
                - :class:`~.covariant_functorial_construction.CovariantFunctorialConstruction`

            TESTS::

                sage: TestSuite(Groups().Finite().Algebras(QQ)).run()
            """
            from sage.categories.rings import Rings
            assert base_ring in Rings() or (isinstance(base_ring, Category)
                                            and base_ring.is_subcategory(Rings()))
            return AlgebrasCategory.category_of(self, base_ring)

        @cached_method
        def Finite(self):
            """
            Return the full subcategory of the finite objects of ``self``.

            EXAMPLES::

                sage: Sets().Finite()
                Category of finite sets
                sage: Rings().Finite()
                Category of finite rings

            TESTS::

                sage: TestSuite(Sets().Finite()).run()
                sage: Rings().Finite.__module__
                'sage.categories.sets_cat'
            """
            return self._with_axiom('Finite')

        @cached_method
        def Infinite(self):
            """
            Return the full subcategory of the infinite objects of ``self``.

            EXAMPLES::

                sage: Sets().Infinite()
                Category of infinite sets
                sage: Rings().Infinite()
                Category of infinite rings

            TESTS::

                sage: TestSuite(Sets().Infinite()).run()
                sage: Rings().Infinite.__module__
                'sage.categories.sets_cat'
            """
            return self._with_axiom('Infinite')

        @cached_method
        def Enumerated(self):
            """
            Return the full subcategory of the enumerated objects of ``self``.

            An enumerated object can be iterated to get its elements.

            EXAMPLES::

                sage: Sets().Enumerated()
                Category of enumerated sets
                sage: Rings().Finite().Enumerated()
                Category of finite enumerated rings
                sage: Rings().Infinite().Enumerated()
                Category of infinite enumerated rings

            TESTS::

                sage: TestSuite(Sets().Enumerated()).run()
                sage: Rings().Enumerated.__module__
                'sage.categories.sets_cat'
            """
            return self._with_axiom('Enumerated')

        def Facade(self):
            r"""
            Return the full subcategory of the facade objects of ``self``.

            .. _facade-sets:

            .. RUBRIC:: What is a facade set?

            Recall that, in Sage, :ref:`sets are modelled by *parents*
            <category-primer-parents-elements-categories>`, and their
            elements know which distinguished set they belong to. For
            example, the ring of integers `\ZZ` is modelled by the
            parent :obj:`ZZ`, and integers know that they belong to
            this set::

                sage: ZZ
                Integer Ring
                sage: 42.parent()
                Integer Ring

            Sometimes, it is convenient to represent the elements of a
            parent ``P`` by elements of some other parent. For
            example, the elements of the set of prime numbers are
            represented by plain integers::

                sage: Primes()
                Set of all prime numbers: 2, 3, 5, 7, ...
                sage: p = Primes().an_element(); p
                43
                sage: p.parent()
                Integer Ring

            In this case, ``P`` is called a *facade set*.

            This feature is advertised through the category of `P`::

                sage: Primes().category()
                Category of facade infinite enumerated sets
                sage: Sets().Facade()
                Category of facade sets

            Typical use cases include modeling a subset of an existing
            parent::

                sage: Set([4,6,9])                    # random
                {4, 6, 9}
                sage: Sets().Facade().example()
                An example of facade set: the monoid of positive integers

            or the union of several parents::

                sage: Sets().Facade().example("union")
                An example of a facade set: the integers completed by +-infinity

            or endowing an existing parent with more (or less!)
            structure::

                sage: Posets().example("facade")
                An example of a facade poset: the positive integers ordered by divisibility

            Let us investigate in detail a close variant of this last
            example: let `P` be set of divisors of `12` partially
            ordered by divisibility. There are two options for
            representing its elements:

            1. as plain integers::

                sage: P = Poset((divisors(12), attrcall("divides")), facade=True)

            2. as integers, modified to be aware that their parent is `P`::

                sage: Q = Poset((divisors(12), attrcall("divides")), facade=False)

            The advantage of option 1. is that one needs not do
            conversions back and forth between `P` and `\ZZ`. The
            disadvantage is that this introduces an ambiguity when
            writing `2 < 3`: does this compare `2` and `3` w.r.t. the
            natural order on integers or w.r.t. divisibility?::

                sage: 2 < 3
                True

            To raise this ambiguity, one needs to explicitly specify
            the underlying poset as in `2 <_P 3`::

                sage: P = Posets().example("facade")
                sage: P.lt(2,3)
                False

            On the other hand, with option 2. and once constructed,
            the elements know unambiguously how to compare
            themselves::

                sage: Q(2) < Q(3)
                False
                sage: Q(2) < Q(6)
                True

            Beware that ``P(2)`` is still the integer `2`. Therefore
            ``P(2) < P(3)`` still compares `2` and `3` as integers!::

                sage: P(2) < P(3)
                True

            In short `P` being a facade parent is one of the programmatic
            counterparts (with e.g. coercions) of the usual mathematical idiom:
            "for ease of notation, we identify an element of `P` with the
            corresponding integer". Too many identifications lead to
            confusion; the lack thereof leads to heavy, if not obfuscated,
            notations. Finding the right balance is an art, and even though
            there are common guidelines, it is ultimately up to the writer to
            choose which identifications to do. This is no different in code.

            .. SEEALSO::

               The following examples illustrate various ways to
               implement subsets like the set of prime numbers; look
               at their code for details::

                   sage: Sets().example("facade")
                   Set of prime numbers (facade implementation)
                   sage: Sets().example("inherits")
                   Set of prime numbers
                   sage: Sets().example("wrapper")
                   Set of prime numbers (wrapper implementation)

            .. RUBRIC:: Specifications

            A parent which is a facade must either:

            - call :meth:`Parent.__init__` using the ``facade`` parameter to
              specify a parent, or tuple thereof.
            - overload the method :meth:`~Sets.Facade.ParentMethods.facade_for`.

            .. NOTE::

                The concept of facade parents was originally introduced
                in the computer algebra system MuPAD.

            TESTS:

            Check that multiple categories initialisation
            works (:trac:`13801`)::

                sage: class A(Parent):
                ....:   def __init__(self):
                ....:       Parent.__init__(self, category=(FiniteEnumeratedSets(),Monoids()), facade=True)
                sage: a = A()

                sage: Posets().Facade()
                Category of facade posets
                sage: Posets().Facade().Finite() is  Posets().Finite().Facade()
                True
            """
            return self._with_axiom('Facade')

    class ParentMethods:
        # TODO: simplify the _element_constructor_ definition logic
        # TODO: find a nicer mantra for conditionally defined methods
        @lazy_attribute
        def _element_constructor_(self):
            r"""
            TESTS::

                sage: S = Sets().example()
                sage: S._element_constructor_(17)
                17
                sage: S(17) # indirect doctest
                17

                sage: A = FreeModule(QQ, 3)
                sage: A.element_class
                <type 'sage.modules.vector_rational_dense.Vector_rational_dense'>
                sage: A._element_constructor_
                <bound method FreeModule_ambient_field_with_category._element_constructor_ of Vector space of dimension 3 over Rational Field>

                sage: B = SymmetricGroup(3).algebra(ZZ)
                sage: B.element_class
                <...SymmetricGroupAlgebra_n_with_category.element_class'>
                sage: B._element_constructor_
                <bound method SymmetricGroupAlgebra_n_with_category._element_constructor_
                of Symmetric group algebra of order 3 over Integer Ring>
            """
            if hasattr(self, "element_class"):
                return self._element_constructor_from_element_class
            else:
                return NotImplemented

        def _element_constructor_from_element_class(self, *args, **keywords):
            """
            The default constructor for elements of this parent ``self``.

            Among other things, it is called upon ``self(data)`` when
            the coercion model did not find a way to coerce ``data`` into
            this parent.

            This default implementation for
            :meth:`_element_constructor_` calls the constructor of the
            element class, passing ``self`` as first argument.

            EXAMPLES::

                sage: S = Sets().example("inherits")
                sage: s = S._element_constructor_from_element_class(17); s
                17
                sage: type(s)
                <class 'sage.categories.examples.sets_cat.PrimeNumbers_Inherits_with_category.element_class'>
            """
            return self.element_class(self, *args, **keywords)

        def is_parent_of(self, element):
            """
            Return whether ``self`` is the parent of ``element``.

            INPUT:

            - ``element`` -- any object

            EXAMPLES::

                sage: S = ZZ
                sage: S.is_parent_of(1)
                True
                sage: S.is_parent_of(2/1)
                False

            This method differs from :meth:`__contains__` because it
            does not attempt any coercion::

                sage: 2/1 in S, S.is_parent_of(2/1)
                (True, False)
                sage: int(1) in S, S.is_parent_of(int(1))
                (True, False)
            """
            from sage.structure.element import parent
            return parent(element) == self

        @abstract_method
        def __contains__(self, x):
            """
            Test whether the set ``self`` contains the object ``x``.

            All parents in the category ``Sets()`` should implement this method.

            EXAMPLES::

                sage: P = Sets().example(); P
                Set of prime numbers (basic implementation)
                sage: 12 in P
                False
                sage: P(5) in P
                True
            """

        @cached_method
        def an_element(self):
            r"""
            Return a (preferably typical) element of this parent.

            This is used both for illustration and testing purposes. If the
            set ``self`` is empty, :meth:`an_element` should raise the exception
            :class:`EmptySetError`.

            This default implementation calls :meth:`_an_element_` and
            caches the result. Any parent should implement either
            :meth:`an_element` or :meth:`_an_element_`.

            EXAMPLES::

               sage: CDF.an_element()
               1.0*I
               sage: ZZ[['t']].an_element()
               t
            """
            return self._an_element_()

        def _test_an_element(self, **options):
            """
            Run generic tests on the method :meth:`.an_element`.

            See also: :class:`TestSuite`.

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_an_element()

            Let us now write a broken :meth:`.an_element` method::

                sage: from sage.categories.examples.sets_cat import PrimeNumbers
                sage: class CCls(PrimeNumbers):
                ....:     def an_element(self):
                ....:         return 18
                sage: CC = CCls()
                sage: CC._test_an_element()
                Traceback (most recent call last):
                ...
                AssertionError: self.an_element() is not in self

            TESTS::

                sage: FiniteEnumeratedSet([])._test_an_element()
            """
            tester = self._tester(**options)
            try:
                an_element = self.an_element()
            except EmptySetError:
                return
            tester.assertTrue(an_element in self, "self.an_element() is not in self")
#            tester.assertTrue(self.is_parent_of(an_element), "self is not the parent of self.an_element()")
#            tester.assertEqual(self(an_element), an_element, "element construction is not idempotent")
            if self.is_parent_of(an_element):
                tester.assertEqual(self(an_element), an_element, "element construction is not idempotent")
            else: # Allows self(an_element) to fails for facade parent.
                try:
                    rebuilt_element = self(an_element)
                except NotImplementedError:
                    tester.info("\n  The set doesn't seems to implement __call__; skipping test of construction idempotency")
                else:
                    tester.assertEqual(rebuilt_element, an_element, "element construction is not idempotent")

        def _test_elements(self, tester=None, **options):
            """
            Run generic tests on element(s) of ``self``.

            See also: :class:`TestSuite`.

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_elements(verbose = True)
                <BLANKLINE>
                  Running the test suite of self.an_element()
                  running ._test_category() . . . pass
                  running ._test_eq() . . . pass
                  running ._test_new() . . . pass
                  running ._test_nonzero_equal() . . . pass
                  running ._test_not_implemented_methods() . . . pass
                  running ._test_pickling() . . . pass
                <BLANKLINE>

            Debugging tip: in case of failure of this test, run instead::

                sage: TestSuite(C.an_element()).run()

            Let us now implement a parent whose elements cannot be pickled::

                sage: from sage.categories.examples.sets_cat import PrimeNumbers
                sage: class Bla(SageObject): pass
                sage: class CCls(PrimeNumbers):
                ....:     def an_element(self):
                ....:         return Bla()
                sage: CC = CCls()
                sage: CC._test_elements()
                Failure in _test_pickling:
                ...
                The following tests failed: _test_pickling
            """
            # TODO: add native support for nested test suites to TestSuite

            # The intention is to raise an exception only if this is
            # run as a sub-testsuite of a larger testsuite.
            is_sub_testsuite = (tester is not None)
            tester = self._tester(tester = tester, **options)
            # Or do we want to run the test on some_elements?
            try:
                an_element = self.an_element()
            except EmptySetError:
                return
            tester.info("\n  Running the test suite of self.an_element()")
            TestSuite(an_element).run(verbose = tester._verbose, prefix = tester._prefix+"  ",
                                      raise_on_failure = is_sub_testsuite)
            tester.info(tester._prefix+" ", newline = False)

        def _test_elements_eq_reflexive(self, **options):
            """
            Run generic tests on the equality of elements.

            Test that ``==`` is reflexive.

            See also: :class:`TestSuite`.

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_elements_eq_reflexive()

            We try a non-reflexive equality::

                sage: P = Sets().example("wrapper")
                sage: P._test_elements_eq_reflexive()
                sage: eq = P.element_class.__eq__

                sage: P.element_class.__eq__ = (lambda x, y:
                ....:      False if eq(x, P(47)) and eq(y, P(47)) else eq(x, y))
                sage: P._test_elements_eq_reflexive()
                Traceback (most recent call last):
                ...
                AssertionError: 47 != 47

            We restore ``P.element_class`` in a proper state for further tests::

                sage: P.element_class.__eq__ = eq

            """
            tester = self._tester(**options)
            S = list(tester.some_elements()) + [None, 0]
            for x in S:
                tester.assertEqual(x, x)

        def _test_elements_eq_symmetric(self, **options):
            """
            Run generic tests on the equality of elements.

            This tests that ``==`` is symmetric.

            See also: :class:`TestSuite`.

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_elements_eq_symmetric()

            We test a non symmetric equality::

                sage: P = Sets().example("wrapper")
                sage: P._test_elements_eq_symmetric()
                sage: eq = P.element_class.__eq__

                sage: def non_sym_eq(x, y):
                ....:    if not y in P:                      return False
                ....:    elif eq(x, P(47)) and eq(y, P(53)): return True
                ....:    else:                               return eq(x, y)
                sage: P.element_class.__eq__ = non_sym_eq
                sage: P._test_elements_eq_symmetric()
                Traceback (most recent call last):
                ...
                AssertionError: non symmetric equality: 47 == 53 but 53 != 47

            We restore ``P.element_class`` in a proper state for further tests::

                sage: P.element_class.__eq__ = eq

            """
            tester = self._tester(**options)
            S = list(tester.some_elements()) + [None, 0]
            from sage.misc.misc import some_tuples
            for x, y in some_tuples(S, 2, tester._max_runs):
                tester.assertEqual(x==y, y==x,
                    LazyFormat("non symmetric equality: %s but %s") % (
                        print_compare(x, y), print_compare(y, x)))

        def _test_elements_eq_transitive(self, **options):
            """
            Run generic tests on the equality of elements.

            Test that ``==`` is transitive.

            See also: :class:`TestSuite`.

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_elements_eq_transitive()

            We test a non transitive equality::

                sage: R = Zp(3)
                sage: test = raw_getattr(Sets().ParentMethods, "_test_elements_eq_transitive")
                sage: test(R, elements=[R(3,2),R(3,1),R(0)])
                Traceback (most recent call last):
                ...
                AssertionError: non transitive equality:
                3 + O(3^2) == O(3) and O(3) == 0 but 3 + O(3^2) != 0

            """
            tester = self._tester(**options)
            S = list(tester.some_elements())
            n = tester._max_runs
            if (len(S)+2)**3 <= n:
                S = list(S) + [None, 0]
            else:
                from random import sample
                from sage.rings.integer import Integer
                S = sample(S, Integer(n).nth_root(3,truncate_mode=1)[0] - 2) + [None, 0]

            for x in S:
                for y in S:
                    if not x == y:
                        continue
                    for z in S:
                        if not y == z:
                            continue
                        tester.assertTrue(x == z,
                            LazyFormat("non transitive equality:\n"
                                       "%s and %s but %s")%(
                                print_compare(x, y),
                                print_compare(y, z),
                                print_compare(x, z)))

        def _test_elements_neq(self, **options):
            """
            Run generic tests on the equality of elements.

            Test that ``==`` and ``!=`` are consistent.

            See also: :class:`TestSuite`.

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_elements_neq()

            We try a broken inequality::

                sage: P = Sets().example("wrapper")
                sage: P._test_elements_neq()
                sage: ne = P.element_class.__ne__
                sage: eq = P.element_class.__eq__

                sage: P.element_class.__ne__ = lambda x, y: False
                sage: P._test_elements_neq()
                Traceback (most recent call last):
                ...
                AssertionError: __eq__ and __ne__ inconsistency:
                  47 == 53 returns False  but  47 != 53 returns False

                sage: P.element_class.__ne__ = lambda x, y: not(x == y)

            We restore ``P.element_class`` in a proper state for further tests::

                sage: P.element_class.__ne__ = ne
                sage: P.element_class.__eq__ = eq
            """
            tester = self._tester(**options)
            S = list(tester.some_elements()) + [None, 0]

            from sage.misc.misc import some_tuples
            for x,y in some_tuples(S, 2, tester._max_runs):
                tester.assertNotEqual(x == y, x != y,
                    LazyFormat("__eq__ and __ne__ inconsistency:\n"
                        "  %s == %s returns %s  but  %s != %s returns %s")%(
                            x, y, (x == y), x, y, (x != y)))

        def some_elements(self):
            """
            Return a list (or iterable) of elements of ``self``.

            This is typically used for running generic tests
            (see :class:`TestSuite`).

            This default implementation calls :meth:`.an_element`.

            EXAMPLES::

                sage: S = Sets().example(); S
                Set of prime numbers (basic implementation)
                sage: S.an_element()
                47
                sage: S.some_elements()
                [47]
                sage: S = Set([])
                sage: S.some_elements()
                []

            This method should return an iterable, *not* an iterator.
            """
            try:
                return [self.an_element()]
            except EmptySetError:
                return []

        def _test_some_elements(self, **options):
            """
            Run generic tests on the method :meth:`.some_elements`.

            .. SEEALSO:: :class:`TestSuite`

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_some_elements()

            Let us now write a broken :meth:`.some_elements` method::

                sage: from sage.categories.examples.sets_cat import *
                sage: class CCls(PrimeNumbers):
                ....:     def some_elements(self):
                ....:         return [self(17), 32]
                sage: CC = CCls()
                sage: CC._test_some_elements()
                Traceback (most recent call last):
                ...
                AssertionError: the object 32 in self.some_elements() is not in self
            """
            tester = self._tester(**options)
            elements = self.some_elements()
            # Todo: enable this once
            #tester.assertTrue(elements != iter(elements),
            #               "self.some_elements() should return an iterable, not an iterator")
            for x in elements:
                tester.assertTrue(x in self, LazyFormat(
                    "the object %s in self.some_elements() is not in self")%(x,))

        #Note: the four methods 'cardinality', 'is_finite_, 'is_empty' and
        # 'random_element' might or might not be implemented in the parent
        # objects. Most of the time a default implementation will be provided by
        # a subcategory of Sets. We do not declare them as optional abstract
        # methods to not pollute the namespace.

        # def cardinality(self)
        # def is_finite(self)
        # def is_empty(self)
        # def random_element(self):

        def _test_cardinality(self, **options):
            r"""
            Run generic test on the method :meth:`.cardinality`.

            EXAMPLES::

                sage: C = Sets().example()
                sage: C._test_cardinality()

            Let us now write a broken :meth:`cardinality` method::

                sage: from sage.categories.examples.sets_cat import *
                sage: class CCls(PrimeNumbers):
                ....:     def cardinality(self):
                ....:         return int(5)
                sage: CC = CCls()
                sage: CC._test_cardinality()
                Traceback (most recent call last):
                ...
                AssertionError: the output of the method cardinality must either
                be a Sage integer or infinity. Not <... 'int'>.
            """
            try:
                cardinality = self.cardinality()
            except (AttributeError,NotImplementedError):
                return
            from sage.structure.element import parent
            from sage.rings.infinity import Infinity
            from sage.rings.integer_ring import ZZ
            tester = self._tester(**options)
            tester.assertTrue(cardinality is Infinity or parent(cardinality) is ZZ,
                    "the output of the method cardinality must either be a Sage integer or infinity. Not {}.".format(type(cardinality)))

        # Functorial constructions

        def construction(self):
            """
            Return a pair ``(functor, parent)`` such that
            ``functor(parent)`` returns ``self``. If ``self`` does
            not have a functorial construction, return ``None``.

            EXAMPLES::

                sage: QQ.construction()
                (FractionField, Integer Ring)
                sage: f, R = QQ['x'].construction()
                sage: f
                Poly[x]
                sage: R
                Rational Field
                sage: f(R)
                Univariate Polynomial Ring in x over Rational Field
            """
            return None

        def _test_construction(self, **options):
            """
            Test that the construction returned by self really yields self.

            :meth:`construction` either returns None or a pair ``(F,O)``,
            and if it returns the latter, then it is supposed that ``F(O)==self`.
            The test verifies this assumption.

            EXAMPLES:

            We create a parent that returns a wrong construction (its construction
            returns the rational field rather than the parent itself)::

                sage: class P(Parent):
                ....:     Element = ElementWrapper
                ....:     def __init__(self):
                ....:         Parent.__init__(self, category=Sets())
                ....:     def __eq__(self, P):
                ....:         return type(self) == type(P)
                ....:     def __hash__(self):
                ....:         return hash(type(self))
                ....:     def construction(self):
                ....:         return sage.categories.pushout.FractionField(), ZZ
                ....:
                sage: import __main__
                sage: __main__.P = P   # this is to enable pickling in doctests
                sage: p = P()
                sage: F,R = p.construction()
                sage: F(R)
                Rational Field
                sage: TestSuite(p).run()
                Failure in _test_construction:
                Traceback (most recent call last):
                ...
                AssertionError: the object's construction does not recreate this object
                ...
                The following tests failed: _test_construction

            If the parent returns the empty construction, the test will not complain::

                sage: ZZ.construction() is None
                True
                sage: TestSuite(ZZ).run()   # indirect doctest

            If the construction works as expected, the test will not complain
            either::

                sage: F,R = QQ.construction()
                sage: F(R) == QQ
                True
                sage: TestSuite(QQ).run()   # indirect doctest

            """
            tester = self._tester(**options)
            FO = self.construction()
            if FO is None:
                return
            tester.assertEqual(FO[0](FO[1]), self, "the object's construction does not recreate this object")

        CartesianProduct = CartesianProduct

        def cartesian_product(*parents, **kwargs):
            """
            Return the Cartesian product of the parents.

            INPUT:

            - ``parents`` -- a list (or other iterable) of parents.

            - ``category`` -- (default: ``None``) the category the
              Cartesian product belongs to. If ``None`` is passed,
              then
              :meth:`~sage.categories.covariant_functorial_construction.CovariantFactorialConstruction.category_from_parents`
              is used to determine the category.

            - ``extra_category`` -- (default: ``None``) a category
              that is added to the Cartesian product in addition
              to the categories obtained from the parents.

            - other keyword arguments will passed on to the class used
              for this Cartesian product (see also
              :class:`~sage.sets.cartesian_product.CartesianProduct`).

            OUTPUT:

            The Cartesian product.

            EXAMPLES::

                sage: C = AlgebrasWithBasis(QQ)
                sage: A = C.example(); A.rename("A")
                sage: A.cartesian_product(A,A)
                A (+) A (+) A
                sage: ZZ.cartesian_product(GF(2), FiniteEnumeratedSet([1,2,3]))
                The Cartesian product of (Integer Ring, Finite Field of size 2, {1, 2, 3})

                sage: C = ZZ.cartesian_product(A); C
                The Cartesian product of (Integer Ring, A)

            TESTS::

                sage: type(C)
                <class 'sage.sets.cartesian_product.CartesianProduct_with_category'>
                sage: C.category()
                Join of Category of rings and ...
                    and Category of Cartesian products of commutative additive groups

            ::

                sage: cartesian_product([ZZ, ZZ], category=Sets()).category()
                Category of sets
                sage: cartesian_product([ZZ, ZZ]).category()
                Join of
                Category of Cartesian products of commutative rings and
                Category of Cartesian products of metric spaces and
                Category of Cartesian products of enumerated sets
                sage: cartesian_product([ZZ, ZZ], extra_category=Posets()).category()
                Join of
                Category of Cartesian products of commutative rings and
                Category of posets and
                Category of Cartesian products of metric spaces and
                Category of Cartesian products of enumerated sets
            """
            category = kwargs.pop('category', None)
            extra_category = kwargs.pop('extra_category', None)

            category = category or cartesian_product.category_from_parents(parents)
            if extra_category:
                if isinstance(category, (list, tuple)):
                    category = tuple(category) + (extra_category,)
                else:
                    category = category & extra_category
            return parents[0].CartesianProduct(parents, category=category, **kwargs)

        def algebra(self, base_ring, category=None, **kwds):
            """
            Return the algebra of ``self`` over ``base_ring``.

            INPUT:

            - ``self`` -- a parent `S`
            - ``base_ring`` -- a ring `K`
            - ``category`` -- a super category of the category
              of `S`, or ``None``

            This returns the space of formal linear combinations of
            elements of `G` with coefficients in `R`, endowed with
            whatever structure can be induced from that of `S`.
            See the documentation of
            :mod:`sage.categories.algebra_functor` for details.

            EXAMPLES:

            If `S` is a :class:`group <Groups>`, the result is its
            group algebra `KS`::

                sage: S = DihedralGroup(4); S
                    Dihedral group of order 8 as a permutation group
                sage: A = S.algebra(QQ); A
                Algebra of Dihedral group of order 8 as a permutation group
                        over Rational Field
                sage: A.category()
                Category of finite group algebras over Rational Field
                sage: a = A.an_element(); a
                () + (1,3) + 2*(1,3)(2,4) + 3*(1,4,3,2)

            This space is endowed with an algebra structure, obtained
            by extending by bilinearity the multiplication of `G` to a
            multiplication on `RG`::

                sage: a * a
                6*() + 4*(2,4) + 3*(1,2)(3,4) + 12*(1,2,3,4) + 2*(1,3)
                 + 13*(1,3)(2,4) + 6*(1,4,3,2) + 3*(1,4)(2,3)

            If `S` is a :class:`monoid <Monoids>`, the result is its
            monoid algebra `KS`::

                sage: S = Monoids().example(); S
                An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
                sage: A = S.algebra(QQ); A
                Algebra of An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
                        over Rational Field
                sage: A.category()
                Category of monoid algebras over Rational Field

            Similarly, we can construct algebras for additive magmas,
            monoids, and groups.

            One may specify for which category one takes the algebra;
            here we build the algebra of the additive group `GF_3`::

                sage: from sage.categories.additive_groups import AdditiveGroups
                sage: S = GF(7)
                sage: A = S.algebra(QQ, category=AdditiveGroups()); A
                Algebra of Finite Field of size 7 over Rational Field
                sage: A.category()
                Category of finite dimensional additive group algebras
                         over Rational Field

                sage: a = A(S(1))
                sage: a
                1
                sage: 1 + a * a * a
                0 + 3

            Note that the ``category`` keyword needs to be fed with
            the structure on `S` to be used, not the induced structure
            on the result.
            """
            if category is None:
                category = self.category()
            from sage.categories.semigroups import Semigroups
            from sage.categories.commutative_additive_semigroups import CommutativeAdditiveSemigroups
            if category.is_subcategory(Semigroups()) and category.is_subcategory(CommutativeAdditiveSemigroups()):
                raise TypeError(
""" `S = {}` is both an additive and a multiplicative semigroup.
Constructing its algebra is ambiguous.
Please use, e.g., S.algebra(QQ, category=Semigroups())""".format(self))
            from sage.categories.groups import Groups
            from sage.categories.additive_groups import AdditiveGroups
            from sage.algebras.group_algebra import GroupAlgebra_class
            algebra_category = category.Algebras(base_ring)
            if (category.is_subcategory(Groups())
                or category.is_subcategory(AdditiveGroups())):
                # Somewhat dirty hack to wrap non-atomic objects
                from sage.categories.modules_with_basis import ModulesWithBasis
                if self not in ModulesWithBasis:
                    if 'prefix' not in kwds:
                        kwds['prefix'] = ''
                    if 'bracket' not in kwds:
                        kwds['bracket'] = False
            result = GroupAlgebra_class(base_ring, self,
                                        category=algebra_category, **kwds)
            result.__doc__ = Sets.ParentMethods.algebra.__doc__
            return result

        def _sympy_(self):
            """
            Return an instance of a subclass of SymPy ``Set`` corresponding to ``self``.

            The default implementation creates an instance of
            :class:`~sage.interfaces.sympy_wrapper`.

            EXAMPLES::

                sage: F = FiniteEnumeratedSets().example(); F
                An example of a finite enumerated set: {1,2,3}
                sage: sF = F._sympy_(); sF
                SageSet(An example of a finite enumerated set: {1,2,3})
                sage: sF.is_finite_set
                True
                sage: bool(sF)
                True
                sage: len(sF)
                3
                sage: list(sF)
                [1, 2, 3]
                sage: from sympy import FiniteSet
                sage: FiniteSet.fromiter(sF)
                FiniteSet(1, 2, 3)

                sage: RR._sympy_().is_finite_set
                False

                sage: F = Family([1, 2])
                sage: F is Family([1, 2])
                False
                sage: sF = F._sympy_(); sF
                SageSet(Family (1, 2))
                sage: sF._sage_() is F
                True
            """
            from sage.interfaces.sympy_wrapper import SageSet
            from sage.interfaces.sympy import sympy_init
            sympy_init()
            return SageSet(self)

    class ElementMethods:
        ## Should eventually contain the basic operations which are no math
        ## latex, hash, ...
        ##def equal(x,y):
        ##def =(x,y):

        # Used by Element._test_category
        _dummy_attribute = None

        def cartesian_product(*elements):
            """
            Return the Cartesian product of its arguments, as an element of
            the Cartesian product of the parents of those elements.

            EXAMPLES::

                sage: C = AlgebrasWithBasis(QQ)
                sage: A = C.example()
                sage: (a,b,c) = A.algebra_generators()
                sage: a.cartesian_product(b, c)
                B[(0, word: a)] + B[(1, word: b)] + B[(2, word: c)]

            FIXME: is this a policy that we want to enforce on all parents?
            """
            from sage.structure.element import parent, Element
            assert all(isinstance(element, Element) for element in elements)
            parents = [parent(element) for element in elements]
            return cartesian_product(parents)._cartesian_product_of_elements(elements) # good name???

    class MorphismMethods:
        @abstract_method(optional=True)
        def __invert__(self):
            r"""
            Return the inverse morphism, or raise an error.

            The error may either state that the morphism is not
            invertible, or that Sage cannot invert it.

            EXAMPLES::

                sage: i = End(QQ).identity(); i
                Identity endomorphism of Rational Field
                sage: i.__invert__()
                Identity endomorphism of Rational Field

            This method is meant to be used with the Python inversion
            operator `~`::

                sage: ~i
                Identity endomorphism of Rational Field

            We now try to inverse a couple of morphisms defined by a matrix::

                sage: H = End(QQ^2)
                sage: phi = H(matrix([[1,1],[0,1]])); phi
                Vector space morphism represented by the matrix:
                [1 1]
                [0 1]
                Domain: Vector space of dimension 2 over Rational Field
                Codomain: Vector space of dimension 2 over Rational Field
                sage: ~phi
                Vector space morphism represented by the matrix:
                [ 1 -1]
                [ 0  1]
                Domain: Vector space of dimension 2 over Rational Field
                Codomain: Vector space of dimension 2 over Rational Field

                sage: phi = H(matrix([[1,1],[1,1]]))
                sage: ~phi
                Traceback (most recent call last):
                ...
                ZeroDivisionError: matrix morphism not invertible

            .. NOTE::

                This is an optional method. A default implementation
                raising ``NotImplementedError`` could be provided instead.
            """

        def is_injective(self):
            r"""
            Return whether this map is injective.

            EXAMPLES::

                sage: f = ZZ.hom(GF(3)); f
                Natural morphism:
                  From: Integer Ring
                  To:   Finite Field of size 3
                sage: f.is_injective()
                False
            """
            if self.domain().cardinality() <= 1:
                return True
            if self.domain().cardinality() > self.codomain().cardinality():
                return False
            raise NotImplementedError

    Enumerated = LazyImport('sage.categories.enumerated_sets', 'EnumeratedSets', at_startup=True)
    Facade = LazyImport('sage.categories.facade_sets', 'FacadeSets')
    Finite = LazyImport('sage.categories.finite_sets', 'FiniteSets', at_startup=True)
    Topological = LazyImport('sage.categories.topological_spaces',
                             'TopologicalSpaces', 'Topological', at_startup=True)
    Metric = LazyImport('sage.categories.metric_spaces', 'MetricSpaces',
                        'Metric', at_startup=True)

    class Infinite(CategoryWithAxiom):

        class ParentMethods:

            def is_finite(self):
                """
                Return whether this set is finite.

                Since this set is infinite this always returns ``False``.

                EXAMPLES::

                    sage: C = InfiniteEnumeratedSets().example()
                    sage: C.is_finite()
                    False

                TESTS::

                    sage: C.is_finite.__func__ is sage.categories.sets_cat.Sets.Infinite.ParentMethods.is_finite
                    True
                """
                return False

            def is_empty(self):
                r"""
                Return whether this set is empty.

                Since this set is infinite this always returns ``False``.

                EXAMPLES::

                    sage: C = InfiniteEnumeratedSets().example()
                    sage: C.is_empty()
                    False
                """
                return False

            def cardinality(self):
                """
                Count the elements of the enumerated set.

                EXAMPLES::

                    sage: NN = InfiniteEnumeratedSets().example()
                    sage: NN.cardinality()
                    +Infinity
                """
                from sage.rings.infinity import infinity
                return infinity

    class Subquotients(SubquotientsCategory):
        """
        A category for subquotients of sets.

        .. SEEALSO:: :meth:`Sets().Subquotients`

        EXAMPLES::

            sage: Sets().Subquotients()
            Category of subquotients of sets
            sage: Sets().Subquotients().all_super_categories()
            [Category of subquotients of sets, Category of sets,
             Category of sets with partial maps,
             Category of objects]
        """

        class ParentMethods:

            def _repr_(self):
                """
                EXAMPLES::

                    sage: from sage.categories.examples.semigroups import IncompleteSubquotientSemigroup
                    sage: S = IncompleteSubquotientSemigroup()
                    sage: S._repr_()
                    'A subquotient of An example of a semigroup: the left zero semigroup'
                """
                return "A subquotient of %s"%(self.ambient())

            @abstract_method
            def ambient(self):
                """
                Return the ambient space for ``self``.

                EXAMPLES::

                    sage: Semigroups().Subquotients().example().ambient()
                    An example of a semigroup: the left zero semigroup

                .. SEEALSO::

                    :meth:`Sets.SubcategoryMethods.Subquotients` for the
                    specifications and :meth:`.lift` and :meth:`.retract`.
                """

            # Should lift and retract be declared as conversions to the coercion mechanism ?
            # Compatibility issue: in IntegerModRing, lift is a method returning the actual
            # lifting morphism::
            #
            #   sage: F = IntegerModRing(3)
            #   sage: F.lift()
            #   Set-theoretic ring morphism:
            #   From: Ring of integers modulo 3
            #   To:   Integer Ring
            #   Defn: Choice of lifting map
            @abstract_method
            def lift(self, x):
                """
                Lift `x` to the ambient space for ``self``.

                INPUT:

                - ``x`` -- an element of ``self``

                EXAMPLES::

                    sage: S = Semigroups().Subquotients().example()
                    sage: s = S.an_element()
                    sage: s, s.parent()
                    (42, An example of a (sub)quotient semigroup: a quotient of the left zero semigroup)
                    sage: S.lift(s), S.lift(s).parent()
                    (42, An example of a semigroup: the left zero semigroup)
                    sage: s.lift(), s.lift().parent()
                    (42, An example of a semigroup: the left zero semigroup)

                .. SEEALSO::

                    :class:`Sets.SubcategoryMethods.Subquotients` for
                    the specifications, :meth:`.ambient`, :meth:`.retract`,
                    and also :meth:`Sets.Subquotients.ElementMethods.lift`.
                """

            @abstract_method
            def retract(self, x):
                """
                Retract ``x`` to ``self``.

                INPUT:

                - ``x`` -- an element of the ambient space for ``self``

                .. SEEALSO::

                    :class:`Sets.SubcategoryMethods.Subquotients` for
                    the specifications, :meth:`.ambient`, :meth:`.retract`,
                    and also :meth:`Sets.Subquotients.ElementMethods.retract`.

                EXAMPLES::

                    sage: S = Semigroups().Subquotients().example()
                    sage: s = S.ambient().an_element()
                    sage: s, s.parent()
                    (42, An example of a semigroup: the left zero semigroup)
                    sage: S.retract(s), S.retract(s).parent()
                    (42, An example of a (sub)quotient semigroup: a quotient of the left zero semigroup)
                """

        class ElementMethods:

            def lift(self):
                """
                Lift ``self`` to the ambient space for its parent.

                EXAMPLES::

                    sage: S = Semigroups().Subquotients().example()
                    sage: s = S.an_element()
                    sage: s, s.parent()
                    (42, An example of a (sub)quotient semigroup: a quotient of the left zero semigroup)
                    sage: S.lift(s), S.lift(s).parent()
                    (42, An example of a semigroup: the left zero semigroup)
                    sage: s.lift(), s.lift().parent()
                    (42, An example of a semigroup: the left zero semigroup)
                """
                return self.parent().lift(self)

    class Quotients(QuotientsCategory):
        """
        A category for quotients of sets.

        .. SEEALSO:: :meth:`Sets().Quotients`

        EXAMPLES::

            sage: Sets().Quotients()
            Category of quotients of sets
            sage: Sets().Quotients().all_super_categories()
            [Category of quotients of sets,
             Category of subquotients of sets,
             Category of sets,
             Category of sets with partial maps,
             Category of objects]
        """

        class ParentMethods:

            def _repr_(self):
                """
                EXAMPLES::

                    sage: from sage.categories.examples.semigroups import IncompleteSubquotientSemigroup
                    sage: S = IncompleteSubquotientSemigroup(category=Semigroups().Quotients())
                    sage: S._repr_()
                    'A quotient of An example of a semigroup: the left zero semigroup'
                """
                return "A quotient of {}".format(self.ambient())

            def _an_element_(self):
                """
                Return an element of ``self``, as per
                :meth:`Sets.ParentMethods.an_element`

                EXAMPLES::

                    sage: S = FiniteEnumeratedSets().IsomorphicObjects().example()
                    sage: S.an_element()  # indirect doctest
                    1
                """
                return self.retract(self.ambient().an_element())

    class Subobjects(SubobjectsCategory):
        """
        A category for subobjects of sets.

        .. SEEALSO:: :meth:`Sets().Subobjects`

        EXAMPLES::

            sage: Sets().Subobjects()
            Category of subobjects of sets
            sage: Sets().Subobjects().all_super_categories()
            [Category of subobjects of sets,
             Category of subquotients of sets,
             Category of sets,
             Category of sets with partial maps,
             Category of objects]
        """

        class ParentMethods:

            def _repr_(self):
                """
                EXAMPLES::

                    sage: from sage.categories.examples.semigroups import IncompleteSubquotientSemigroup
                    sage: S = IncompleteSubquotientSemigroup(category = Semigroups().Subobjects())
                    sage: S._repr_()
                    'A subobject of An example of a semigroup: the left zero semigroup'
                """
                return "A subobject of {}".format(self.ambient())

    class IsomorphicObjects(IsomorphicObjectsCategory):
        """
        A category for isomorphic objects of sets.

        EXAMPLES::

            sage: Sets().IsomorphicObjects()
            Category of isomorphic objects of sets
            sage: Sets().IsomorphicObjects().all_super_categories()
            [Category of isomorphic objects of sets,
             Category of subobjects of sets, Category of quotients of sets,
             Category of subquotients of sets,
             Category of sets,
             Category of sets with partial maps,
             Category of objects]
        """

        class ParentMethods:

            def _repr_(self):
                """
                EXAMPLES::

                    sage: S = FiniteEnumeratedSets().IsomorphicObjects().example()
                    sage: S._repr_()
                    'The image by some isomorphism of An example of a finite enumerated set: {1,2,3}'
                """
                return "The image by some isomorphism of %s"%(self.ambient())

    class CartesianProducts(CartesianProductsCategory):
        """
        EXAMPLES::

            sage: C = Sets().CartesianProducts().example()
            sage: C
            The Cartesian product of (Set of prime numbers (basic implementation),
             An example of an infinite enumerated set: the non negative integers,
             An example of a finite enumerated set: {1,2,3})
            sage: C.category()
            Category of Cartesian products of sets
            sage: C.categories()
            [Category of Cartesian products of sets, Category of sets,
             Category of sets with partial maps,
             Category of objects]
            sage: TestSuite(C).run()
        """

        def extra_super_categories(self):
            """
            A Cartesian product of sets is a set.

            EXAMPLES::

                sage: Sets().CartesianProducts().extra_super_categories()
                [Category of sets]
                sage: Sets().CartesianProducts().super_categories()
                [Category of sets]
            """
            return [Sets()]

        def example(self):
            """
            EXAMPLES::

                sage: Sets().CartesianProducts().example()
                The Cartesian product of (Set of prime numbers (basic implementation),
                 An example of an infinite enumerated set: the non negative integers,
                 An example of a finite enumerated set: {1,2,3})
            """
            from .finite_enumerated_sets import FiniteEnumeratedSets
            from .infinite_enumerated_sets import InfiniteEnumeratedSets
            from .cartesian_product import cartesian_product
            S1 = Sets().example()
            S2 = InfiniteEnumeratedSets().example()
            S3 = FiniteEnumeratedSets().example()
            return cartesian_product([S1, S2, S3])


        class ParentMethods:
            def __iter__(self):
                r"""
                Return a lexicographic iterator for the elements of this Cartesian product.

                EXAMPLES:

                Sets are intrinsically unordered::

                    sage: for x,y in cartesian_product([Set([1,2]), Set(['a','b'])]): # random
                    ....:     print((x, y))
                    (1, 'b')
                    (1, 'a')
                    (2, 'b')
                    (2, 'a')

                    sage: A = FiniteEnumeratedSets()(["a", "b"])
                    sage: B = FiniteEnumeratedSets().example(); B
                    An example of a finite enumerated set: {1,2,3}
                    sage: C = cartesian_product([A, B, A]); C
                    The Cartesian product of ({'a', 'b'}, An example of a finite enumerated set: {1,2,3}, {'a', 'b'})
                    sage: C in FiniteEnumeratedSets()
                    True
                    sage: list(C)
                    [('a', 1, 'a'), ('a', 1, 'b'), ('a', 2, 'a'), ('a', 2, 'b'), ('a', 3, 'a'), ('a', 3, 'b'),
                     ('b', 1, 'a'), ('b', 1, 'b'), ('b', 2, 'a'), ('b', 2, 'b'), ('b', 3, 'a'), ('b', 3, 'b')]
                    sage: C.__iter__.__module__
                    'sage.categories.sets_cat'

                    sage: F22 = GF(2).cartesian_product(GF(2))
                    sage: list(F22)
                    [(0, 0), (0, 1), (1, 0), (1, 1)]

                    sage: C = cartesian_product([Permutations(10)]*4)
                    sage: it = iter(C)
                    sage: next(it)
                    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    sage: next(it)
                    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                     [1, 2, 3, 4, 5, 6, 7, 8, 10, 9])

                .. WARNING::

                    The elements are returned in lexicographic order,
                    which gives a valid enumeration only if all
                    factors, but possibly the first one, are
                    finite. So the following one is fine::

                        sage: it = iter(cartesian_product([ZZ, GF(2)]))
                        sage: [next(it) for _ in range(10)]
                        [(0, 0), (0, 1), (1, 0), (1, 1),
                         (-1, 0), (-1, 1), (2, 0), (2, 1),
                         (-2, 0), (-2, 1)]

                    But this one is not::

                        sage: it = iter(cartesian_product([GF(2), ZZ]))
                        sage: [next(it) for _ in range(10)]
                        doctest:...: UserWarning: Sage is not able to determine
                        whether the factors of this Cartesian product are
                        finite. The lexicographic ordering might not go through
                        all elements.
                        [(0, 0), (0, 1), (0, -1), (0, 2), (0, -2),
                         (0, 3), (0, -3), (0, 4), (0, -4), (0, 5)]

                .. NOTE::

                    Here it would be faster to use :func:`itertools.product` for sets
                    of small size. But the latter expands all factor in memory!
                    So we can not reasonably use it in general.

                ALGORITHM:

                Recipe 19.9 in the Python Cookbook by Alex Martelli
                and David Ascher.
                """
                if any(f not in Sets().Finite() for f in self.cartesian_factors()[1:]):
                    from warnings import warn
                    warn("Sage is not able to determine whether the factors of "
                         "this Cartesian product are finite. The lexicographic "
                         "ordering might not go through all elements.")

                # visualize an odometer, with "wheels" displaying "digits"...:
                factors = list(self.cartesian_factors())
                wheels = [iter(f) for f in factors]
                try:
                    digits = [next(it) for it in wheels]
                except StopIteration:
                    return
                while True:
                    yield self._cartesian_product_of_elements(digits)
                    for i in range(len(digits)-1, -1, -1):
                        try:
                            digits[i] = next(wheels[i])
                            break
                        except StopIteration:
                            wheels[i] = iter(factors[i])
                            try:
                                digits[i] = next(wheels[i])
                            except StopIteration:
                                return
                    else:
                        break

            @cached_method
            def an_element(self):
                """
                EXAMPLES::

                    sage: C = Sets().CartesianProducts().example(); C
                    The Cartesian product of (Set of prime numbers (basic implementation),
                     An example of an infinite enumerated set: the non negative integers,
                     An example of a finite enumerated set: {1,2,3})
                    sage: C.an_element()
                    (47, 42, 1)
                """
                return self._cartesian_product_of_elements(s.an_element() for s in self._sets)

            def is_empty(self):
                r"""
                Return whether this set is empty.

                EXAMPLES::


                    sage: S1 = FiniteEnumeratedSet([1,2,3])
                    sage: S2 = Set([])
                    sage: cartesian_product([S1,ZZ]).is_empty()
                    False
                    sage: cartesian_product([S1,S2,S1]).is_empty()
                    True
                """
                return any(c.is_empty() for c in self.cartesian_factors())

            def is_finite(self):
                r"""
                Return whether this set is finite.

                EXAMPLES::

                    sage: E = FiniteEnumeratedSet([1,2,3])
                    sage: C = cartesian_product([E, SymmetricGroup(4)])
                    sage: C.is_finite()
                    True

                    sage: cartesian_product([ZZ,ZZ]).is_finite()
                    False
                    sage: cartesian_product([ZZ, Set(), ZZ]).is_finite()
                    True
                """
                f = self.cartesian_factors()
                try:
                    # Note: some parent might not implement "is_empty". So we
                    # carefully isolate this test.
                    test = any(c.is_empty() for c in f)
                except (AttributeError, NotImplementedError):
                    pass
                else:
                    if test:
                        return test
                return all(c.is_finite() for c in f)

            def cardinality(self):
                r"""
                Return the cardinality of self.

                EXAMPLES::

                    sage: E = FiniteEnumeratedSet([1,2,3])
                    sage: C = cartesian_product([E,SymmetricGroup(4)])
                    sage: C.cardinality()
                    72

                    sage: E = FiniteEnumeratedSet([])
                    sage: C = cartesian_product([E, ZZ, QQ])
                    sage: C.cardinality()
                    0

                    sage: C = cartesian_product([ZZ, QQ])
                    sage: C.cardinality()
                    +Infinity

                    sage: cartesian_product([GF(5), Permutations(10)]).cardinality()
                    18144000
                    sage: cartesian_product([GF(71)]*20).cardinality() == 71**20
                    True
                """
                f = self.cartesian_factors()

                try:
                    # Note: some parent might not implement "is_empty". So we
                    # carefully isolate this test.
                    is_empty = any(c.is_empty() for c in f)
                except (AttributeError,NotImplementedError):
                    pass
                else:
                    if is_empty:
                        from sage.rings.integer_ring import ZZ
                        return ZZ.zero()
                    elif any(c in Sets().Infinite() for c in f):
                        from sage.rings.infinity import Infinity
                        return Infinity

                from sage.misc.misc_c import prod
                return prod(c.cardinality() for c in f)

            def random_element(self, *args):
                r"""
                Return a random element of this Cartesian product.

                The extra arguments are passed down to each of the
                factors of the Cartesian product.

                EXAMPLES::

                    sage: C = cartesian_product([Permutations(10)]*5)
                    sage: C.random_element()           # random
                    ([2, 9, 4, 7, 1, 8, 6, 10, 5, 3],
                     [8, 6, 5, 7, 1, 4, 9, 3, 10, 2],
                     [5, 10, 3, 8, 2, 9, 1, 4, 7, 6],
                     [9, 6, 10, 3, 2, 1, 5, 8, 7, 4],
                     [8, 5, 2, 9, 10, 3, 7, 1, 4, 6])

                    sage: C = cartesian_product([ZZ]*10)
                    sage: c1 = C.random_element()
                    sage: c1                   # random
                    (3, 1, 4, 1, 1, -3, 0, -4, -17, 2)
                    sage: c2 = C.random_element(4,7)
                    sage: c2                   # random
                    (6, 5, 6, 4, 5, 6, 6, 4, 5, 5)
                    sage: all(4 <= i < 7 for i in c2)
                    True
                """
                return self._cartesian_product_of_elements(
                        c.random_element(*args) for c in self.cartesian_factors())

            @abstract_method
            def _sets_keys(self):
                """
                Return the indices of the Cartesian factors of ``self``.

                EXAMPLES::

                    sage: cartesian_product([QQ, ZZ, ZZ])._sets_keys()
                    {0, 1, 2}
                """

            @abstract_method
            def cartesian_factors(self):
                """
                Return the Cartesian factors of ``self``.

                EXAMPLES::

                    sage: cartesian_product([QQ, ZZ, ZZ]).cartesian_factors()
                    (Rational Field, Integer Ring, Integer Ring)
                """

            @abstract_method
            def cartesian_projection(self, i):
                """
                Return the natural projection onto the `i`-th
                Cartesian factor of ``self``.

                INPUT:

                - ``i`` -- the index of a Cartesian factor of ``self``

                EXAMPLES::

                    sage: C = Sets().CartesianProducts().example(); C
                    The Cartesian product of (Set of prime numbers (basic implementation),
                     An example of an infinite enumerated set: the non negative integers,
                     An example of a finite enumerated set: {1,2,3})
                    sage: x = C.an_element(); x
                    (47, 42, 1)
                    sage: pi = C.cartesian_projection(1)
                    sage: pi(x)
                    42
                """

            @abstract_method
            def _cartesian_product_of_elements(self, elements):
                """
                Return the Cartesian product of the given ``elements``.

                This method should accept any iterable.

                INPUT:

                - ``elements`` -- an iterable (e.g. a tuple or a list) of
                  elements of each Cartesian factor of ``self``

                EXAMPLES::

                    sage: S1 = Sets().example()
                    sage: S2 = InfiniteEnumeratedSets().example()
                    sage: X = [S2, S1, S2]
                    sage: C = cartesian_product(X)
                    sage: C._cartesian_product_of_elements([S.an_element() for S in X])
                    (42, 47, 42)
                    sage: C._cartesian_product_of_elements(S.an_element() for S in X)
                    (42, 47, 42)
                """

            def _sympy_(self):
                """
                Return a SymPy ``ProductSet`` corresponding to ``self``.

                EXAMPLES::

                    sage: ZZ3 = cartesian_product([ZZ, ZZ, ZZ])
                    sage: sZZ3 = ZZ3._sympy_(); sZZ3
                    ProductSet(Integers, Integers, Integers)
                    sage: (1, 2, 3) in sZZ3
                    True
                """
                from sympy import ProductSet
                from sage.interfaces.sympy import sympy_init
                sympy_init()
                return ProductSet(*self.cartesian_factors())

        class ElementMethods:

            def cartesian_projection(self, i):
                """
                Return the projection of ``self`` onto the `i`-th
                factor of the Cartesian product.

                INPUT:

                - ``i`` -- the index of a factor of the Cartesian product

                EXAMPLES::

                    sage: F = CombinatorialFreeModule(ZZ, [4,5]); F.__custom_name = "F"
                    sage: G = CombinatorialFreeModule(ZZ, [4,6]); G.__custom_name = "G"
                    sage: S = cartesian_product([F, G])
                    sage: x = S.monomial((0,4)) + 2 * S.monomial((0,5)) + 3 * S.monomial((1,6))
                    sage: x.cartesian_projection(0)
                    B[4] + 2*B[5]
                    sage: x.cartesian_projection(1)
                    3*B[6]
                """
                return self.parent().cartesian_projection(i)(self)

            def cartesian_factors(self):
                """
                Return the Cartesian factors of ``self``.

                EXAMPLES::

                    sage: F = CombinatorialFreeModule(ZZ, [4,5]); F.__custom_name = "F"
                    sage: G = CombinatorialFreeModule(ZZ, [4,6]); G.__custom_name = "G"
                    sage: H = CombinatorialFreeModule(ZZ, [4,7]); H.__custom_name = "H"
                    sage: S = cartesian_product([F, G, H])
                    sage: x = S.monomial((0,4)) + 2 * S.monomial((0,5)) + 3 * S.monomial((1,6)) + 4 * S.monomial((2,4)) + 5 * S.monomial((2,7))
                    sage: x.cartesian_factors()
                    (B[4] + 2*B[5], 3*B[6], 4*B[4] + 5*B[7])
                    sage: [s.parent() for s in x.cartesian_factors()]
                    [F, G, H]
                    sage: S.zero().cartesian_factors()
                    (0, 0, 0)
                    sage: [s.parent() for s in S.zero().cartesian_factors()]
                    [F, G, H]
                """
                # TODO: optimize
                return tuple(self.cartesian_projection(i)
                             for i in self.parent()._sets_keys())
                #return Family(self._sets.keys(), self.projection)

    class Algebras(AlgebrasCategory):

        def extra_super_categories(self):
            """
            EXAMPLES::

                sage: Sets().Algebras(ZZ).super_categories()
                [Category of modules with basis over Integer Ring]

                sage: Sets().Algebras(QQ).extra_super_categories()
                [Category of vector spaces with basis over Rational Field]

                sage: Sets().example().algebra(ZZ).categories()
                [Category of set algebras over Integer Ring,
                 Category of modules with basis over Integer Ring,
                 ...
                 Category of objects]

            """
            from sage.categories.modules_with_basis import ModulesWithBasis
            return [ModulesWithBasis(self.base_ring())]

        class ParentMethods:
            def construction(self):
                r"""
                Return the functorial construction of ``self``.

                EXAMPLES::

                    sage: A = GroupAlgebra(KleinFourGroup(), QQ)
                    sage: F, arg = A.construction(); F, arg
                    (GroupAlgebraFunctor, Rational Field)
                    sage: F(arg) is A
                    True

                This also works for structures such as monoid algebras (see
                :trac:`27937`)::

                    sage: A = FreeAbelianMonoid('x,y').algebra(QQ)
                    sage: F, arg = A.construction(); F, arg
                    (The algebra functorial construction,
                     Free abelian monoid on 2 generators (x, y))
                    sage: F(arg) is A
                    True
                """
                from sage.categories.algebra_functor import (
                        GroupAlgebraFunctor, AlgebraFunctor)
                try:
                    group = self.group()
                except AttributeError:
                    return (AlgebraFunctor(self.base_ring()),
                            self.basis().keys())
                return GroupAlgebraFunctor(group), self.base_ring()

            def _repr_(self):
                r"""
                Return the string representation of `self`.

                EXAMPLES::

                    sage: A = Groups().example().algebra(QQ); A
                    Algebra of General Linear Group of degree 4 over Rational Field
                     over Rational Field
                    sage: A._name = "foo"
                    sage: A
                    foo over Rational Field
                    sage: A = KleinFourGroup().algebra(ZZ)
                    sage: A
                    Algebra of The Klein 4 group of order 4, as a permutation group
                     over Integer Ring
                """
                if hasattr(self, "_name"):
                    return self._name + " over {}".format(self.base_ring())
                else:
                    return 'Algebra of {} over {}'.format(self.basis().keys(),
                                                          self.base_ring())

    class WithRealizations(WithRealizationsCategory):

        def extra_super_categories(self):
            """
            A set with multiple realizations is a facade parent.

            EXAMPLES::

                sage: Sets().WithRealizations().extra_super_categories()
                [Category of facade sets]
                sage: Sets().WithRealizations().super_categories()
                [Category of facade sets]
            """
            return [Sets().Facade()]

        def example(self, base_ring = None, set = None):
            r"""
            Return an example of set with multiple realizations, as
            per :meth:`Category.example`.

            EXAMPLES::

                sage: Sets().WithRealizations().example()
                The subset algebra of {1, 2, 3} over Rational Field

                sage: Sets().WithRealizations().example(ZZ, Set([1,2]))
                The subset algebra of {1, 2} over Integer Ring
            """
            from sage.rings.rational_field import QQ
            from sage.sets.set import Set
            if base_ring is None:
                base_ring = QQ
            if set is None:
                set = Set([1,2,3])
            from sage.categories.examples.with_realizations import SubsetAlgebra
            return SubsetAlgebra(base_ring, set)

        class ParentMethods:

            def _test_with_realizations(self, **options):
                r"""
                Test that this parent with realizations is
                properly implemented.

                INPUT:

                - ``options`` -- any keyword arguments accepted
                  by :meth:`_tester`

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example()
                    sage: A._test_with_realizations()

                See the documentation for :class:`TestSuite`
                for more information.
                """
                tester = self._tester(**options)
                for R in self.realizations():
                    tester.assertIn(R, self.Realizations())
                # Could check that there are coerce maps between any two realizations

            @lazy_attribute
            def _realizations(self):
                """
                This lazily initializes the attribute
                ``_realizations`` the first time it is needed.

                TESTS::

                    sage: class MyParent(Parent):
                    ....:    pass
                    sage: P = MyParent(category = Sets().WithRealizations())
                    sage: P._realizations
                    []
                """
                return []

            def _register_realization(self, realization):
                """
                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(QQ['x']); A
                    The subset algebra of {1, 2, 3} over Univariate Polynomial Ring in x over Rational Field
                    sage: class ANewRealizationOfA(CombinatorialFreeModule):
                    ....:     pass
                    sage: category = A.Realizations() & Algebras(QQ[x]).WithBasis()
                    sage: R = ANewRealizationOfA(A.base_ring(), A.F().basis().keys(), category = category)
                    sage: R in A.realizations()  # indirect doctest
                    True

                Note: the test above uses ``QQ[x]`` to not interfer
                with other tests.
                """
                assert realization.realization_of() is self
                self._realizations.append(realization)

            def inject_shorthands(self, shorthands=None, verbose=True):
                """
                Import standard shorthands into the global namespace.

                INPUT:

                - ``shorthands`` -- a list (or iterable) of strings (default: ``self._shorthands``)
                  or ``"all"`` (for ``self._shorthands_all``)
                - ``verbose`` -- boolean (default ``True``);
                   whether to print the defined shorthands

                EXAMPLES:

                When computing with a set with multiple realizations,
                like :class:`SymmetricFunctions` or
                :class:`~sage.categories.examples.with_realizations.SubsetAlgebra`,
                it is convenient to define shorthands for the various
                realizations, but cumbersome to do it by hand::

                    sage: S = SymmetricFunctions(ZZ); S
                    Symmetric Functions over Integer Ring
                    sage: s = S.s(); s
                    Symmetric Functions over Integer Ring in the Schur basis
                    sage: e = S.e(); e
                    Symmetric Functions over Integer Ring in the elementary basis

                This method automates the process::

                    sage: S.inject_shorthands()
                    Defining e as shorthand for Symmetric Functions over Integer Ring in the elementary basis
                    Defining f as shorthand for Symmetric Functions over Integer Ring in the forgotten basis
                    Defining h as shorthand for Symmetric Functions over Integer Ring in the homogeneous basis
                    Defining m as shorthand for Symmetric Functions over Integer Ring in the monomial basis
                    Defining p as shorthand for Symmetric Functions over Integer Ring in the powersum basis
                    Defining s as shorthand for Symmetric Functions over Integer Ring in the Schur basis
                    sage: s[1] + e[2] * p[1,1] + 2*h[3] + m[2,1]
                    s[1] - 2*s[1, 1, 1] + s[1, 1, 1, 1] + s[2, 1] + 2*s[2, 1, 1] + s[2, 2] + 2*s[3] + s[3, 1]

                    sage: e
                    Symmetric Functions over Integer Ring in the elementary basis
                    sage: p
                    Symmetric Functions over Integer Ring in the powersum basis
                    sage: s
                    Symmetric Functions over Integer Ring in the Schur basis

                Sometimes, like for symmetric functions, one can
                request for all shorthands to be defined, including
                less common ones::

                    sage: S.inject_shorthands("all")
                    Defining e as shorthand for Symmetric Functions over Integer Ring in the elementary basis
                    Defining f as shorthand for Symmetric Functions over Integer Ring in the forgotten basis
                    Defining h as shorthand for Symmetric Functions over Integer Ring in the homogeneous basis
                    Defining ht as shorthand for Symmetric Functions over Integer Ring in the induced trivial symmetric group character basis
                    Defining m as shorthand for Symmetric Functions over Integer Ring in the monomial basis
                    Defining o as shorthand for Symmetric Functions over Integer Ring in the orthogonal basis
                    Defining p as shorthand for Symmetric Functions over Integer Ring in the powersum basis
                    Defining s as shorthand for Symmetric Functions over Integer Ring in the Schur basis
                    Defining sp as shorthand for Symmetric Functions over Integer Ring in the symplectic basis
                    Defining st as shorthand for Symmetric Functions over Integer Ring in the irreducible symmetric group character basis
                    Defining w as shorthand for Symmetric Functions over Integer Ring in the Witt basis

                The messages can be silenced by setting ``verbose=False``::

                    sage: Q = QuasiSymmetricFunctions(ZZ)
                    sage: Q.inject_shorthands(verbose=False)

                    sage: F[1,2,1] + 5*M[1,3] + F[2]^2
                    5*F[1, 1, 1, 1] - 5*F[1, 1, 2] - 3*F[1, 2, 1] + 6*F[1, 3] +
                    2*F[2, 2] + F[3, 1] + F[4]

                    sage: F
                    Quasisymmetric functions over the Integer Ring in the
                     Fundamental basis
                    sage: M
                    Quasisymmetric functions over the Integer Ring in the
                     Monomial basis

                One can also just import a subset of the shorthands::

                    sage: SQ = SymmetricFunctions(QQ)
                    sage: SQ.inject_shorthands(['p', 's'], verbose=False)
                    sage: p
                    Symmetric Functions over Rational Field in the powersum basis
                    sage: s
                    Symmetric Functions over Rational Field in the Schur basis

                Note that ``e`` is left unchanged::

                    sage: e
                    Symmetric Functions over Integer Ring in the elementary basis

                TESTS::

                    sage: e == S.e(), h == S.h(), m == S.m(), p == SQ.p(), s == SQ.s()
                    (True, True, True, True, True)
                """
                from sage.misc.misc import inject_variable
                if shorthands == 'all':
                    shorthands = getattr(self, '_shorthands_all', None)
                if shorthands is None:
                    shorthands = getattr(self, '_shorthands', None)
                    if shorthands is None:
                        raise NotImplementedError("no shorthands defined for {}".format(self))
                for shorthand in shorthands:
                    realization = getattr(self, shorthand)()
                    if verbose:
                        print('Defining {} as shorthand for {}'.format(shorthand, realization))
                    inject_variable(shorthand, realization, warn=False)

            @abstract_method(optional=True)
            def a_realization(self):
                """
                Return a realization of ``self``.

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: A.a_realization()
                    The subset algebra of {1, 2, 3} over Rational Field in the Fundamental basis
                """

            def realizations(self):
                """
                Return all the realizations of ``self`` that ``self``
                is aware of.

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: A.realizations()
                    [The subset algebra of {1, 2, 3} over Rational Field in the Fundamental basis, The subset algebra of {1, 2, 3} over Rational Field in the In basis, The subset algebra of {1, 2, 3} over Rational Field in the Out basis]

                .. NOTE::

                    Constructing a parent ``P`` in the category
                    ``A.Realizations()`` automatically adds ``P`` to
                    this list by calling ``A._register_realization(A)``
                """
                return self._realizations

            def facade_for(self):
                """
                Return the parents ``self`` is a facade for, that is
                the realizations of ``self``

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: A.facade_for()
                    [The subset algebra of {1, 2, 3} over Rational Field in the Fundamental basis, The subset algebra of {1, 2, 3} over Rational Field in the In basis, The subset algebra of {1, 2, 3} over Rational Field in the Out basis]

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: f = A.F().an_element(); f
                    F[{}] + 2*F[{1}] + 3*F[{2}] + F[{1, 2}]
                    sage: i = A.In().an_element(); i
                    In[{}] + 2*In[{1}] + 3*In[{2}] + In[{1, 2}]
                    sage: o = A.Out().an_element(); o
                    Out[{}] + 2*Out[{1}] + 3*Out[{2}] + Out[{1, 2}]
                    sage: f in A, i in A, o in A
                    (True, True, True)
                """
                return self.realizations()

            # Do we really want this feature?
            class Realizations(Category_realization_of_parent):

                def super_categories(self):
                    """
                    EXAMPLES::

                        sage: A = Sets().WithRealizations().example(); A
                        The subset algebra of {1, 2, 3} over Rational Field
                        sage: A.Realizations().super_categories()
                        [Category of realizations of sets]
                    """
                    return [Sets().Realizations()]

            def _an_element_(self):
                """
                Return an element of some realization of ``self``.

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: A.an_element()        # indirect doctest
                    F[{}] + 2*F[{1}] + 3*F[{2}] + F[{1, 2}]

                TESTS:

                Check that we are consistent no matter which basis is
                created first::

                    sage: M = posets.BooleanLattice(4).moebius_algebra(QQ)
                    sage: I = M.I()
                    sage: M._an_element_()
                    2*E[0] + 2*E[1] + 3*E[2]
                """
                return self.a_realization().an_element()

            # TODO: maybe this could be taken care of by Sets.Facade()?
            def __contains__(self, x):
                r"""
                Test whether ``x`` is in ``self``, that is if it is an
                element of some realization of ``self``.

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: A.an_element() in A
                    True
                    sage: A.In().an_element() in A
                    True
                    sage: A.F().an_element() in A
                    True
                    sage: A.Out().an_element() in A
                    True
                    sage: 1 in A
                    True
                    sage: QQ['x'].an_element() in A
                    False
                """
                return any(x in realization for realization in self.realizations())

    class Realizations(RealizationsCategory):

        class ParentMethods:

            def __init_extra__(self):
                """
                Register ``self`` as a realization of ``self.realization_of``.

                TESTS::

                    sage: A = Sets().WithRealizations().example()
                    sage: A.realizations()    # indirect doctest
                    [The subset algebra of {1, 2, 3} over Rational Field in the Fundamental basis,
                     The subset algebra of {1, 2, 3} over Rational Field in the In basis,
                     The subset algebra of {1, 2, 3} over Rational Field in the Out basis]
                """
                self.realization_of()._register_realization(self)

            @cached_method
            def realization_of(self):
                """
                Return the parent this is a realization of.

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: In = A.In(); In
                    The subset algebra of {1, 2, 3} over Rational Field in the In basis
                    sage: In.realization_of()
                    The subset algebra of {1, 2, 3} over Rational Field
                """
                for category in self.categories():
                    if isinstance(category, Category_realization_of_parent):
                        return category.base()

            def _realization_name(self):
                """
                Return the name of this realization.

                In this default implementation, this is guessed from
                the name of its class.

                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: In = A.In(); In
                    The subset algebra of {1, 2, 3} over Rational Field in the In basis
                    sage: In._realization_name()
                    'In'
                """
                # The __base__ gets rid of the with_category
                # The split adds support for nested classes
                return self.__class__.__base__.__name__.split('.')[-1]

            def _repr_(self):
                """
                EXAMPLES::

                    sage: A = Sets().WithRealizations().example(); A
                    The subset algebra of {1, 2, 3} over Rational Field
                    sage: In = A.In(); In
                    The subset algebra of {1, 2, 3} over Rational Field in the In basis

                In the example above, :meth:`repr` was overridden by
                the category ``A.Realizations()``. We now add a new
                (fake) realization which is not in
                ``A.Realizations()`` to actually exercise this
                method::

                    sage: from sage.categories.realizations import Realizations
                    sage: class Blah(Parent):
                    ....:     pass
                    sage: P = Blah(category = Sets.WithRealizations.ParentMethods.Realizations(A))
                    sage: P     # indirect doctest
                    The subset algebra of {1, 2, 3} over Rational Field in the realization Blah
                """
                return "{} in the realization {}".format(self.realization_of(), self._realization_name())

# Moved from sage.categories.cartesian_product to avoid circular import errors
cartesian_product = CartesianProductFunctor()
