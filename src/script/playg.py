import excel_parser

s = "132"
print(s.isdigit())

s = "132a"
print(s.isdigit())

s = "132"
print(excel_parser.is_empty_integer(s))

s = ""
print(excel_parser.is_empty_integer(s))

print(s.partition("-"))
print(s.partition("-")[1])

print((s.partition("-")[1] == '-'))

print(s.partition("-")[0].lstrip().rstrip().isdigit())

print(len(str(s.partition("-")[2])) > 2)

val = ""
v = (str(val)).partition("-")
print(v)
print(v == ('', '', ''))
print(v == set(''))
