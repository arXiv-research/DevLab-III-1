Usage:

go mod graph

Graph prints the module requirement graph (with replacements applied) in text form. Each line in the output has two space-separated fields: a module and one of its requirements. Each module is identified as a string of the form path@version, except for the main module, which has no @version suffix.

See https://golang.org/ref/mod#go-mod-graph for more about 'go mod graph'.
