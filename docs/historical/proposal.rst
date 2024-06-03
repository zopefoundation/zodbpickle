Proposal for ZODB pickle compatibility
======================================

Issues
------

- There exists no forward-compatible way to pickle bytes on Python2 (Py3k
  pickle module "guesses", decoding any Python2 ``str`` using ``latin1``).

- Some data pickled as ``str`` on Python2 truly is binary (e.g., ``Pdata``
  objects for Zope2's ``OFS.Image.File`` and ``OFS.Image.Image``
  types;  crypto hases?)

- Some Python2 applications may have the same attribute for a given class
  stored both as ``str`` and as ``unicode`` (due e.g., to bugs in the code,
  literal defaults, browser quirks, changes to code over time).


Scenarios
---------


.. _py2_forever:

Existing Python2-only Application
+++++++++++++++++++++++++++++++++

- Code for the app is never(ish) going to migrate to Py3k.

- Using an updated / supported ZODb package **must** be possible

- Ideally, requires no changes to application code.

- Ideally, requies no database fixup / conversion.

- Best strategy is likely ignore_compat_.


.. _py3k_only:

New, Py3k-only Application
++++++++++++++++++++++++++

- Code for the app will run only on Py3k.

- Running with the latest-and-greatest ZODB **must** be possible.

- Ideally, the code for the app will make no concessions to backward-
  compatibility.

- Best strategy is likely ignore_compat_.


.. _migrate_w_convert:

Python2 Application Migrating to Py3k
+++++++++++++++++++++++++++++++++++++

- Application code "straddles" both Pythons using "compatible subset"
  dialect, but only during the migration period.

- During that period, code **must** be able to open the database from both
  Python2 and Py3k.

- Ideally, application code will need to make no concessions to
  backward-compatibility after migration.

- It is acceptable to run a conversion process which normalizes all
  active records in the database prior to testing.

- For databases which are already "binary clean" (binary data exists only
  in blobs; the application creates no new non-blob binary attributes), 
  the best strategy is likely ignore_compat_.

- For databases which are not already "binary clean" (there may be non-blob
  binary attributes), the best strategy is likely to convert_storages_,
  followed by replace_py2_cpickle_ (if the Python2 client might create new
  non-blob binary attributes).

- wrap_storages_ (on the Python2 side) might be simpler than
  replace_py2_cpickle_, if the sources of non-blob binary attributes are
  well understood.


.. _straddle_w_convert:

Python2 Application Straddling Python2 / Py3k (1)
+++++++++++++++++++++++++++++++++++++++++++++++++

- Application code "straddles" both Pythons using "compatible subset"
  dialect.

- Code **must** be able to open the database from both Python2 and Py3k.

- It is acceptable to run a conversion process which normalizes all
  active records in the database prior to testing.

- For databases which are already "binary clean" (binary data exists only
  in blobs; the application creates no new non-blob binary attributes), 
  the best strategy is likely ignore_compat_.

- For databases which are not already "binary clean" (there may be non-blob
  binary attributes), the best strategy is likely to convert_storages_,
  followed by replace_py2_cpickle_ (if the Python2 client might create new
  non-blob binary attributes).

- For cases where Python2 and Py3k clients may share the database for an
  extended period, and where disruption to the Python2 clients must be
  minimized, the replace_py3k_pickle_ strategy might be preferred, until
  convert_storages_ becomes feasible.


.. _straddle_no_convert:

Python2 Application Migrating to Py3k (2)
+++++++++++++++++++++++++++++++++++++++++

- Application code "straddles" both Pythons using "compatible subset"
  dialect.

- Code **must** be able to open the database from both Python2 and Py3k.

- It is **not** acceptable to run a conversion process which normalizes all
  active records in the database prior to testing (e.g., the database is
  too large to convert on existing hardware, or the downtime required for
  conversion is unacceptable).

- Because disruption to the Python2 clients must be minimized, the best
  strategy is likely replace_py3k_pickle_ until convert_storages_ becomes
  feasible.

- Alternatively, wrap_storages_ might be the best strategy for the Py3k
  clients.


Strategies
----------


.. _ignore_compat:

Ignore compatibility
++++++++++++++++++++

Use the stdlib pickle support in its default mode.

- No changes to the ``ZODB`` packages on Python2 or Py3k.

- Pickles created under Python2 will be readable on Py3k;  however,
  *all* bytes data will be coerced (via ``latin1``) to unicode.

- Pickles created under Py3k will likely not be readable on Python2 (Python2
  has no support for ``protocol 3``).

- Easiest usage for applications which are never going to straddle.

- Compatibility will only be achievalble via one-time conversions (where
  the conversion script uses one of the other strategies or tools).


.. _replace_py3k_pickle:

Replace Py3k ``pickle``
+++++++++++++++++++++++

Keep pickling in the Python2 / protocol 1 way we have always done.

- No changes to the ``ZODB`` packages on Python2.  Storages do not
  need to be configured with any custom pickle support.

- On Py3k, ``ZODB`` uses pickler / unpickler from the ``zodbpickle`` module,
  such that Python2 ``str`` objects are unpickled as ``bytes``;  ``bytes``
  are pickled using the ``protocol 1`` opcodes (so that Python2 will unpickle
  them as ``str``).


.. _replace_py2_cPickle:

Replace Python2 ``cPickle``
+++++++++++++++++++++++++++

Move to pickling in the new protocol 3 way (native under Py3k).

- On Python2, applications which need to ensure that ``bytes`` objects
  unpickle correctly under Py3k need must be changed to use a new type,
  ``zodbpickle,binary``.  ``ZODB`` is configured with pickler / upickler
  from ``zodbpickle``,
  such that objects of this type will be pickled using the ``protocol 3``
  opcodes for bytes (so that Py3k will unpickle them as ``bytes``).

- Existing data for the affected classes will need to be fixed up using
  a variation of convert_storages_.

- No changes to the ``ZODB`` packages on Py3k.  Storages do not
  need to be configured with any custom pickle support.


.. _convert_storages:

Convert Database Storages
+++++++++++++++++++++++++

- Need tool(s) to identify problematic data:

  - Classes which mix ``str`` and ``unicode`` values for the same attribute
    across records / instances.

- Utility which can apply per-class transforms to state pickles:

  - E.g., for instances of ``OFS.Image.Pdata``, convert the ``data``
    attribute (which should be a Python2 ``str``) to ``zodbpickle.binary``.
    (Of course, these would probably be better off written out as blobs).

  - Or, for some application which mixes ``str`` and ``unicode`` under
    Python2 (either across instances or across transaction):  upconvert
    any value of type ``str`` for the given attribute(s) to ``unicode``,
    using a configured encoding strategy (e.g, try ``utf8`` first, falling
    back to ``latin1``).

- One-time converter utility would use ``copyTransactionsFrom``-style
  pattern, opening the existing database readonly, getting pickles for
  each transaction, invoking the converter utility for each instance
  to fix up the pickle, then writing the converted pickles into the new
  database.


.. _wrap_storages:

Wrap Database Storages
++++++++++++++++++++++

- A wrapper storage uses the converter utility (identified above) during the
  ``load`` operation, fixing up the object state it is handed to the
  instance's ``__setstate__``.

- During the ``save`` operation, the wrapper would fix up pickled instance
  state (after calling ``__getstate__``).

- Wrappers might be applied under Python2 (e.g., for apps where the
  databse is already converted to ``protocol 3``) as an alternative to
  replace_py2_cpickle_.

- Wrappers might be applied under Py3k (e.g., for apps where the
  databse is not already converted to ``protocol 3``) as an alternative to
  replace_py3k_pickle_..
