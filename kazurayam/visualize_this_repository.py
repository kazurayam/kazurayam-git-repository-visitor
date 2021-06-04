from graphviz import Digraph
from . import visualize_git_repository

visualizer = visualize_git_repository.GitRepositoryVisualizer()
g: Digraph = visualizer.visualize(".")
g.render("tmp/this-repository", format="png")
