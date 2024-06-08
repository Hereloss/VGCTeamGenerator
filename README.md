# VGC Team Generator

A Pokemon VGC Team Generator using last month's stats to build a sample (potentially!) viable team

## Description

This generator will generate a whole 6 Pokemon team for VGC Reg G using last month's usage stats. It will then paste them out as a Showdown paste in the terminal, ready to use. The teams will be potentially viable - you may need to tweak them! They should give you some good ideas, and are probably most useful for low usage pokemon.
All stats are gotten from Munchstats, and then parsed using Python to get percentages. A random number is generated, and this is used to pick the moves, items, nature and teammates. This means it will likely be using the most normal setup - but could be using something strange! 
As not all moves/teammates are recorded on Munchstats, they will not be able to use every teammate - so it's advisable to put the least common Pokemon as your captain

## Getting Started

### Dependencies

Python 3 with htmlToText dependency and something to run it on!

### Installing

* Download the Gitlab Repo
* Build

### Executing program

* Run by running the main class - it will prompt you for your main Pokemon, BO3 (if not, will be BO1) and if you want to name your whole team (at which point it will just generate details for the Pokemon)
* It will then print out a Showdown paste that you can paste directly into Pokemon Showdown to test or further tweak the team

* If you wish to generate this for other Metagames, please edit the URL at the top accordingly (and say no to BO3 games)


## Help

No issues detected yet - but if there are any, please contact me directly

## Version History

* 0.1
    * Initial Release

## License

This project is licensed for personal use only. Any other use, please contact me directly
