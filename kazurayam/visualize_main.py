from graphviz import Digraph
from . import visualize_git_repository

if __name__ == '__main__':
    print('__package__: {}, __name__: {}'.format(__package__, __name__))
    visualizer = visualize_git_repository.GitRepositoryVisualizer()
    g: Digraph = visualizer.visualize("tmp/test_visualize")
    g.render("tmp/visualize_main_output", format="png")


