import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import import_ipynb

from A_i243024_Lab06 import (
    hospital_graph,
    hospital_locations,
    hospital_greedy_best_first_search as gbfs,
    a_star_search as a_star
)

# Streamlit GUI
#*******************#

# Set Page Config
st.set_page_config(
    page_title="Informed Search Visualization",
    layout="wide"
)

# write meaningful title and description for the app
st.title("Informed Search Visualization")

st.write(
    "Select the initial node, goal node, and search algorithm "
    "to find and visualize the solution path."
)

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    #pass the list of nodes to the selectbox
    nodes,
    # set the default value to "Pharmacy"
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    #pass the list of nodes to the selectbox
    nodes,
    # set the default value to "Emergency_Ward"
    index=nodes.index("Emergency_Ward")
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)


if st.button("Run Search"):

    try:

        if algorithm == "GBFS":

            # run the GBFS algorithm with the selected start and goal nodes
            path, cost, expansion_order = gbfs(
                start,
                goal,
                hospital_graph
            )

        else:

            # run the A* algorithm with the selected start and goal nodes
            path, cost, expansion_order, g_cost = a_star(
                start,
                goal,
                hospital_graph
            )

    except KeyError:
        path = None
        cost = 0

    if path is None:

       # display a error message indicating that no path was found
       st.error("No path found between the selected nodes.")

    else:
       
        # Display result
        st.subheader("Search Result")

        st.write(
            f"**Algorithm:** {algorithm}"
        )

        st.write(
            f"**Solution Path:** {' → '.join(path)}"
        )

        st.write(
            f"**Total Path Cost:** {cost:.2f}"
        )


        
        # Visualize NetworkX graph
        
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

               G.add_edge(
                   node,
                   neighbor,
                   weight=weight
               )

        pos = hospital_locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=2500,
            ax=ax
        )

        nx.draw_networkx_edges(
            G,
            pos,
            arrows=True,
            ax=ax
        )

        nx.draw_networkx_labels(
            G,
            pos,
            font_size=8,
            ax=ax
        )

        edge_labels = nx.get_edge_attributes(
            G,
            "weight"
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            ax=ax
        )

        solution_edges = list(
            zip(
                path,
                path[1:]
            )
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=solution_edges,
            edge_color="red",
            width=3,
            arrows=True,
            ax=ax
        )

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=path,
            node_color="orange",
            node_size=2500,
            ax=ax
        )

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)