import graphviz

# Create a new directed graph using neato for precise positioning
dot = graphviz.Digraph(comment='AI Learning Progression', format='png', engine='neato')

# Set graph attributes - increased width for more white background
dot.attr(size='18,12', dpi='300', splines='ortho')
dot.attr('node', shape='oval', style='filled', fontname='Arial', fontsize='32',
         width='6', height='1.5', fixedsize='true')
dot.attr('edge', fontname='Arial')


# Define positions for main nodes (x,y coordinates)
# Coding and Financial Analysis horizontally aligned
dot.node('C', 'Coding', fillcolor='#e6f3ff', pos='3,10!')  # Light blue (start of sequence)
dot.node('FA', 'Financial Analysis', fillcolor='lightgreen', pos='10,10!')

# Other nodes below Coding - sequential blues getting darker
# Adjusted vertical spacing for 3 nodes instead of 4
dot.node('CC', 'Custom Chatbots', fillcolor='#80bfff', pos='3,7!')  # Medium blue
dot.node('AA', 'Apps and Agents', fillcolor='#4da6ff', pos='3,4!')  # Darker blue


# Main progression arrows
# Horizontal arrow from Coding to Financial Analysis
dot.edge('C', 'FA', color='black', penwidth='4')
# Vertical arrow from Coding to Custom Chatbots
dot.edge('C', 'CC', color='blue', penwidth='2.5')
# Continue vertical progression
dot.edge('CC', 'AA', color='blue', penwidth='2.5')

# Create invisible nodes for the return path
# All right nodes at exactly x=10 (center of Financial Analysis) for perfect vertical alignment
dot.attr('node', shape='point', width='0.01', height='0.01', style='invis')

dot.node('CC_right', '', pos='10,7!')
dot.node('AA_right', '', pos='10,4!')

# Horizontal lines extending right from each oval to center of Financial Analysis
dot.edge('CC', 'CC_right', color='black', penwidth='4', dir='none')
dot.edge('AA', 'AA_right', color='black', penwidth='4', dir='none')

# Single vertical line from Apps and Agents level up to Financial Analysis (with arrow)
dot.edge('AA_right', 'CC_right', color='black', penwidth='4', dir='none')
dot.edge('CC_right', 'FA', color='black', penwidth='4')

# Save the diagram
dot.render('ai_progression2', directory='.', cleanup=True)
print("Diagram created as ai_progression2")