# Economic and Population Comparison Tool

## Overview

The **Economic and Population Comparison Tool** is a Streamlit application that allows users to visualize and compare various economic and population metrics across countries and groups. The application fetches data from the World Bank API and presents it using interactive charts from Plotly.

## Features

- **Country Comparison**: Compare economic and population metrics of a selected country with the global average.
- **Group Comparison**: Compare economic and population metrics of a selected group of countries with the global average and within the group.
- **Country vs. Country**: Compare metrics between two selected countries over a specified range of years.
- **Group vs. Group**: Compare metrics between two selected groups of countries over a specified range of years.
- **Chart Types**: Supports various chart types including bar, pie, line, and scatter.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/economic-comparison-tool.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd economic-comparison-tool
    ```

3. **Set up a virtual environment (optional but recommended)**:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Streamlit application**:

    ```bash
    streamlit run app.py
    ```

## Usage

Once the application is running, you can use the sidebar to select different types of analyses and customize your charts:

- **Analysis Type**: Choose between "Country Comparison", "Group Comparison", "Country vs. Country", and "Group vs. Group".
- **Chart Type**: Select the type of chart you want to visualize the data (bar, pie, line, scatter).
- **Metric**: Choose the metric you want to compare (Population, GDP, GDP Growth Rate).

## Code Structure

- **`app.py`**: The main Streamlit application script.
- **`requirements.txt`**: List of required Python packages.
- **`data_fetching.py`**: Contains functions for fetching and processing data from the World Bank API (if separate).
- **`plotting.py`**: Contains functions for plotting different types of charts (if separate).

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. For detailed information on contributing, refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please open an issue or contact [your email](mailto:youremail@example.com).

