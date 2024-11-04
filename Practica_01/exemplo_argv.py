import sys, os 


def main():
	print('Introducíronse', len(sys.argv)-1,'argumentos')
	print('Nome do programa:', sys.argv[0])
	i=1
	for arg in sys.argv[1:]:
		print('Argumento',i,':',arg)
		i+=1
		
		
		
		
if __name__ == "__main__":
    main()
		
		