A set of **read-only** tools for validating correctness in Leaguepedia wikitext.

Some utilities may query the wiki for the purposes of validation, but no edits will be made.

Some utilities may expect wikitext objects from `mwparserfromhell` library, but templates will not be modified.

# Installation
```pip install -U git+git://github.com/RheingoldRiver/leaguepedia_validation```

# Deletion
I'm not actually using this, instead cache will be merged into `river_mwclient` and everything else will be done separately, validation isn't a well-defined-enough thing to do a lib like this for
