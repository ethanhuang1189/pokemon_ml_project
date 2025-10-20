# Pokemon Battle Bot ML Project Website

This is the project documentation website for the Pokemon Battle Bot ML project.

## Viewing the Website

Simply open `index.html` in your web browser to view the full project documentation, including:

- **Project Overview**: Mission and goals
- **Bot Descriptions**: Detailed information about all 3 bots (Random, Max Damage, Custom Strategy)
- **Performance Data**: Interactive charts showing battle results
- **ML Roadmap**: Plans for machine learning implementation
- **Challenges**: Technical difficulties and how to overcome them
- **Future Plans**: Short, medium, and long-term goals

## Battle Data

The `battle_results.json` file contains results from 50 battles per matchup:
- Random vs Max Damage
- Random vs Custom Strategy
- Max Damage vs Custom Strategy

This data is visualized in the interactive Chart.js graphs on the website.

## Key Insights

The website demonstrates that:
1. **Custom Strategy Bot performs best** (~66% overall win rate)
2. **Max Damage Bot is competitive** (~52% overall win rate)
3. **Type effectiveness matters** more than raw power
4. **Multi-factor strategies** outperform single-factor approaches
5. There's **significant room for ML improvement**

## Next Steps

To run more battles and update the data:
1. Ensure Pokemon Showdown server is running on port 8000
2. Run `python analyze_battles.py` from the root directory
3. Battle results will update `battle_results.json`
4. Refresh the website to see updated graphs
