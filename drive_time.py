#!/usr/bin/env python3
"""
drive_time.py – prints live driving ETA, and (optionally) ETA n-minutes ahead.
"""
import os
import sys
import time
import json
import datetime
import argparse
from pathlib import Path
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv
import googlemaps

# Configuration
CONFIG_DIR = Path.home() / '.config' / 'drive_time'
DEFAULTS_FILE = CONFIG_DIR / 'defaults.json'

def get_gmaps_client() -> googlemaps.Client:
    """Initialize and return Google Maps client with API key validation."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY environment variable not found.")
        print("Please set it in your .env file or environment variables.")
        print("You can get an API key from: https://developers.google.com/maps/documentation/directions/get-api-key")
        sys.exit(1)
    
    try:
        return googlemaps.Client(key=api_key)
    except Exception as e:
        print(f"Error initializing Google Maps client: {str(e)}")
        print("Please check your API key and ensure it's valid.")
        sys.exit(1)

load_dotenv()
try:
    gmaps = get_gmaps_client()
    # Test the client with a simple request
    gmaps.geocode('Test', timeout=2)
except Exception as e:
    print(f"Error: Failed to connect to Google Maps API: {str(e)}")
    print("Please check your internet connection and API key permissions.")
    sys.exit(1)

def eta_minutes(origin: str, destination: str, depart_epoch: int) -> tuple[float, str, str, str]:
    """
    Return driving time in minutes, formatted addresses, and distance.
    
    Returns:
        tuple: (travel_time_minutes, formatted_origin, formatted_destination, distance_text)
    """
    result = gmaps.directions(
        origin,
        destination,
        mode="driving",
        departure_time=depart_epoch,  # now or any future second
        traffic_model="best_guess"
    )
    
    leg = result[0]["legs"][0]
    seconds = leg["duration_in_traffic"]["value"]
    formatted_origin = leg["start_address"]
    formatted_destination = leg["end_address"]
    distance = leg["distance"]["text"]
    
    return round(seconds / 60, 1), formatted_origin, formatted_destination, distance

def load_defaults() -> Optional[Dict[str, str]]:
    """Load saved default addresses from config file."""
    try:
        with open(DEFAULTS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_defaults(origin: str, destination: str) -> None:
    """Save the given addresses as defaults."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(DEFAULTS_FILE, 'w') as f:
        json.dump({"origin": origin, "destination": destination}, f)

def get_addresses() -> Tuple[str, str]:
    """Get origin and destination from defaults or prompt user."""
    defaults = load_defaults()
    if not defaults:
        print("No default addresses found. Please provide addresses.")
        origin = input("Enter origin address or 'lat,lng': ").strip()
        destination = input("Enter destination address or 'lat,lng': ").strip()
        return origin, destination
    return defaults['origin'], defaults['destination']

def main() -> None:
    """
    Parse command line arguments and display driving time estimates.
    
    Shows current ETA and optionally future ETA if --future flag is provided.
    """
    parser = argparse.ArgumentParser(
        description="Live driving time and optional future‐traffic forecast")
    parser.add_argument("origin", nargs='?', help="start address or 'lat,lng'")
    parser.add_argument("destination", nargs='?', help="end address or 'lat,lng'")
    parser.add_argument("-f", "--future", type=int, metavar="N",
                        help="also show ETA if leaving N minutes from now")
    parser.add_argument("-d", "--defaults", action="store_true",
                        help="save the provided addresses as defaults")
    args = parser.parse_args()

    # If no addresses provided, try to load defaults
    if args.origin is None or args.destination is None:
        if args.defaults:
            print("Error: Must provide addresses when using --defaults")
            parser.print_help()
            return
        args.origin, args.destination = get_addresses()
    
    # Save as defaults if requested
    if args.defaults:
        save_defaults(args.origin, args.destination)
        print(f"Saved default addresses: {args.origin} → {args.destination}")

    try:
        now = int(time.time())
        # Get current ETA, formatted addresses, and distance
        current_eta, formatted_origin, formatted_destination, distance = eta_minutes(args.origin, args.destination, now)
        
        # Update origin and destination with formatted versions
        args.origin, args.destination = formatted_origin, formatted_destination
        
        # Calculate average speed in mph
        distance_mi = float(distance.split()[0])  # Extract numeric value from '32.4 mi'
        hours = current_eta / 60
        avg_speed = distance_mi / hours if hours > 0 else 0
        
        # Calculate estimated arrival time
        current_time = datetime.datetime.now()
        arrival_time = current_time + datetime.timedelta(minutes=current_eta)
        
        print(f"Route: {formatted_origin} → {formatted_destination} ({distance})")
        print(f"Current ETA: {arrival_time.strftime('%-I:%M %p')} ({current_eta:.1f} min, {distance_mi:.1f} mi @ {avg_speed:.1f} mph)")
    
        if args.future is not None:
            future_epoch = now + args.future * 60
            future_eta, _, _, future_distance = eta_minutes(args.origin, args.destination, future_epoch)
            future_distance_mi = float(future_distance.split()[0])
            future_hours = future_eta / 60
            future_avg_speed = future_distance_mi / future_hours if future_hours > 0 else 0
            future_arrival = current_time + datetime.timedelta(minutes=args.future + future_eta)
            print(f"ETA in {args.future} min: {future_arrival.strftime('%-I:%M %p')} ({future_eta:.1f} min, {future_distance_mi:.1f} mi @ {future_avg_speed:.1f} mph)")
    except Exception as e:
        print(f"Error: {str(e)}")
        if "ZERO_RESULTS" in str(e):
            print("No route found between the specified addresses.")

if __name__ == "__main__":
    main()