from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import json

app = Flask(__name__)

def get_category_color(category_type, category):
    color_map = {
        'Industry': {
            'ACDP': '#3498DB',       # Blue
            'CONSULTING': '#9B59B6',  # Purple
            'TECH': '#2ECC71',       # Green
        },
        'Technology': {
            'AI': '#E74C3C',         # Red
            'IoT': '#F39C12',        # Orange
            'Cloud': '#3498DB',      # Light Blue
            'Blockchain': '#2ECC71',  # Light Green
            'Data Analytics': '#9B59B6',  # Purple
            'Data Visualisation': '#9B59B6',  # Purple
            'Building Information Modeling': '#E67E22',  # Dark Orange
            'Generative Design': '#16A085',  # Turquoise
            'Urban Data Analytics': '#8E44AD',  # Dark Purple
            'Real-Time Evaluation': '#E74C3C',  # Red
            'Simulation & Visualization': '#F39C12',  # Orange
            'Data Interpretation': '#9B59B6',  # Purple
            'User Interface': '#3498DB',  # Blue
            'Dashboard': '#2ECC71',  # Green
            'Parametric Design': '#E67E22',  # Dark Orange
            'Parametric Optimization': '#16A085',  # Turquoise
            'Typology Analysis': '#8E44AD',  # Dark Purple
            'Performance Optimization': '#E74C3C',  # Red
            'Geometry Generation': '#F39C12',  # Orange
            'Analytics & Visualization': '#9B59B6',  # Purple
            'AI & Machine Learning': '#E74C3C',  # Red
            'Digital Twins': '#E67E22',  # Dark Orange
            'User Interface/Platform': '#3498DB',  # Blue
            'Decision Making': '#2ECC71',  # Green
            'Sustainability': '#16A085',  # Turquoise
            'Revenue & Cost Optimization': '#8E44AD',  # Dark Purple
            'Platform': '#F39C12',  # Orange
            'Software Tech': '#95A5A6',  # Gray
            'API': '#34495E',  # Dark Gray
            'Automation': '#E74C3C',  # Red
        }
    }
    return color_map.get(category_type, {}).get(category, '#95A5A6')  # Default gray

def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

def create_sankey_diagram():
    try:
        # Read the clean CSV file
        df_clean = pd.read_csv('sankey_clean_data.csv')
        
        # Clean up the data
        df_clean = df_clean.dropna(subset=['Industry', 'Company', 'Technology'])
        
        # Sort companies by industry and frequency
        company_freq = df_clean['Company'].value_counts()
        df_clean['company_freq'] = df_clean['Company'].map(company_freq)
        
        # Sort technologies by frequency
        tech_freq = df_clean['Technology'].value_counts()
        df_clean['tech_freq'] = df_clean['Technology'].map(tech_freq)
        
        # Get unique values for each category
        industries = sorted(df_clean['Industry'].unique())
        companies = df_clean.groupby('Industry')['Company'].unique()
        companies = [item for sublist in companies for item in sublist]  # Flatten list
        technologies = sorted(df_clean['Technology'].unique(), key=lambda x: -tech_freq[x])
        key_techs = sorted(df_clean['Key Tech'].unique())
        
        # Create nodes list with specific ordering
        all_nodes = (
            list(industries) +    # First layer
            list(companies) +     # Second layer
            list(technologies) +  # Third layer
            list(key_techs)      # Fourth layer
        )
        node_indices = {node: idx for idx, node in enumerate(all_nodes)}
        
        # Calculate y-positions for better organization
        y_positions = []
        current_y = 0
        
        # Position industries evenly with compact spacing
        industry_spacing = 0.8 / (len(industries) + 1)  # Reduced from 1.0 to 0.8
        for _ in industries:
            current_y += industry_spacing
            y_positions.append(current_y)
        
        # Position companies based on their industry with compact spacing
        company_y = {}
        for industry in industries:
            industry_companies = df_clean[df_clean['Industry'] == industry]['Company'].unique()
            spacing = industry_spacing / (len(industry_companies) + 1)
            industry_y = y_positions[industries.index(industry)]
            for i, company in enumerate(industry_companies, 1):
                company_y[company] = industry_y - industry_spacing/2 + i * spacing
        
        for company in companies:
            y_positions.append(company_y[company])
        
        # Position technologies with compact spacing
        tech_spacing = 0.8 / (len(technologies) + 1)  # Reduced from 1.0 to 0.8
        for i in range(len(technologies)):
            y_positions.append(0.1 + (i + 1) * tech_spacing)  # Added 0.1 offset
        
        # Position key techs with compact spacing
        key_tech_spacing = 0.8 / (len(key_techs) + 1)  # Reduced from 1.0 to 0.8
        for i in range(len(key_techs)):
            y_positions.append(0.1 + (i + 1) * key_tech_spacing)  # Added 0.1 offset
        
        # Create node colors with adjusted transparency
        node_colors = []
        for node in all_nodes:
            if node in industries:
                node_colors.append(get_category_color('Industry', node))
            elif node in technologies:
                node_colors.append(get_category_color('Technology', node))
            elif node in key_techs:
                node_colors.append('#34495E')  # Dark gray for key techs
            else:
                # Companies get a lighter version of their industry color
                industry = df_clean[df_clean['Company'] == node]['Industry'].iloc[0]
                node_colors.append(hex_to_rgba(get_category_color('Industry', industry), 0.8))
        
        # Create links with adjusted values for better visibility
        sources = []
        targets = []
        values = []
        link_colors = []
        
        # Industry to Company links
        for industry in industries:
            industry_companies = df_clean[df_clean['Industry'] == industry]['Company'].unique()
            for company in industry_companies:
                count = len(df_clean[(df_clean['Industry'] == industry) & (df_clean['Company'] == company)])
                sources.append(node_indices[industry])
                targets.append(node_indices[company])
                values.append(count * 1.5)  # Adjusted weight
                link_colors.append(hex_to_rgba(get_category_color('Industry', industry), 0.4))
        
        # Company to Technology links
        for _, row in df_clean.groupby(['Company', 'Technology']).size().reset_index(name='count').iterrows():
            sources.append(node_indices[row['Company']])
            targets.append(node_indices[row['Technology']])
            values.append(row['count'])
            industry = df_clean[df_clean['Company'] == row['Company']]['Industry'].iloc[0]
            link_colors.append(hex_to_rgba(get_category_color('Industry', industry), 0.3))
        
        # Technology to Key Tech links
        for _, row in df_clean.groupby(['Technology', 'Key Tech']).size().reset_index(name='count').iterrows():
            sources.append(node_indices[row['Technology']])
            targets.append(node_indices[row['Key Tech']])
            values.append(row['count'])
            link_colors.append(hex_to_rgba(get_category_color('Technology', row['Technology']), 0.3))
        
        # Create Sankey diagram with improved layout
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=40,        # Adjusted padding
                thickness=15,  # Reduced thickness
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color=node_colors,
                x=[0.05 if node in industries else 
                   0.35 if node in companies else
                   0.65 if node in technologies else
                   0.95 for node in all_nodes],  # Adjusted column positions
                y=y_positions
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=link_colors
            ),
            arrangement='snap'  # Keep only valid properties
        )])
        
        # Update layout with zoom capabilities
        fig.update_layout(
            title=dict(
                text="Smart City Technology Flow Analysis",
                font=dict(size=24, color='#2C3E50'),
                x=0.5,
                y=0.98
            ),
            font=dict(size=12, color='#2C3E50'),
            height=900,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=60, l=20, r=20, b=20),
            hovermode='closest',
            dragmode='zoom',
            showlegend=False,
            modebar=dict(
                orientation='v',
                bgcolor='rgba(255,255,255,0.7)',
                color='#2C3E50',
                activecolor='#34495E'
            )
        )
        
        return json.dumps(fig.to_dict())
    except Exception as e:
        print(f"Error creating Sankey diagram: {str(e)}")
        return json.dumps({})

@app.route('/')
def index():
    sankey_data = create_sankey_diagram()
    return render_template('index.html', sankey_data=sankey_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 