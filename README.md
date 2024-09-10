# Fantasy Football League Data Exporter

This Python script connects to your ESPN Fantasy Football league, exports all relevant data about your team, matchups, players, free agents, and recent activity, and generates a detailed prompt to ask GPT for recommendations on how to improve your team. The prompt can be copied to your clipboard, and all exported data is saved in a JSON file.

## Features

- Exports your team's data, including player performance, matchups, and standings.
- Retrieves free agent information for potential roster improvements.
- Exports recent league activity such as trades and waiver wire actions.
- Copies a detailed prompt to your clipboard for use with GPT, enabling AI-driven recommendations for managing your fantasy football team.
- Saves data in JSON format for easy analysis.

## Installation

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Step 2: Install Required Packages
You’ll need to install several Python packages to run the script. You can install them with the following command:
```bash
pip install -r requirements.txt
```

### Step 3: Set Up `secrets.py`
The script requires your ESPN Fantasy Football cookies (`espn_s2` and `swid`) to authenticate with your private league. You can set these up in a `secrets.py` file.

1. Copy `secrets_example.py` to `secrets.py`:
   ```bash
   cp secrets_example.py secrets.py
   ```

2. Open `secrets.py` and replace the placeholder values with your actual `espn_s2` and `swid` cookie values. Here’s an example of what it should look like:
   ```python
   espn_s2 = "YOUR_ESPN_S2_COOKIE"
   SWID = "YOUR_SWID_COOKIE"
   ```

   You can find these cookie values by logging into ESPN Fantasy Football, opening the Developer Tools in your browser (usually by pressing F12), and looking under the "Application" tab for the cookies.

## Running the Script

Once you've installed the required packages and set up your `secrets.py`, you can run the script as follows:

```bash
python main.py
```

The script will:
1. Connect to your ESPN Fantasy Football league using the credentials from `secrets.py`.
2. Export data such as your team’s performance, player stats, matchups, free agents, and recent activity into a JSON file.
3. Copy a detailed prompt to your clipboard to ask GPT for recommendations on how to manage your team.

### Output Files
- The exported data will be saved in the `data_exports` folder in JSON format, named as `league_data_week_{week}_{timestamp}.json`.
- A file called `prompt.txt` is included with the same GPT prompt that is copied to your clipboard.

## How to Use the GPT Prompt

After running the script, the prompt for GPT will be copied to your clipboard. You can also find it in `prompt.txt`.

The prompt provides GPT with all the necessary context to analyze your fantasy football team and give you recommendations for lineup changes, trades, and other strategies.

Make sure **not** to share your `secrets.py` file on GitHub or with others, as it contains sensitive information.

## Contributing

Feel free to submit issues or pull requests if you would like to contribute to the project. Any improvements, suggestions, or bug fixes are welcome!
