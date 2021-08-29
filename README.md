## Run locally
`python3 -m venv venv`  
`source venv/bin/activate`  
`python ./bin/run_locally.py`  
http://localhost:8000/docs  

## Game Workflow

* Player A creates a Game (so called the game master)
* Player B joins the Game (through a join link)
* Player C joins the Game (For now minimum players 3)
* Player D joins the Game
* ...
* Player A (master) starts the first Round 
  * A statement and participants are provided
  * Participants are the players who will act for/against the statement
* The participants will defend their positions
  * For the given amount of time, default 90secs
* Starts Voting process
  * Participants can't vote
  * Every Player can vote just once per round
  * The winner increases the score
* Player A starts next round
* ...
