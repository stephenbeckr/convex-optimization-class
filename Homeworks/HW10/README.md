### Note on `handel.pkl`/`handel2.pkl`
`handel.pkl` was pickled in Python 3 with the default protocol=3, which is not
backwards compatible with the Python 2 pickler.
`handel2.pkl` was pickled with protocol=2, which is backwards compatible with
Python 2.
