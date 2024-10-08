# Empire Eats Telegram Bot

This Telegram bot helps users find nearby restaurants and photogenic spots based on their location. The bot provides food recommendations and aesthetic photo opportunities, perfect for those who want to enjoy a hearty meal and capture beautiful moments.

## Features

- **Food Recommendations**: Get a list of highly rated restaurants based on your location.
- **Photogenic Spots**: Discover top photogenic locations near you and view aesthetic images of those spots.

## How It Works

### Commands

- **/start**: Initiates the bot and presents you with two options:
  - **FOOD**: Enter your location to receive restaurant recommendations.
  - **PHOTOS**: Enter your location to discover photogenic spots with accompanying images.

### Workflow

1. **Start the bot**: The user starts the bot by typing `/start`, which triggers the bot to display options for food or photo recommendations.
2. **Select an option**: The user selects either "FOOD" or "PHOTOS".
   - If **FOOD** is selected, the user is prompted to enter a location (city, neighborhood, country, etc.). The bot then provides a list of nearby restaurants based on the criteria of minimum rating and review count.
   - If **PHOTOS** is selected, the user is prompted to enter a location. The bot then finds nearby photogenic spots and sends images of these spots using the Unsplash API.
3. **Restart or End**: After the results are provided, the user is asked whether they want to restart the process or end the session.

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/ogngnaoh/food-n-photos.git
   cd yourrespository
   ```

2. **Install dependencies**:
   Ensure you have `pip` installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   UNSPLASH_API_KEY=your_unsplash_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

4. **Run the bot**:
   Start the bot by running:
   ```
   python main.py
   ```

## Project Structure

- **main.py**: The main file that handles the Telegram bot logic, including command handlers and conversation flow.
- **google_api.py**: Contains functions for interacting with the Google Maps API to fetch coordinates, nearby restaurants, and photogenic spots.
- **unsplash_api.py**: Contains functions for fetching photos from Unsplash based on the location.
- **messages.py**: Stores the messages sent to users by the bot, including the start and selection messages.

## Usage

To use this bot, simply start it on Telegram, choose whether you want food recommendations or photo spots, and provide your location. The bot will handle the rest, giving you a curated list of either restaurants or beautiful spots along with images.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.