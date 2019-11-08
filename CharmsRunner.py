from antlr4 import *
from antlr4.tree.Trees import Trees
from CharmsLexer import CharmsLexer
from CharmsParserListener import CharmsParserListener
from CharmsParser import CharmsParser
from Quad import Quad
from Variable import Variable
from VariableTable import VariableTable
import sys

class CharmsPrintListener(CharmsParserListener):
	def exitType_id(self, ctx):
		global varType
		if ctx.INT():
			varType = "int"
		elif ctx.CHAR():
			varType = "char"
		elif ctx.BOOL():
			varType = "bool"
		else:
			Exception("{} is not a valid data type".format(varType))

	def exitVar_cte(self, ctx):
		myId = str(ctx.ID())
		myCTE_INT = str(ctx.CTE_INT())
		if myId != "None":
			stackOperands.append(myId)
			stackTypes.append(varTable.getVariableType(myId))
		else:
			stackOperands.append(int(myCTE_INT))
			stackTypes.append("int")
		# print("stackOperands:")
		# print(stackOperands)
		# print("stackTypes:")
		# print(stackTypes)

	def exitE1(self, ctx):
		operator = ctx.PLUS() or ctx.MINUS()
		operator = str(operator)
		if operator != "None":
			stackOperators.append(operator)
		# print("stackOperator:")
		# print(stackOperators)

	def addVar(self, ctx):
		global varId
		varId = str(ctx.ID()) # cast to string to avoid dealing with TerminalNode objects
		if varId != "None":
			varTable.insertVariable(varId, varType, "global")
			# varTable.printTable()

	def enterV(self, ctx):
		self.addVar(ctx)

	def enterV1(self, ctx):
		self.addVar(ctx)

def main(argv):
	global varTable
	global stackOperands
	global stackOperators
	global stackTypes
	global queueQuads
	stackOperands = []
	stackOperators = []
	stackTypes = []
	queueQuads = []

	varTable = VariableTable({}, ["int", "void", "bool", "char", "if", "else", "while", "print", "read", "return", "function", "id"])
	lexer = CharmsLexer(StdinStream())
	stream = CommonTokenStream(lexer)
	parser = CharmsParser(stream)
	printer = CharmsPrintListener()
	walker = ParseTreeWalker()
	tree = parser.program()
	walker.walk(printer, tree)
	# print(Trees.toStringTree(tree, None, parser))

if __name__ == '__main__':
    main(sys.argv)
