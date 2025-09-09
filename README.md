# Smart City Technology Flow Visualization

An interactive Sankey diagram visualization showing the flow between industries, companies, technologies, and key technology categories in smart city development.

## Quick Setup

### Option 1: Run on Replit (Recommended for Sharing)

1. **Go to [Replit.com](https://replit.com)** and sign up/login
2. **Click "Create Repl"**
3. **Select "Import from GitHub"**
4. **Enter your GitHub repository URL**
5. **Click "Import"**
6. **Click the green "Run" button**
7. **Access your visualization at the provided URL**

### Option 2: Local Setup

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

#### Installation & Running

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser and navigate to:**
   ```
   http://localhost:8080
   ```

## Features

- **Interactive Sankey Diagram**: Visualize technology flows between industries, companies, and technologies
- **Zoom & Pan**: Use toolbar controls to explore the visualization
- **Color-coded Categories**: Different colors for industries and technologies
- **Export Options**: Save visualizations as PNG images
- **Responsive Design**: Works on desktop and mobile devices

## Data Structure

The visualization is based on `sankey_clean_data.csv` which contains:
- **Industries**: Architecture & Design (ACDP), Consulting, Technology
- **Companies**: Various companies within each industry
- **Technologies**: AI, IoT, Cloud, Blockchain, Data Analytics, etc.
- **Key Tech Categories**: AI & Machine Learning, Analytics & Visualization, User Interface/Platform, Decision Making

## Troubleshooting

### Local Setup Issues
- **Port already in use**: If port 8080 is busy, the app will show an error. Kill any existing Python processes or modify the port in `app.py`
- **Missing dependencies**: Make sure all packages in `requirements.txt` are installed
- **Data not loading**: Ensure `sankey_clean_data.csv` is in the same directory as `app.py`

### Replit Issues
- **App not starting**: Make sure you clicked the "Run" button in Replit
- **Dependencies not installing**: Replit should auto-install from `requirements.txt`, but you can manually run `pip install -r requirements.txt` in the console
- **App sleeping**: Replit free tier puts apps to sleep after inactivity. Just refresh the page or click "Run" again

## Stopping the Application

Press `Ctrl+C` in the terminal to stop the Flask server.

---

**Note**: This is a development server. For production deployment, use a proper WSGI server like Gunicorn or uWSGI.
