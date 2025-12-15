# ✈️ US Flight Delays & Cancellations Dashboard (2015)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Interactive data visualization dashboard for analyzing 2015 flight delays and cancellations across US airlines. Built with Streamlit and featuring professional data storytelling with dynamic visualizations.

## 🌐 Live Demo

**[View Dashboard on Streamlit Cloud](https://your-app-name.streamlit.app)** *(Deploy and update this link)*

## ✨ Features

### 📊 Executive Summary Dashboard
- **Real-time KPIs**: Total operations, punctuality rate, average delays, and cancellation statistics
- **Temporal trends**: Interactive daily flight volume visualization
- **Delay categorization**: Visual breakdown of flight punctuality levels
- **Weekly performance**: Dual-axis comparison of flight volume vs. average delays

### 📅 Temporal Analysis
- **Heatmap visualization**: Monthly and weekly delay patterns
- **Hourly distribution**: Flight operations by time of day
- **Seasonal trends**: Identify peak congestion periods

### 🏆 Airline Rankings
- **Performance metrics**: Comparative analysis of airline punctuality and reliability
- **Top performers**: Best and worst airlines by average delay
- **Cancelation rates**: Color-coded visual rankings

### 🗺️ Geographic Operations
- **Interactive map**: Airport locations with delay metrics
- **Top airports**: Busiest hubs with performance statistics
- **Route analysis**: Origin-destination delay patterns

### 🔍 Detailed Analysis
- **Multiple breakdown views**: By delay causes, distance, time, and cancellation reasons
- **Raw data explorer**: Full dataset access with filtering capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- `uv` (recommended) or `pip` for package management

### Installation

#### Option 1: Using `uv` (Recommended)

```bash
# Clone the repository
git clone https://github.com/DanielArizaGarcia/Data-analysis-for-the-2015-flight-dealys-and-cancelation.git
cd Data-analysis-for-the-2015-flight-dealys-and-cancelation

# Run the application (script handles environment setup automatically)
./run_app.sh
```

#### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/DanielArizaGarcia/Data-analysis-for-the-2015-flight-dealys-and-cancelation.git
cd Data-analysis-for-the-2015-flight-dealys-and-cancelation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`.

## 📁 Project Structure

```
Data-analysis-for-the-2015-flight-dealys-and-cancelation/
├── app.py                      # Main Streamlit application
├── Dani.py                     # Alternative dashboard version
├── run_app.sh                  # Automated setup & launch script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   └── config.toml            # Streamlit configuration & theme
├── flights.csv                 # Main dataset (2015 flight data)
├── airlines.csv                # Airline reference data
├── airports.csv                # Airport reference data
└── data.ipynb                  # Data preprocessing notebook
```

## 📊 Data Sources

This dashboard analyzes the **2015 Flight Delays and Cancellations** dataset, which includes:

- **5.8M+ flight records** from major US airlines
- **Origin/destination airports** across the United States
- **Delay metrics**: Departure/arrival delays, delay causes
- **Cancellation data**: Reasons and frequencies
- **Temporal information**: Date, time, and scheduling details

### Dataset Columns

Key columns used in the analysis:
- `AIRLINE`, `FLIGHT_NUMBER`: Flight identification
- `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT`: Route information
- `DEPARTURE_DELAY`, `ARRIVAL_DELAY`: Delay metrics (minutes)
- `CANCELLED`, `CANCELLATION_REASON`: Cancellation status
- `AIR_SYSTEM_DELAY`, `WEATHER_DELAY`, `AIRLINE_DELAY`, etc.: Delay cause breakdown

## 🎨 Dashboard Features in Detail

### Interactive Filters (Sidebar)
- **Date range selection**: Analyze specific time periods
- **Airline filter**: Focus on individual carriers
- **Flight status**: Toggle between operated and cancelled flights

### Professional Design
- **Custom color scheme**: Corporate blue palette with semantic color coding
- **Responsive layout**: Optimized for desktop and tablet viewing
- **Data storytelling**: Contextual insights and interpretations
- **Modern UI**: Glassmorphism effects, smooth animations, professional typography

## 🌐 Deploying to Streamlit Cloud

1. **Fork/Push to GitHub**: Ensure your repository is on GitHub
2. **Visit [Streamlit Cloud](https://streamlit.io/cloud)**
3. **Sign in** with your GitHub account
4. **Create new app**:
   - Repository: `DanielArizaGarcia/Data-analysis-for-the-2015-flight-dealys-and-cancelation`
   - Branch: `main`
   - Main file: `app.py`
5. **Deploy**: Streamlit Cloud will automatically detect `requirements.txt`

Your dashboard will be live at a URL like `https://your-app-name.streamlit.app`

### Configuration Notes

- The `.streamlit/config.toml` file contains theme customization
- Ensure all CSV data files are included in your repository or update the app to use remote data sources
- For large datasets, consider using Streamlit's caching features (already implemented)

## 🛠️ Technical Details

### Built With

- **[Streamlit](https://streamlit.io/)**: Interactive web application framework
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis
- **[Plotly](https://plotly.com/)**: Interactive visualizations
- **[Matplotlib](https://matplotlib.org/)**: Statistical graphics (used for styling)
- **[NumPy](https://numpy.org/)**: Numerical computing

### Key Features

- **Efficient data loading**: Uses `@st.cache_data` for performance optimization
- **Robust error handling**: Graceful fallbacks for missing data
- **Professional styling**: Custom CSS with modern design principles
- **Responsive charts**: Dynamic sizing and hover interactions
- **Data preprocessing**: Automated cleaning and feature engineering

## 📈 Usage Examples

### Filter by Date Range
Navigate to specific periods to analyze seasonal patterns:
```
Sidebar > Date Range > Select start and end dates
```

### Compare Airlines
Analyze individual airline performance:
```
Sidebar > Airline > Select airline name
Tab 3 > View rankings and metrics
```

### Explore Geographic Patterns
Visualize airport-level delays:
```
Tab 4 > Interactive map > Hover for details
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is for educational purposes as part of a university project on Data Storage, Visualization, and Processing.

## 👤 Author

**Daniel Ariza García**

- GitHub: [@DanielArizaGarcia](https://github.com/DanielArizaGarcia)
- Repository: [Data-analysis-for-the-2015-flight-dealys-and-cancelation](https://github.com/DanielArizaGarcia/Data-analysis-for-the-2015-flight-dealys-and-cancelation)
- University Project: Almacenamiento, Visualización y Procesamiento de Datos

## 🙏 Acknowledgments

- Dataset source: US Department of Transportation (DOT) Bureau of Transportation Statistics
- Visualization inspiration: Modern data storytelling best practices
- Built with ❤️ using Streamlit

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/DanielArizaGarcia/Data-analysis-for-the-2015-flight-dealys-and-cancelation/issues) page
2. Create a new issue with detailed information
3. Contact via GitHub discussions

---

**Star ⭐ this repository if you find it useful!**
