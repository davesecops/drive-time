# Drive Time

A command-line tool to get live driving ETAs with traffic information using Google Maps API.

## Features

- Get current driving time with traffic
- Save default origin and destination addresses
- Check future ETAs based on departure time
- Clean, formatted output with distance and average speed
- Simple command-line interface

## Prerequisites

- Python 3.10 or higher
- Google Maps API key with Directions API enabled

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd drive-time
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   conda create -n drive-time python=3.10
   conda activate drive-time
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add your Google Maps API key:
   ```
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage
```bash
python drive_time.py "Origin Address" "Destination Address"
```

### Save Default Addresses
```bash
python drive_time.py -d "Home Address" "Work Address"
```

### Check Future Travel Time
```bash
python drive_time.py -f 30  # Check ETA if leaving in 30 minutes
```

### Using Saved Defaults
```bash
python drive_time.py  # Uses saved default addresses
```

## Options

- `-d, --defaults`: Save the provided addresses as defaults
- `-f N, --future N`: Show ETA if leaving in N minutes

## Configuration

Default addresses are stored in `~/.config/drive_time/defaults.json`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
