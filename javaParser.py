import plyj.parser as plyj

parser = plyj.Parser()

# parse a compilation unit from a file
tree = parser.parse_file(file('SignInActivity.java'))
print tree
# parse a compilation unit from a string
#tree = parser.parse_string('class Foo { }')

# parse expression from string
#tree = parser.parse_expression('1 / 2 * (float) 3')

#tree = parser.parse_file("SignInActivity.java")