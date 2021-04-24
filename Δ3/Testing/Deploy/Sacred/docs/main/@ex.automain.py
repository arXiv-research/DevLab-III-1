from sacred import Experiment
ex = Experiment()

@ex.main
def my_main():
    pass

if __name__ == '__main__':
    ex.run_commandline()
